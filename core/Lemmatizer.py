import nltk
from nltk.stem import PorterStemmer

class Lemmatizer:
    def __init__(self, tokens: list):
        self.tokens = tokens

    def lemmatize(self) -> list:
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()

        # We get the treebank_tag, convert it to 'part of speech' and lemmatize
        # nltk.pos_tag() accepts and returns lists.
        # Lemmatizing: https://www.geeksforgeeks.org/python-lemmatization-with-nltk/?ref=lbp
        # To be more flexible we enumerate through the tokens and manipulate each one as a one item list.
        for index, token in enumerate(self.tokens):
            token_tag = nltk.pos_tag([token])

            # The token is stemmed to minimize mismatching.
            # Stemming: https://www.geeksforgeeks.org/python-stemming-words-with-nltk/
            stemmed_token = stemmer.stem(token)
            token = lemmatizer.lemmatize(stemmed_token, self.get_wordnet_pos(token_tag[0][1]))
            self.tokens[index] = token

        return self.tokens

    # Convert treebank tag to 'part of speech' (adjective, verb etc.).
    # This information is used to search for more accurate lemmas.
    @staticmethod
    def get_wordnet_pos(treebank_tag):
        from nltk.corpus import wordnet

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
