import unittest
import asyncio
import aiohttp
from api.utils import _fetch_one, fetch


class TestFetchOne(unittest.TestCase):

    async def setUp(self):
        self.sema = asyncio.BoundedSemaphore(value=100)
        self.url = "https://hacker-news.firebaseio.com/v0/item/8863.json"
        tasks = []
        async with aiohttp.ClientSession() as session:
            tasks.append(_fetch_one(session=session,
                                    url=self.url,
                                    sema=self.sema))
        self.responses = await asyncio.gather(*tasks,
                                              loop=None,
                                              return_exceptions=False)
        

    def test_fetch_one(self):
        """
        Using https://hacker-news.firebaseio.com/v0/item/8863.json as a test case
        """
        self.assertEqual(len(self.responses), 1)
        

# class TestFetch(unittest.TestCase):

#     def test_fetch(self):
#         """
#         Using https://hacker-news.firebaseio.com/v0/item/8863.json as a test case
#         """
#         ids = [9224,8917,8952,8884,8887,8869,8958,8940,8908,9005,8873,
#                9671,9067,9055,8865,8881,8872,8955,10403,8903,8928,9125,
#                8998,8901,8902,8907,8894,8870,8878,8980,8934,8943,8876]

if __name__ == '__main__':
    unittest.main()
