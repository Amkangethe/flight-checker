#imports
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

api_key = os.getenv("RAPIDAPI_KEY") # Fetch the API key from environment variables

# Function to search for airports based on city, IATA code, or ICAO code
def search_airports():

    url = "https://aerodatabox.p.rapidapi.com/airports/search/term" # API endpoint 

    # request headers
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }

    # Prompt user for search term
    try:
        query = input("Enter search term (city, or IATA code, or ICAO code): ")
        if len(query) < 3:
            print("\nSearch term must be at least 3 characters long. Please try again!\n")
            return
        params = {"q": query, "limit": 10}
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return
    

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
   
def view_airport_details():
    # Loop to allow repeated searches until the user chooses to exit
    while True:
        # Prompt user for airport code
        airport = input("\nEnter the IATA code or ICAO code of the airport: ").strip().upper()
        if len(airport) < 3:
            print("\nAirport code must be at least 3 characters long. Please try again!\n")
            continue

        # Prepare both IATA and ICAO endpoints for lookup
        endpoints = [
            f"https://aerodatabox.p.rapidapi.com/airports/iata/{airport}",
            f"https://aerodatabox.p.rapidapi.com/airports/icao/{airport}"
        ]
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
        }
        found = False
        # Try each endpoint until a valid airport is found
        for url in endpoints:
            try:
                response = requests.get(url, headers=headers)
                # Skip if response is not OK or empty
                if response.status_code != 200 or not response.text.strip():
                    continue
                data = response.json()
                # If the response contains a name or fullName, it's valid
                if data.get("name") or data.get("fullName"):
                    print(f"\nAirport Details:")
                    print(f"Name: {data.get('fullName', data.get('name', 'N/A'))}")
                    print(f"IATA: {data.get('iata', 'N/A')}")
                    print(f"ICAO: {data.get('icao', 'N/A')}")
                    country = data.get('country', {})
                    print(f"Country: {country.get('name', country.get('code', 'N/A'))}")
                    print(f"City: {data.get('municipalityName', 'N/A')}")
                    print(f"Website: {data.get('urls', {}).get('webSite', 'N/A')}")                   
                    found = True
                    break  # Stop after finding the first valid result
            except Exception as e:
                print(f"Error fetching details: {e}")
                continue
        # If no valid airport was found, notify the user
        if not found:
            print("\nCould not fetch airport details. Please check the code and try again.")
        # Ask if the user wants to search again
        retry = input("Would you like to search for another airport? (y/n): ").strip().lower()
        if retry != 'y':
            print("Exiting the airport details view.")
            break

        



if __name__ == "__main__":
    # Greetings message
    print("\nHello, welcome to flight-checker by @amkangethe!")
    print("These are your options:")

    while True:
        print("1. Search for Airports")
        print("2. View Airport Details")
        print("3. Search for Flights by Flight Number")
        print("4. Search for Flights by Route")
        print("5. View Arrivals/Departures at an Airport")
        print("6. Check Flight Status")
        print("7. Exit")
        
        try:
            userInput = int(input("Your Choice: "))
        except Exception as e:
            print("\nYou did not enter a valid number. Please try again")
            continue

        if userInput == 1:
            search_airports()
            print()  # single blank line after function returns
        elif userInput == 2:
            view_airport_details()
            print()
        # ...existing code for other options...
        elif userInput == 7:
            print("Goodbye!")
            break



