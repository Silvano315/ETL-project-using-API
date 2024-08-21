import requests
import json
import os

import requests

# https://rapidapi.com/weatherbit/api/air-quality

url = "https://air-quality.p.rapidapi.com/history/airquality"

querystring = {"lon":"9.188","lat":"45.464"}

# Lat and Lon correspond to Milan, taken from https://www.latlong.net/place/milan-lombardy-italy-27241.html

headers = {
	"x-rapidapi-key": "1bfb9b4632msh4e1551fe30d9159p1f5563jsnf121f0b0713c",
	"x-rapidapi-host": "air-quality.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

if response.status_code == 200:
    data = response.json()  

    os.makedirs("Data", exist_ok=True)
    file_path = os.path.join("Data", "Milan_Air_Quality.json")

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON data saved to 'Milan_Air_Quality.json'")
else:
    print(f"Request failed with status code {response.status_code}")
