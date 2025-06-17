import os
import requests
from dotenv import load_dotenv

# Load API key from .env in current directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
API_KEY = os.getenv("RAPIDAPI_KEY")

from datetime import datetime, timedelta, timezone

start_time = datetime.now(timezone.utc)
end_time = start_time + timedelta(hours=6)

start_str = start_time.strftime("%Y-%m-%dT%H:%M")
end_str = end_time.strftime("%Y-%m-%dT%H:%M")

def get_departures(iata_code):
    url = f"https://aerodatabox.p.rapidapi.com/flights/airports/iata/{iata_code}/{start_str}/{end_str}"


    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }

    params = {
        "direction": "Departure",
        "withLeg": "true",
        "withCancelled": "false",
        "withCodeshared": "true",
        "withCargo": "false",
        "withPrivate": "false"
    }

    print(f"\n[DEBUG] Requesting departures with URL: {url}")
    print(f"[DEBUG] Params: {params}")
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        return

    try:
        data = response.json()
    except Exception as e:
        print(f"❌ Failed to parse JSON: {e}")
        print(response.text)
        return
    flights = data.get("departures", [])

    if not flights:
        print("No flights found for this window.")
        return

    print("🛫 Upcoming Departures:")
    for i, flight in enumerate(flights[:5], 1):
        try:
            flight_number = flight['flight']['number']
            destination = flight['arrival']['airport']['name']
            departure_time = flight['departure']['scheduledTimeLocal']
            print(f"{i}. Flight {flight_number} to {destination} at {departure_time}")
        except KeyError:
            print(f"[DEBUG] Skipping flight due to missing data: {flight}")
            continue


def search_airports_by_city(city_name):
    url = "https://aerodatabox.p.rapidapi.com/airports/search/term"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
    }

    params = {
        "q": city_name,
        "limit": 10
    }

    print(f"\n[DEBUG] Searching airports with URL: {url}")
    print(f"[DEBUG] Params: {params}")
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return []

    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: Could not search airports.")
        print(response.text)
        return []

    try:
        results = response.json().get("items", [])
    except Exception as e:
        print(f"❌ Failed to parse JSON: {e}")
        print(response.text)
        return []
    if not results:
        print("No airports found for that city.")
        return []

    print(f"\n🌐 Airports matching '{city_name}':")
    for i, airport in enumerate(results, 1):
        name = airport.get('name', 'Unknown')
        iata = airport.get('iata', 'N/A')
        location = airport.get('location', {})
        city = location.get('city')
        country = location.get('country', {}).get('name')
        # Try to show more info if city/country missing
        if not city:
            city = location.get('region') or location.get('state') or location.get('municipality') or 'Unknown'
        if not country:
            country = location.get('countryCode') or 'Unknown'
        # For debugging, print the whole location if still unknown
        if city == 'Unknown' or country == 'Unknown':
            print(f"[DEBUG] Full location for {name}: {location}")
        print(f"{i}. {name} ({iata}) – {city}, {country}")

    return results
        

if __name__ == "__main__":
    if not API_KEY or API_KEY.strip() == "":
        print("❌ RAPIDAPI_KEY not set in environment. Please check your .env file.")
        exit(1)

    city = input("Enter a city: ")
    airports = search_airports_by_city(city)

    if airports:
        while True:
            try:
                selection = int(input("Select airport number: ")) - 1
                if 0 <= selection < len(airports):
                    break
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Please enter a number.")
        chosen_iata = airports[selection]['iata']
        get_departures(chosen_iata)

