import requests

def get_ip():
    response = requests.get('https://whatismyip.akamai.com/')
    return response.text

def ip_to_lat_lon(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    data = response.json()
    loc = data['loc'].split(',')
    return loc[0], loc[1]

def celsius_to_fahrenheit(celsius):
    if celsius is None:
        return 'N/A'
    return round((celsius * 9 / 5) + 32, 1)

def kmh_to_mph(kmh):
    if kmh is None:
        return 'N/A'
    return round(kmh * 0.621371, 1)

def get_current_conditions(lat, lon):
    points_url = f'https://api.weather.gov/points/{lat},{lon}'
    points_response = requests.get(points_url)
    points_data = points_response.json()

    if 'properties' in points_data and 'observationStations' in points_data['properties']:
        city = points_data['properties']['relativeLocation']['properties']['city']
        state = points_data['properties']['relativeLocation']['properties']['state']
        stations_url = points_data['properties']['observationStations']
        stations_response = requests.get(stations_url)
        stations_data = stations_response.json()

        if 'features' in stations_data and stations_data['features']:
            station_url = stations_data['features'][0]['id']
            current_observation_url = station_url + '/observations/latest'
            observation_response = requests.get(current_observation_url)
            observation_data = observation_response.json()

            if 'properties' in observation_data:
                observation_properties = observation_data['properties']
                temperature_c = observation_properties.get('temperature', {}).get('value')
                temperature_f = celsius_to_fahrenheit(temperature_c)
                wind_speed_kmh = observation_properties.get('windSpeed', {}).get('value')
                wind_speed_mph = kmh_to_mph(wind_speed_kmh)
                description = observation_properties.get('textDescription', 'N/A')
                return city, state, temperature_f, wind_speed_mph, description
            else:
                return city, state, "No current weather data available."
        else:
            return city, state, "No observation stations found."
    else:
        return None, None, "No data available for this location."

def main():
    ip_address = get_ip()

    lat, lon = ip_to_lat_lon(ip_address)

    city, state, temperature_f, wind_speed_mph, description = get_current_conditions(lat, lon)
    if temperature_f is not None:
        print(f"Current Weather Conditions for {city}, {state}:")
        print(f"Temperature: {temperature_f}°F")
        print(f"Wind Speed: {wind_speed_mph} mph")
        print(f"Description: {description}")
    else:
        print("No current weather data available.")

if __name__ == "__main__":
    main()
