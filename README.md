# Anisearch

Declarative GraphQL query builder for the [AniList](https://anilist.co) API.

## Installation

```bash
pip install Anisearch

# For async support
pip install Anisearch[async]
```

## Quick Start

```python
from Anisearch import Anilist

anilist = Anilist()

# Get anime by ID
result = anilist.media(id=13601, type="ANIME") \
    .id().title("romaji", "english").episodes().status() \
    .execute()
print(result)
```

## Builder API

Every query starts from an `Anilist` instance. Call `.media()`, `.character()`, `.staff()`, or `.studio()` to get a builder, chain the fields you want, then `.execute()`.

### Media

```python
result = anilist.media(search="Psycho-Pass", type="ANIME") \
    .id().title("romaji", "english").genres().episodes().status() \
    .execute()
```

### Character

```python
result = anilist.character(search="Saber") \
    .id().name().image() \
    .execute()
```

### Staff

```python
result = anilist.staff(id=113803) \
    .id().name().image() \
    .execute()
```

### Studio

```python
result = anilist.studio(search="J.C. Staff") \
    .id().name() \
    .execute()
```

## Pagination

Wrap any query with `.paginate()` to get paginated results:

```python
result = anilist.media(search="Sword", type="ANIME") \
    .id().title("romaji") \
    .paginate(page=1, per_page=10) \
    .execute()
```

## Nested Fields

Some fields accept sub-field selections:

```python
result = anilist.media(id=13601) \
    .title("romaji", "english", "native") \
    .cover_image("large", "medium") \
    .characters(sort="FAVOURITES_DESC", per_page=5)(lambda c: c.id().name().image()) \
    .execute()
```

## Fragments

Reuse field selections across queries with `Fragment`:

```python
from Anisearch import Fragment

basic_info = Fragment.media(lambda m: m.id().title("romaji", "english").genres())

result = anilist.media(id=13601).use(basic_info).episodes().execute()
```

## Retry Configuration

Customize retry behavior with `RetryStrategy`:

```python
from Anisearch import RetryStrategy

retry = RetryStrategy(
    max_retries=5,
    on_rate_limit="wait",       # "wait" or "raise"
    on_server_error="backoff",  # "backoff" or "raise"
    max_wait=60,
)
anilist = Anilist(retry=retry)
```

## Raw Query

For queries the builder doesn't cover, use `raw_query`:

```python
query = """
query ($id: Int) {
  Media(id: $id) {
    id
    title { romaji }
  }
}
"""
result = anilist.raw_query({"id": 13601}, query)
```

## Async Usage

All builders support async execution (requires `aiohttp`):

```python
import asyncio
from Anisearch import Anilist

async def main():
    anilist = Anilist()
    result = await anilist.media(id=13601) \
        .id().title("romaji") \
        .execute_async()
    print(result)

asyncio.run(main())
```

## License

MIT
