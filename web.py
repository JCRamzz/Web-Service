#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask import send_from_directory
from flask_api import status
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import requests

# API key
apikey = '416c46727662229e0326014748346721'

# Initialize app
app = Flask('app')

# Access-Control-Allow-Origin:
CORS(app)

# Setup swagger blueprint and path
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Web Service"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Say hello
@app.route('/hello', methods=['GET'])
def get():
    return jsonify({'message': 'hello yourself'}), status.HTTP_200_OK

# Grab API key from the header request
def getAPIKEY():
    API_KEY = str(request.headers.get('Appid')).split(" ")[0]
    print(str(request.headers))
    return API_KEY

# Get weather by zipcode
@app.route('/weather/<zipcode>', methods=['GET'])
def get_weather_zipcode(zipcode):

    token = getAPIKEY()
    print(token[0])
    if token[0] is None:
        return jsonify({'message': 'Authorization Needed!'}), status.HTTP_401_UNAUTHORIZED

    if zipcode.isdigit() is False:
        return jsonify({'message': 'Invalid Input!'}), status.HTTP_400_BAD_REQUEST

    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?zip={zipcode}&units=imperial&appid={token}')
    print(response)
    if response.status_code == 200:
        return response.json(), status.HTTP_200_OK
    if response.status_code == 401:
        return response.json(), status.HTTP_401_UNAUTHORIZED

    return status.HTTP_404_NOT_FOUND


# Login landing page
@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']

        if userName == 'Miles' and password == 'Morales':
            return redirect('/swagger'), status.HTTP_200_OK
        else:
            return redirect('/login'), status.HTTP_401_UNAUTHORIZED

    return render_template("login2.html"), status.HTTP_200_OK

# Create account page
@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']

        if password == confirmation:
            return redirect('/login'), status.HTTP_200_OK
        else:
            return redirect('/create'), status.HTTP_400_BAD_REQUEST
    return render_template("createaccount.html"), status.HTTP_200_OK



@app.route('/static/<path:path>')
def send_swagger(path):
    return send_from_directory('static', path)


# Root
@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('get_login')), status.HTTP_200_OK


# Run server
if __name__ == '__main__':
    app.run(debug=True)
