#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask import send_from_directory
from flask_api import status
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

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

# test input
@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        firstName = request.form['fname']
        lastName = request.form['lname']

        if firstName == 'Miles' and lastName == 'Morales':
            return redirect('/swagger'), status.HTTP_200_OK
        else:
            return redirect('/login'), status.HTTP_401_UNAUTHORIZED

    return render_template("login.html"), status.HTTP_200_OK


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
