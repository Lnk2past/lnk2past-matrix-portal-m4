from datetime import datetime
import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def data():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    url = 'https://api.weather.gov/gridpoints/PHI/40,75/forecast'
    forecast = requests.get(url)
    temp = forecast.json()['properties']['periods'][0]['temperature']
    return {
        'data': {
            'hour': hour,
            'minute': minute,
            'temp': temp,
        }
    }
