"""Base builder with shared compile/execute logic."""

import re


def _snake_to_camel(name):
    """Convert snake_case to camelCase."""
    parts = name.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])


# Maps Python argument types to GraphQL type strings
_GRAPHQL_TYPES = {
    "id": "Int",
    "idMal": "Int",
    "search": "String",
    "type": "MediaType",
    "format": "MediaFormat",
    "format_in": "[MediaFormat]",
    "status": "MediaStatus",
    "season": "MediaSeason",
    "seasonYear": "Int",
    "isAdult": "Boolean",
    "onList": "Boolean",
    "sort": "[MediaSort]",
    "page": "Int",
    "perPage": "Int",
    "isBirthday": "Boolean",
}

# Root-level entity type overrides for sort arguments
_ENTITY_SORT_TYPES = {
    "Character": "[CharacterSort]",
    "Staff": "[StaffSort]",
    "Studio": "[StudioSort]",
    "Page": None,  # handled by page builder
}


class BaseBuilder:
    """Base class for all GraphQL query builders.

    Each builder tracks a root field (e.g. "Media"), root arguments,
    selected fields, and optional pagination wrapping.
    """

    _graphql_type = "Media"  # Override in subclasses

    def __init__(self, request_fn, async_request_fn, root_field, root_args):
        self._request = request_fn
        self._async_request = async_request_fn
        self._root_field = root_field
        self._root_args = root_args  # {"id": 13601, "type": "ANIME"}
        self._fields = []  # list of (field_str,) — pre-formatted field strings
        self._fragments = []
        self._page_args = None

    def use(self, *fragments):
        """Apply Fragment selections to this builder."""
        for frag in fragments:
            self._fragments.append(frag)
        return self

    def page(self, page=1, per_page=10):
        """Wrap this query in Page { pageInfo { ... } }."""
        self._page_args = {"page": page, "perPage": per_page}
        return self

    def _add_scalar(self, name):
        self._fields.append(name)

    def _add_object(self, graphql_name, sub_fields, defaults=None):
        """Add an object field with sub-field selection.

        Args:
            graphql_name: The GraphQL field name (e.g. "title")
            sub_fields: Tuple of selected sub-field names, or empty for defaults
            defaults: Default sub-fields if none provided
        """
        if not sub_fields and defaults:
            sub_fields = defaults
        if not sub_fields:
            return
        inner = " ".join(sub_fields)
        self._fields.append(f"{graphql_name} {{ {inner} }}")

    def _add_connection(self, graphql_name, *, args=None, fields_fn=None,
                        node_type=None, edge_fields=None):
        """Add a connection/nested field with optional arguments and sub-builder.

        Args:
            graphql_name: e.g. "characters"
            args: Dict of arguments like {"perPage": 5, "sort": ["FAVOURITES_DESC"]}
            fields_fn: Lambda that receives a sub-builder and configures it
            node_type: The builder class for the sub-selection (e.g. CharacterBuilder)
            edge_fields: Additional edge-level fields to include
        """
        parts = []
        # Build argument string
        arg_str = ""
        if args:
            arg_parts = []
            for k, v in args.items():
                if v is None:
                    continue
                arg_parts.append(f"{k}: {_format_arg_value(v)}")
            if arg_parts:
                arg_str = f"({', '.join(arg_parts)})"

        if fields_fn and node_type:
            sub = node_type(None, None, "", {})
            fields_fn(sub)
            # Merge fragment fields too
            all_fields = list(sub._fields)
            for frag in sub._fragments:
                all_fields.extend(frag._fields)
            inner = " ".join(all_fields)
            if edge_fields:
                edge_inner = " ".join(edge_fields)
                parts.append(f"{graphql_name}{arg_str} {{ edges {{ {edge_inner} node {{ {inner} }} }} }}")
            else:
                parts.append(f"{graphql_name}{arg_str} {{ nodes {{ {inner} }} }}")
        elif fields_fn:
            # fields_fn provided but no node_type — treat as raw
            parts.append(f"{graphql_name}{arg_str}")
        else:
            # No sub-selection — use default minimal selection
            parts.append(f"{graphql_name}{arg_str}")

        for p in parts:
            self._fields.append(p)

    def _collect_fields(self):
        """Collect all fields including from fragments."""
        all_fields = list(self._fields)
        for frag in self._fragments:
            all_fields.extend(frag._fields)
        return all_fields

    def _compile(self):
        """Build the GraphQL query string and variables dict.

        Returns:
            (query_string, variables_dict)
        """
        all_fields = self._collect_fields()
        if not all_fields:
            # Default to id if no fields selected
            all_fields = ["id"]

        fields_str = "\n      ".join(all_fields)
        variables = dict(self._root_args)

        if self._page_args:
            return self._compile_paginated(fields_str, variables)
        return self._compile_single(fields_str, variables)

    def _compile_single(self, fields_str, variables):
        """Compile a non-paginated query."""
        # Build variable declarations
        var_decls = []
        for key, val in variables.items():
            gql_type = _infer_type(key, val, self._graphql_type)
            var_decls.append(f"${key}: {gql_type}")

        var_str = f"({', '.join(var_decls)})" if var_decls else ""

        # Build root field arguments
        arg_parts = [f"{k}: ${k}" for k in variables]
        arg_str = f"({', '.join(arg_parts)})" if arg_parts else ""

        query = f"""query {var_str} {{
  {self._root_field}{arg_str} {{
      {fields_str}
  }}
}}"""
        return query, variables

    def _compile_paginated(self, fields_str, variables):
        """Compile a paginated query wrapped in Page {}."""
        variables.update(self._page_args)

        # Determine the collection field name for inside Page
        collection_field = _root_to_collection(self._root_field)

        # Build variable declarations
        var_decls = []
        for key, val in variables.items():
            gql_type = _infer_type(key, val, self._graphql_type)
            var_decls.append(f"${key}: {gql_type}")

        var_str = f"({', '.join(var_decls)})" if var_decls else ""

        # Page-level args
        page_arg_parts = ["page: $page", "perPage: $perPage"]
        page_arg_str = f"({', '.join(page_arg_parts)})"

        # Entity-level args (everything except page/perPage)
        entity_args = {k: v for k, v in variables.items() if k not in ("page", "perPage")}
        entity_arg_parts = [f"{k}: ${k}" for k in entity_args]
        entity_arg_str = f"({', '.join(entity_arg_parts)})" if entity_arg_parts else ""

        query = f"""query {var_str} {{
  Page{page_arg_str} {{
    pageInfo {{
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }}
    {collection_field}{entity_arg_str} {{
      {fields_str}
    }}
  }}
}}"""
        return query, variables

    def execute(self, **kwargs):
        """Compile and execute the query synchronously."""
        query, variables = self._compile()
        return self._request(variables, query, **kwargs)

    async def execute_async(self, **kwargs):
        """Compile and execute the query asynchronously."""
        if self._async_request is None:
            raise RuntimeError("Async connection not available. Install aiohttp: pip install anisearch[async]")
        query, variables = self._compile()
        return await self._async_request(variables, query, **kwargs)


