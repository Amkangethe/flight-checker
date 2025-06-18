#imports
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

api_key = os.getenv("RAPIDAPI_KEY") # Fetch the API key from environment variables

# Function to search for airports based on city, country, or IATA code
def search_airports():

    url = "https://aerodatabox.p.rapidapi.com/airports/search/term" # API endpoint 

    # request headers
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }

    # Prompt user for search term
    try:
        query = input("Enter search term (city, country, or IATA code): ")
        if len(query) < 3:
            print("\nSearch term must be at least 3 characters long. Please try again!\n")
            return
        params = {"q": query, "limit": 10}
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return
    
    print(response.json())


    # If the response is not successful, print an error message
    if(response.json()["count"] == 0):
        print("No airports were found for your search term.")
        print("Would u like to try again? (y/n)")
        try:
            retry = input().strip().lower()
            if retry == 'y':
                search_airports()
            else:
                print("Exiting the search.")
                return
        except Exception as e:
            print(f"An error occurred: {e}")
    # If the response is successful, process the data
    else:
        print(f"Found {response.json()['count']} airports for '{query}':")
        count = 1;

        airports = response.json()["items"]
        airports_sorted = sorted(airports, key=lambda x: x["name"].lower()) # Sort by airport name (case-insensitive)

        # Display the airports
        count = 1
        for airport in airports_sorted:
            print(f"{count}. {airport['iata']}/{airport['icao']} - {airport['name']}, {airport['countryCode']}")
            count += 1

    # Ask the user if they want to search again
    print("\nWould you like to search again? (y/n)")
    try:
        retry = input().strip().lower()
        if retry == 'y':
            search_airports()
        else:
            print("Exiting the search.") 
    except Exception as e:
        print(f"An error occurred: {e}")   




if __name__ == "__main__":
    # Greetings message
    print("\n\nHello, welcome to flight-checker by @amkangethe!")
    print("These are your options: ")

    while True:
        print("1. Search for Airports")
        print("2. Search for Airports")
        print("3. Search for Airports")
        print("4. Search for Airports")
        
        try:
            userInput = int(input("Your Choice: "))
        except Exception as e:
            print("\nYou did not enter a valid number. Please try again\n")
            continue

        if userInput == 1:
            search_airports()

