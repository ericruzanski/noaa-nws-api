import requests

def get_ip():
    response = requests.get('https://whatismyip.akamai.com/')
    return response.text

def ip_to_lat_lon(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    data = response.json()
    loc = data['loc'].split(',')
    return loc[0], loc[1]

def get_weather_alerts(lat, lon):
    points_url = f'https://api.weather.gov/points/{lat},{lon}'
    points_response = requests.get(points_url)
    points_data = points_response.json()

    if 'properties' in points_data and 'forecastZone' in points_data['properties']:
        alerts_url = points_data['properties']['forecastZone']
        alerts_response = requests.get(alerts_url)
        alerts_data = alerts_response.json()

        if 'features' in alerts_data and alerts_data['features']:
            return alerts_data['features']
        else:
            return None
    else:
        return None

def main():
    ip_address = get_ip()
    print(f"IP Address: {ip_address}")

    lat, lon = ip_to_lat_lon(ip_address)
    print(f"Latitude: {lat}, Longitude: {lon}")

    alerts = get_weather_alerts(lat, lon)
    if alerts:
        print("Weather Alerts:")
        for alert in alerts:
            print(f"{alert['properties']['title']}: {alert['properties']['description']}")
    else:
        print("No active alerts for your location. Enjoy the pleasant weather.")

if __name__ == "__main__":
    main()
