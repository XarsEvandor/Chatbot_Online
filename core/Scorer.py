
class Scorer:
    def __init__(self, tag_dict: dict, query_list: list):
        self.tag_dict = tag_dict
        self.query_list = query_list

    # For every key in the tag dictionary, we iterate through the value
    # (list of lemmatized tokens corresponding to the tag) and we search for each words in our query list
    # (list of lemmatized tokens corresponding to the query). If we find a match we increase the score of the tag.
    # The final score is the number of matches divided by the size of the tag plus a constant to ensure long tags get
    # higher scores that short tags.
    def score(self) -> list:
        scored_tags = []
        for tag in self.tag_dict:
            score = 0
            for word in self.query_list:
                if word in self.tag_dict[tag]:
                    score += 1

            score = round(score / (len(self.tag_dict[tag]) + 1), 2)
            scored_tags.append([tag, score])

        return scored_tags


