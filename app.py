import flask
from flask import jsonify, request, render_template
import requests
import json
import crawler

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
    data = requests.get(
        'https://covid19-brazil-api.now.sh/api/report/v1/countries')
    result = json.loads(data.text)
    total = get_totals(result)

    return render_template('countries.html', countries=result, total=total)


@app.route('/data', methods=['GET'])
def all_data():
    return jsonify(crawler.all_data)


if __name__ == "main":
    app.run()
