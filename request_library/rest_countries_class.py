

# This file contains the class for the Rest Countries project

# including some important libraries
import requests


class RestCountries:
    # Private data members
    __BASE_URL: str = "https://restcountries.com/v3.1/"
    __country:  str = ""
    __data = None


    # Contructor
    def __init__(self, country: str) -> None:
        # initialing private data members
        self.__country = country

        # making request
        self.__make_request()

        
    # Member Functions

    # make_request
    def __make_request(self) -> None:
        # generating payload
        payload = {
            "fields": ["languages", "population", "timezones"],
            "fullText": "True"
        }
        # making request to the server with the country
        response = requests.get(self.__BASE_URL + f"name/{self.__country}", params=payload)
        # storing response in JSON format
        self.__data = response.json()


    # extract_language
    def extract_language(self):
        a = 1
        return self.__data[0]["languages"]
    

    # extract_timezones
    def extract_timezones(self):
        return self.__data[0]["timezones"]


    # extract_all
    def extract_population(self):
        return self.__data[0]["population"]
    

    # print_data
    def print_data(self) -> None:
        print(self.__data)