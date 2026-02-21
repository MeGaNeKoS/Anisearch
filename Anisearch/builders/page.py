"""PageBuilder — wraps any entity builder in Page { pageInfo { ... } }."""


class PageBuilder:
    """Created by BaseBuilder.page(). Delegates compile/execute to the wrapped builder."""

    def __init__(self, builder, page=1, per_page=10):
        self._builder = builder
        self._builder._page_args = {"page": page, "perPage": per_page}

    def execute(self, **kwargs):
        return self._builder.execute(**kwargs)

    async def execute_async(self, **kwargs):
        return await self._builder.execute_async(**kwargs)
