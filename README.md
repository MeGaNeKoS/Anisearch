# Anisearch
Anilist API module for python. you only need to copy the Anilist folder to your own script.

### Executing program

* How to run the program
* Import module

```python
from Anisearch import Anilist
instance = Anilist()
```

From there you can get information from Anilist using their new GraphQL API.
To get data on a known ID.
```python
instance.get.anime(13601) # Return data on PSYCHO-PASS 
instance.get.manga(64127) # Return data on Mahouka Koukou no Rettousei
instance.get.staff(113803) # Return data on Kantoku
instance.get.studio(7) # Return data on J.C. Staff
```

Searching is also making a return.
```python
instance.search.anime("Sword") # Anime search results for Sword.
instance.search.manga("Sword") # Manga search results for Sword.
instance.search.character("Tsutsukakushi") # Character search results for Tsutsukakushi.
instance.search.staff("Kantoku") # Staff search results for Kantoku.
instance.search.studio("J.C. Staff") # Studio search result for J.C. Staff.
```
A note about the searching and getting:
```python
search(term, page = 1, perpage = 10, query_string=None)
get(item_id, query_string=None)
```
Pagination is done automatically in the API. By default you'll get 10 results per page. 
If you want more, just change the perpage value. pageInfo is always the first result in the returned data.
Pages start at 1 and if you want another page, just replace page with the next number. 
query_string is to set what info you want to displayed.
