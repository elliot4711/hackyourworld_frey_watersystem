import requests
import json

r = requests.get('https://node-red-hyw-frej.eu-gb.mybluemix.net/weather_data')
weather = r.json()
weather_data = []
for day in weather[0]["forecasts"]:
    weather_data.append(day["day"]["qpf"])
    weather_data.append(day["night"]["qpf"])
for y in range(4):
    print(weather_data[y])
