import subprocess
import json
from bs4 import BeautifulSoup

def fetch_html(url):
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    return result.stdout

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        return []

    rows = table.find_all('tr')

    data_list = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue

        data = {
            'NWS Hazard / Weather Event': cols[0].text.strip(),
            'Priority': cols[1].text.strip(),
            'Color Name': cols[3].text.strip(),
            'RGB Color': cols[4].text.strip(),
            'Hex Code': cols[5].text.strip()
        }
        data_list.append(data)
    return data_list

def save_data_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    url = "https://www.weather.gov/help-map"
    html = fetch_html(url)
    data = parse_html(html)
    save_data_to_json(data, 'nws_hazard_colors.json')

if __name__ == "__main__":
    main()
