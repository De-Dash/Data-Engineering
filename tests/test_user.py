import sys
import unittest
sys.path.append("..")
from api.user import User


class TestUser(unittest.TestCase):

    def test_user(self):
        """
        Using https://hacker-news.firebaseio.com/v0/user/li.json as a test case, 3 comments
        """
        user = User('li')

        self.assertIsInstance(user.profile, dict)
        self.assertCountEqual(list(user.profile.keys()), ['created', 'delay', 'id', 'karma', 'submitted'])
        self.assertEqual(user.profile['created'], 1299432076)
        self.assertEqual(user.profile['karma'], 2)
        self.assertEqual(len(user.profile['submitted']), 3)
        self.assertCountEqual(user.profile['submitted'], [3741349, 2422834, 2318276])

if __name__ == '__main__':
    unittest.main()
