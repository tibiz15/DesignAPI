
import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = "="
RSA_API_KEY = ""

app = Flask(__name__)

def get_weather(date, location):
    url_base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    
    url_date = dt.date.today()
    if date:
        url_date = date
        
    url_location = "Kyiv"
    if location:
        url_location = location
    
    url = f"{url_base_url}/{url_location}/{url_date}/{url_date}?unitGroup=metric&key={RSA_API_KEY}"
    
    response = requests.request("GET", url)
    return json.loads(response.text)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def home_page():
    return "<p><h2>KMA HOMEWORK 1: Python Saas.</h2></p>"


@app.route(
    "/api/v1/weather",
    methods=["POST"],
)
def weather_endpoint():
    json_data = request.get_json()
    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")
    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    location = request.args.get('location')
    date = request.args.get('date')
    weather = get_weather(date, location)
    del weather["days"][0]["hours"]
    return weather


