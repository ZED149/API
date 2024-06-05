

import requests

BASE = "http://127.0.0.1:5000/"
response = requests.put(f"{BASE}video/1", {"likes": 20,
                                "name": "Despacito feat. Bohemia Pakistan",
                                "views": 460127218})
print(response.json())

response = requests.put(f"{BASE}video/2", {"likes": 2000,
                                "views": 12389172398,
                                "name": "Taylor Swift Blank Space"})
print({'sc': response.status_code,
       'message': response.json()})

response = requests.put(f"{BASE}video/31", {"likes": 2123,
                                "views": 28312984,
                                "name": "NFAK Tumhy Dillagi Bhul Jani Paregi by OSA Studios"})

print(response)

response = requests.get(f"{BASE}video/1")
print(response.json())
response = requests.get(f"{BASE}video/2")
print(response.json())

response = requests.get(f"{BASE}video/32")
print(response.status_code)

print("Checking update command API")
response = requests.patch(f"{BASE}video/1", {'likes': 21})
print(response.json())

print("Checking delete command API")
response = requests.delete(f"{BASE}video/1")
print(response.status_code)
