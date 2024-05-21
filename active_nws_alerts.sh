#!/bin/bash

# Define the NWS alerts API endpoint
API_URL="https://api.weather.gov/alerts/active"

# Use cURL to fetch the data and jq to parse it, then save it to a JSON file
curl -s "$API_URL" | jq '.' > active_nws_alerts.json

# Check whether the file was created and contains alert data
if [ -s active_alerts.json ]; then
    echo "NWS alerts fetched successfully and saved to active_nws_alerts.json"
else
    echo "Failed to fetch or save NWS alerts"
fi
