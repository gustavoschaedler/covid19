import flask
from flask import jsonify, request, render_template
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


if __name__ == "main":
    app.run()
