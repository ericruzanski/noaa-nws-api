import requests
import json
import os

def fetch_and_save_nws_alerts():
    # Define the API endpoint
    api_url = "https://api.weather.gov/alerts/active"

    try:
        # Use requests to fetch the data
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the data and save it to a JSON file
        data = response.json()
        file_path = 'active_nws_alerts.json'
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Check whether the file was created and contains alert data
        if os.path.getsize(file_path) > 0:
            print("NWS alerts fetched successfully and saved to active_nws_alerts.json")
        else:
            print("Failed to save NWS alerts")

    except requests.RequestException as e:
        print(f"Failed to fetch or save NWS alerts: {e}")

if __name__ == "__main__":
    fetch_and_save_nws_alerts()
