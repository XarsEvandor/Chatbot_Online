import json

from core import GoogleAPIHandler
from core.Lemmatizer import Lemmatizer
from core.Scorer import Scorer
from core.TagHandler import TagHandler
from core.Tokenizer import Tokenizer
from datetime import datetime


currentMonth = datetime.now().month


def init_regulator():
    with open("config.json", "r+") as regulator_file:
        data = json.load(regulator_file)
        data['API_regulator']['month'] = currentMonth
        data['API_regulator']['API_usage_count'] = 0
        regulator_file.seek(0)
        json.dump(data, regulator_file, indent=4)
        regulator_file.truncate()


def regulate(query_input):
    with open("config.json", "r") as regulator_file:
        data = json.load(regulator_file)
        recorded_month = data['API_regulator']['month']
        recorded_count = data['API_regulator']['API_usage_count']
        use_api = data['init_params']['useAPI']
        delimiters = data['init_params']['delimiters']
        displayed_tags_num = data['init_params']['displayed_tags_num']

    if currentMonth > recorded_month:
        recorded_count = 0
        init_regulator()

    # Ensure tags are processed
    TagHandler.tag_processing(TagHandler.tag_list, delimiters)

    # Use the API only until 4900 uses and only if the use_api variable is true
    # Query pipeline: tokenize -> lemmatize -> score -> sort
    if recorded_count > 4900 or not use_api:
        tokenize_query = Tokenizer(query_input, delimiters)
        lemmatize_query = Lemmatizer(tokenize_query.tokenize())
        query_list = lemmatize_query.lemmatize()

        scorer = Scorer(TagHandler.tag_dictionary, query_list)
        scored_tags = scorer.score()
        sorted_tags = TagHandler.sort(scored_tags)

        answer_json = json.dumps(sorted_tags[:displayed_tags_num])
        # Check if the top tag has a score 0. This tells us we have no results.
        if sorted_tags[0][1] == 0:
            print("\nNo results. Please try something like: 'I want to learn about the war in Ukraine'\n")
            return 0
        else:
            # print("Top " + str(displayed_tags_num) + " tags: \n")
            # print(answer_json)

            return answer_json
    else:
        query_list = GoogleAPIHandler.analyze_syntax(query_input, delimiters)

        recorded_count += 1

        # If we use the API, we need to make sure the usage count is updated in the config.json
        with open("config.json", "r+") as regulator_file:
            data = json.load(regulator_file)
            data['API_regulator']['month'] = currentMonth
            data['API_regulator']['API_usage_count'] = recorded_count
            regulator_file.seek(0)
            json.dump(data, regulator_file, indent=4)
            regulator_file.truncate()


        scorer = Scorer(TagHandler.tag_dictionary, query_list)
        scored_tags = scorer.score()
        sorted_tags = TagHandler.sort(scored_tags)

        answer_json = json.dumps(sorted_tags[:displayed_tags_num])
        if sorted_tags[0][1] == 0:
            print("\nNo results. Please try something like: 'I want to learn about the war in Ukraine'\n")
            return 0
        else:
            # print("Top " + str(displayed_tags_num) + " tags: \n")
            # print(answer_json)

            return answer_json
