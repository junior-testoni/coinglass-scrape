
#get suported coins 
import requests

url = "https://open-api-v4.coinglass.com/api/futures/supported-coins"

headers = {
    "accept": "application/json",
    "CG-API-KEY": "53b0a3236d8d4d2b9fff517c70c544ea"
}

response = requests.get(url, headers=headers)

print(response.text)