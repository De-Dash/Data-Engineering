import asyncio
import aiohttp
from typing import List, Dict
import time


def fetch(*, urls:List[str]) -> List[Dict]:
    """
    Fetches request responses from a list of URLs asynchronously by calling
    _fetch_loop.

    Args: 
        urls: list of urls

    Returns: 
        A list of dicts of url responses
    """
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(_fetch_loop(urls=urls))
    return responses

async def _fetch_loop(*, urls:List[str]) -> List[Dict]:
    """
    Calls _fetch_one using a list of urls asynchronously using up to 100 
    simultaneous calls

    Args: 
        urls: list of urls

    Returns: 
        A list of dicts of url responses
    """
    tasks = []
    
    # We use Python built-in asyncio Semaphore to limit to max 100
    # concurrent actions
    sema = asyncio.BoundedSemaphore(value=100)
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(_fetch_one(session=session,
                                    url=url,
                                    sema=sema))
        # Asynchronously process the tasks without looping if it runs into
        # exceptions. Exceptions are excluded from the responses.
        responses = await asyncio.gather(*tasks,
                                         loop=None,
                                         return_exceptions=False)
    return responses

async def _fetch_one(*, session, url:str, sema) -> Dict:
    """
    Makes a GET request from an URL/API asynchronously to allow
    multiple URL requests to be sent at the same time.

    Args:
        session: aiohttp.ClientSession, a session of aiohttp
        url: The url to fetch responses from
        sema: asyncio semaphore limit

    Returns:
        A dict of the response from the GET request to the input url
    """
    # Using session.requests('GET', url) instead of session.get(url)
    # as it is more readable for my small brain. Both does the same thing
    async with sema, session.request('GET', url) as response:
        return await response.json()


if __name__ == '__main__':
    start_time = time.time()
    urls=['https://hacker-news.firebaseio.com/v0/item/8863.json']
    responses = fetch(urls=urls)
    print(f"{time.time() - start_time}s")
    print(responses)