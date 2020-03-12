import time
from typing import List, Dict
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from api.utils import fetch


class User:

    def __init__(self, username:str):
        self.username = username
        self.profile = self._get_profile(username)
        self.submitted = self._get_submitted()
        self.lemmatizer = WordNetLemmatizer()

    def _get_profile(self, username:str) -> Dict:
        query = [f'https://hacker-news.firebaseio.com/v0/user/{username}.json']
        profile = fetch(urls=query)[0]
        return profile

    def _get_submitted(self) -> List[Dict]:
        ids = self.profile['submitted']
        item_urls = [f"https://hacker-news.firebaseio.com/v0/item/{id}.json" for id in ids]
        submitted = fetch(urls=item_urls)
        return submitted

    def _nltk2wn_tag(self, nltk_tag):
        """
        https://simonhessner.de/lemmatize-whole-sentences-with-python-and-nltks-wordnetlemmatizer/
        """
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:					
            return None

    def words(self) -> List[str]:
        words = ' '.join([submitted['text'].lower() for submitted in self.submitted]).replace('\n', ' ')
        words = self.lemmatizer.lemmatize(words)
        words = [word for word in words if word not in stopwords.words('english')]
        # words = nltk.pos_tag(nltk.tokenize.word_tokenize(words))
        # words = map(lambda x: (x[0], self._nltk2wn_tag(x[1])), words)
        words = nltk.FreqDist(words)
        return words

    def trending(self) -> List[str]:
        raise NotImplementedError

    def stats(self) -> List[str]:
        raise NotImplementedError


if __name__ == '__main__':
    start_time = time.time()
    user = User('jl')  # user with 846 posts
    # user = User('li')    # user with 3 posts
    print(f"{time.time() - start_time}s")