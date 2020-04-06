import flask
from flask import request, jsonify, request, render_template
import requests
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def get_totals(data_cases):

    total = {
        'total_confirmed': sum(item['confirmed'] for item in data_cases['data']),
        'total_deaths': sum(item['deaths'] for item in data_cases['data']),
        'total_recovered': sum(item['recovered'] for item in data_cases['data'])
    }
    return total


@app.route('/', methods=['GET'])
def home():
    params = {
        'x': '1',
    }
    data = requests.get(
        'https://covid19-brazil-api.now.sh/api/report/v1/countries',
        params=params
    )
    result = json.loads(data.text)

    total = get_totals(result)

    return render_template('countries.html', countries=result, total=total)
    # return json.loads(data.text)


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


if __name__ == "main":
    app.run()
