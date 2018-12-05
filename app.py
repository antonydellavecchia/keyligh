import requests
import json
import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def git_hub_counter():
    # parse parameters
    search_term = request.args.get('filter', default='', type = str)
    size = request.args.get('size', default = 10, type = int)
    
    # get last weeks date
    past_week = datetime.date.today() - datetime.timedelta(weeks=1)

    # create request string, uses filter and orders by most starred repos created in last week
    request_url = "https://api.github.com/search/repositories?q={0}+created:>{1}".format(search_term, past_week)

    # Make call to github
    response = requests.get(
        request_url
    )

    # parse data
    json_data = json.loads(response.content)

    # create list of repos
    repos = json_data['items']
    
    # create list of sums
    sums = [ counter(x) for x in json_data['items'] ]

    # returns as JSON determined by size requested
    return jsonify(sums[:size])


# returns number of stars and watchers of repo
def counter(repo_object):
    return repo_object['watchers'] + repo_object['stargazers_count']

    
