

# importing some important libraries
import requests
from flask import Flask, request
from dotenv import load_dotenv
import os

# loading our enviornmental variables into our scope
load_dotenv()

# client_id
CLIENT_ID = os.getenv("CLIENT_ID")

# client_Secret_key
CLIENT_SECRET_KEY = os.getenv("CLIENT_SECRET_KEY")

# github_token_url
GITHUB_TOKEN_URL = f"https://github.com/login/oauth/access_token"

# base_url
BASE_URL = "https://api.github.com"

# initializing our app varibale for the Flask
app = Flask(__name__)

# Routes
# Homepage route
@app.route("/")
def home():
    return f"<a href='https://github.com/login/oauth/authorize?client_id={CLIENT_ID}'> Login with Github"


# Authorize route
@app.route("/authorize")
def authorize():
    # code that we get after client authorize our app
    code = request.args.get('code')
    # payload to send along with the request
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET_KEY,
        "code": code
    }
    # manipulating headers to get our response in Json form
    headers = {
        "Accept": "application/json"
    }
    # making request to the server
    response = requests.post(GITHUB_TOKEN_URL, params=payload, headers=headers)
    # storing access token of the user
    access_token = response.json()['access_token']
    # storing user's access token into our header file
    headers["Authorization"] = f"token {access_token}"
    # making request to the server
    response = requests.get(BASE_URL + "/user/repos", headers=headers)
    # storing our response generated into JSON form
    json_format = response.json()
    # list to store all repo's
    list_of_repos = []
    for repo in json_format:
        list_of_repos.append(repo['name'])

    # Return
    return "<br>".join(list_of_repos)     


# running our app
app.run(debug=True)
