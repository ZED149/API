

# importing some important libraries
import requests
from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")

CLIENT_SECRET_KEY = os.getenv("CLIENT_SECRET_KEY")

GITHUB_TOKEN_URL = f"https://github.com/login/oauth/access_token"

BASE_URL = "https://api.github.com"

app = Flask(__name__)

@app.route("/")
def home():
    return f"<a href='https://github.com/login/oauth/authorize?client_id={CLIENT_ID}'> Login with Github"


@app.route("/authorize")
def authorize():
    code = request.args.get('code')
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET_KEY,
        "code": code
    }
    headers = {
        "Accept": "application/json"
    }
    response = requests.post(GITHUB_TOKEN_URL, params=payload, headers=headers)
    access_token = response.json()['access_token']

    headers = {
        "Authorization": f"token {access_token}"
    }

    response = requests.get(BASE_URL + "/user/repos", headers=headers)
    json_format = response.json()
    list_of_repos = []
    for repo in json_format:
        list_of_repos.append(repo['name'])

    print(list_of_repos)

    return "<br>".join(list_of_repos)     


app.run(debug=True)
