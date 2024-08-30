

# This file contains the REST Countries API practice work

# importing some important libraries
from rest_countries_class import RestCountries

# we will ask the user about what information he wants
# he can have a look on population, languages, timezones or all three

# prompting the user about his choice
print("What information you want?")
print("1. Population")
print("2. Languages")
print("3. Timezones")

# prompting user for the choice
choice = int(input("Enter the number here: "))
# asking user for the country
country = input("Enter country name you wanna search for: ")

# initializng RC object
rc = RestCountries(country=country)

# performing operations according to user's choice
if choice == 1:
    print(rc.extract_population())
elif choice == 2:
    print(rc.extract_language())
elif choice == 3:
    print(rc.extract_timezones())
else:
    exit(0)