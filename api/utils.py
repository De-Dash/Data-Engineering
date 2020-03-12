import asyncio
import aiohttp


async def fetch(session, url):
    """
    Fetches response from an URL/API asynchronously to allow
    multiple URL requests to be sent at the same time.

    Args:
        session: aiohttp.ClientSession, a session of aiohttp
        url: The url to fetch responses from

    Returns:
        Responses from the URL
    """
    async with session.get(url) as response:
        return await response.text()

async def main():
    """
    Main function for testing fetch using asynchronous simultaneous calls

    Args:

    Returns:
    """
    urls = ['https://hacker-news.firebaseio.com/v0/item/8863.json']
    tasks = []
    
    # limit to 100 concurrent actions
    sema = asyncio.BoundedSemaphore(value=100)
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
