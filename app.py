from flask import Flask, render_template, request
from weather import main as get_weather
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

@app.route('/')
def menu():
    return render_template('main.html')

@app.route('/weather', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        data = get_weather(city, state, country, API_KEY)

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
