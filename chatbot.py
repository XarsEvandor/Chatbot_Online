from flask import Flask, request
import os
import core.Regulator

app = Flask(__name__)

@app.route('/')
def index():
    # Test message
    return "<h1>You shouldn't be here.</h1>"

@app.route('/getqry/', methods=['GET'])
def respond():
    # Retrieve the query from the url parameter /getqry/?query=
    query = request.args.get("query", None)
    # # For debugging
    # print(f"Received: {query}")

    response = {}
    
    if not os.path.exists('config.json'):
        response["ERROR"] = "Server error: no config.json found."
        exit(0)

    if not os.path.exists('tags.json'):
        response["ERROR"] = "Server error: no tags.json found."
        exit(0)

    # Check if the user sent a query at all
    if not query:
        response["ERROR"] = "No query found. Please send a query."
    # Check if the user entered a number
    elif str(query).isdigit():
        response["ERROR"] = "The query can't be numeric. Please send a string."
    else:
        response["MESSAGE"] = core.Regulator.regulate(query)

    # Return the response in json format
    return response

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)