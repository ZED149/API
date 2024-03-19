import json

# this is the main for currency convertor api

import requests
from flask import Flask, request, render_template
from bs4 import BeautifulSoup

# initializing our app variable
app = Flask(__name__)

# url for home page
@app.route("/")
def homepage():
    return render_template("homepage.html")

# api
@app.route("/api/currency/<from_currency>/<to_currency>/<amount>")
def api_currency(from_currency, to_currency, amount):
    """
    Converts one currency to another for the specified amount
    and returns in JSON format.
    :param from_currency:
    :param to_currency:
    :param amount:
    :return:
    """

    # constructing url
    url = (f"https://www.x-rates.com/calculator/?from={from_currency}"
           f"&to={to_currency}"
           f"&amount={amount}")

    # making a request to the server
    response = requests.get(url)

    # extracting from page
    # creating soup
    soup = BeautifulSoup(response.text, "html.parser")
    # extracting converted amount
    rates = soup.find(class_="ccOutputRslt").getText().split(" ")[0]

    # creating dictionary
    dictionary = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": float(amount),
        "rates": round(float(rates.replace(",", "")))       # converting rates to float and rounding it up and also,
        # removing any comma character from its string representation
    }

    # return thi json dumped dictionary to the webpage
    return json.dumps(dictionary)


# running our app
app.run(debug=True)
