import time
import string
import re
import nltk
import html
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from typing import List, Dict
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
        Finds the WordNet tag for the word

        https://simonhessner.de/lemmatize-whole-sentences-with-python-and-nltks-wordnetlemmatizer/

        Args: 
            nltk_tag: tokenized words and tag pair

        Returns: 
            WordNet tag       
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

    def words(self) -> Dict:
        """
        Word frequency counts for all the text in user's comments, asks, jobs, and pools. Does not inclue
        story titles. All the words will be lemmatized using NLTK's WordNet.

        Args: 
        
        Returns: 
            Python dictionary of word and word count.
        """
        # only take items with a text field
        words = []
        for post in self.submitted:
            if 'text' in post:
                words.append(post['text'])
                
        words = ' '.join(words).replace('\n', ' ').lower()
        # removes urls
        words = re.sub(r'http\S+', '', words)
        # removes <> and content in betweens
        words = re.sub('<.*?>', ' ', words)
        # unescapes html entities, e.g., &#x2F into /
        words = html.unescape(words)
        
        words = words.translate(str.maketrans(' ', ' ', string.punctuation))
        tagged = nltk.pos_tag(nltk.tokenize.word_tokenize(words))
        tagged = map(lambda x: (x[0], self._nltk2wn_tag(x[1])), tagged)
        
        # Process individual (word, tag) tuples
        words_lemma = []
        for word, tag in tagged:
            if tag is None:
                words_lemma.append(word)
            else:
                words_lemma.append(self.lemmatizer.lemmatize(word, tag))
        words = [word for word in words_lemma if word not in stopwords.words('english')]
        words = nltk.FreqDist(words)
        words = dict(words)
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