import requests
import json
import os

import requests

# https://rapidapi.com/nusantaracodedotcom/api/twitter-pack

url = "https://twitter-pack.p.rapidapi.com/search/tweet"

user = "elonmusk"

querystring = {"query":user,"count":"100"}

with open("API_Twitter_keys.json") as api_keys_file:
    api_keys = json.load(api_keys_file)

response = requests.get(url, headers=api_keys, params=querystring)

print(response.json())

if response.status_code == 200:
    data = response.json()  

    os.makedirs("Data", exist_ok=True)
    file_path = os.path.join("Data", "Twitter_User.json")

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON data saved to 'Twitter_User.json'")
else:
    print(f"Request failed with status code {response.status_code}")