def _format_arg_value(v):
    """Format a Python value as a GraphQL inline argument value."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        # Enum values are unquoted, strings in quotes
        # Heuristic: ALL_CAPS = enum
        if re.match(r'^[A-Z_]+$', v):
            return v
        return f'"{v}"'
    if isinstance(v, list):
        items = ", ".join(_format_arg_value(i) for i in v)
        return f"[{items}]"
    return str(v)


def _infer_type(key, value, entity_type="Media"):
    """Infer GraphQL type from variable name and value."""
    # Known mappings
    known = {
        "id": "Int",
        "idMal": "Int",
        "search": "String",
        "type": "MediaType",
        "format": "MediaFormat",
        "format_in": "[MediaFormat]",
        "status": "MediaStatus",
        "season": "MediaSeason",
        "seasonYear": "Int",
        "isAdult": "Boolean",
        "onList": "Boolean",
        "isBirthday": "Boolean",
        "page": "Int",
        "perPage": "Int",
        "countryOfOrigin": "CountryCode",
        "source": "MediaSource",
        "year": "String",
        "yearLesser": "FuzzyDateInt",
        "yearGreater": "FuzzyDateInt",
        "episodeLesser": "Int",
        "episodeGreater": "Int",
        "durationLesser": "Int",
        "durationGreater": "Int",
        "chapterLesser": "Int",
        "chapterGreater": "Int",
        "volumeLesser": "Int",
        "volumeGreater": "Int",
        "licensedBy": "[Int]",
        "isLicensed": "Boolean",
        "genres": "[String]",
        "excludedGenres": "[String]",
        "tags": "[String]",
        "excludedTags": "[String]",
        "minimumTagRank": "Int",
    }

    if key == "sort":
        sort_map = {
            "Media": "[MediaSort]",
            "Character": "[CharacterSort]",
            "Staff": "[StaffSort]",
            "Studio": "[StudioSort]",
        }
        return sort_map.get(entity_type, "[MediaSort]")

    if key in known:
        return known[key]

    # Fallback inference from Python type
    if isinstance(value, bool):
        return "Boolean"
    if isinstance(value, int):
        return "Int"
    if isinstance(value, float):
        return "Float"
    if isinstance(value, str):
        return "String"
    if isinstance(value, list):
        if value and isinstance(value[0], int):
            return "[Int]"
        if value and isinstance(value[0], str):
            return "[String]"
        return "[String]"
    return "String"


def _root_to_collection(root_field):
    """Convert a root entity type to its paginated collection name.

    Media -> media, Character -> characters, Staff -> staff, Studio -> studios
    """
    mapping = {
        "Media": "media",
        "Character": "characters",
        "Staff": "staff",
        "Studio": "studios",
    }
    return mapping.get(root_field, root_field.lower())
