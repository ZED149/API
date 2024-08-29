

import requests

# URLS's
url = "https://eopsjx3tfnf06vf.m.pipedream.net"
response_url = "https://reqres.in"
# HEADERS
# Are the extra information that goes along(are sent alongside) with the request
# we can also pass a token inside a header for authentication purposes
# a server will take your token and will verify your identity
headers = {
    "my-token": "jasd 11726w9ashdbabd12j1vhvsady9s"
}

# REQUEST METHOD'S
# FIVE MOST POPULAR REQUEST METHODS
# 1. GET        ----->      to retrieve some information
# 2. POST       ----->      to add some new information
# 3. DELETE     ----->      to delete information on the server
# 4. PUT        ----->      to modify/update information on the server
# 5. PATCH      ----->      does the samethins as PUT in a lot of cases

# PAYLOAD 
# we can also use params to send our payload instead of writing each URL parameter seperately
# we can send them in a payload
payload = {"first_name" : "salman",
           "last_name": "ahmad",
           "age": 26,
           "professional_life": {
               "status": "failure", 
               "code": 0
           }}


# JSON DATA 
# to convert it into a JSON object
json_payload = {
    "name": "ZED",
    "job": "Software Engineer"
}

# FORM DATA
form_data = {
    "name": "Salman Ahmad",
    "job": "Machine Learning Engineer"
}


# SENDING FILES
# we can send files in a request but this is very rare
file = {
    "file_1": ("filename", "open()", "type of image")
}

files = {
    "file": ("cat.jpeg", open("cat.jpeg", "rb"), "image/jpeg")
}

# RECEIVING FILES
# we can receive files using request library
receiving_filename = "https://httpbin.org/image/jpeg"


response = requests.get(receiving_filename)
with open("r_filename.jpeg", "wb") as fd:
    for chunk in response.iter_content(chunk_size=500):
        fd.write(chunk)


# EXCEPTIONS
# we can catch and handle exceptions while using request library
# it can be a conn error or it can be from server/client

# Connection error
fake_url = "https://sad2wdsdasdfasdfdas23e3w"
try:
    response = requests.get(fake_url)
except requests.exceptions.ConnectionError:
    print("Failed to connect")


# Server/Client Error
originated_error = "https://httpbin.org/status/200"
response = requests.get(originated_error)
try:
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("Error in status code")


# TIMEOUTS
# we can use timeouts to safely disconnect from a server if its take too long to generate a response
timeout_url = "https://httpbin.org/delay/1"
try:
    response = requests.get(timeout_url, timeout=0.0001)
except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as error:
    match error:
        case requests.exceptions.ConnectTimeout:
            print(f"[ERROR] -> {error}: Request connect timed out while connecting to Httpbin.org")
        case requests.exceptions.ReadTimeout:
            print(f"[ERRor] -> {error}: Request read timeo out while connecting to Httpbin.org")
    print("error here")
    # print(error)
else:
    print("Request success")



# BASIC AUTHENTICATION
# we can use basic authentication in our apps using request library
from requests.auth import HTTPBasicAuth
auth_url = "https://httpbin.org/basic-auth/user/passwd"
response = requests.get(auth_url, auth=HTTPBasicAuth("salman", "123"))
try:
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("Cannot connect to server. Invalid username or passoword")

# now checking with the correct credentials
response = requests.get(auth_url, auth=HTTPBasicAuth("user", "passwd"))
try:
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("Error while authticating")
else:
    print('Sucessfully authenticated with the server')
        






