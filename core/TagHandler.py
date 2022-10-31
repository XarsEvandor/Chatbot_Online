import json

import core.Lemmatizer
import core.Tokenizer


class TagHandler:
    # static variables
    tag_dictionary = {}

    # Read the tags from tags.json
    with open("tags.json", "r") as tag_file:
        data = json.load(tag_file)
        tag_list = data['tags']

    # Read the delimiters from config.json
    with open("config.json", "r") as conf_file:
        data = json.load(conf_file)
        delimiters = data['init_params']['delimiters']

    # static method. scored_tags must be a list where sorted_tags[x]= [tag, score]
    @staticmethod
    def sort(scored_tags: list):
        sorted_tags = sorted(scored_tags, key=lambda x: x[1], reverse=True)
        return sorted_tags

    @staticmethod
    def tag_processing(tag_list: list, delimiters: list):
        for tag in tag_list:
            tag_tokenizer = core.Tokenizer.Tokenizer(tag, delimiters)
            tag_lemmatizer = core.Lemmatizer.Lemmatizer(tag_tokenizer.tokenize())
            tag_tokens = tag_lemmatizer.lemmatize()
            TagHandler.tag_dictionary[tag] = tag_tokens



