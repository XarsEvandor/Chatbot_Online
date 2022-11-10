class Tokenizer:
    import nltk
    from nltk.corpus import stopwords
    nltk.data.append('./nltk_data/')
    
    stopwords = stopwords.words('english')

    def __init__(self, query: str, delimiters: list):
        self.query = query
        self.delimiters = delimiters

    # Split on space
    def tokenize(self) -> list:
        tokens = []
        tokens = self.query.split()

        # Split on all delimiters specified in config.json
        for delimiter in self.delimiters:
            for token in tokens:
                if delimiter in token:
                    if not token == delimiter:
                        tokens.extend(token.split(delimiter))
                    tokens.remove(token)

        # Turn all tokens lowercase to avoid case missmatch
        for index, token in enumerate(tokens):
            tokens[index] = token.lower()

        # Remove stopwords (useless words like I, they, to etc.)
        for token in tokens:
            if token in self.stopwords:
                tokens.remove(token)

        return tokens


