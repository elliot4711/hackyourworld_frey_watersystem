import pyfirmata
import time as t
import requests
import sys
import datetime


board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

board.analog[0].mode = pyfirmata.INPUT

def get_humidity():
    t.sleep(3)
    humidity = board.analog[0].read()
    humidity = round(humidity * 1023)
    print(humidity)
    return humidity

def post_humidity(humidity, status, time):
    r = requests.post('https://node-red-hyw-frej.eu-gb.mybluemix.net/humidity_endpoint', json={"humidity": humidity, "status": status, "time": time})
    print("post status: " + str(r.status_code))

def activation_date(time):
    r = requests.post('https://node-red-hyw-frej.eu-gb.mybluemix.net/pump_activated', json={"time": time})
    print("post status: " + str(r.status_code))

def pump_control(humidity, weather_data):
    time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    precipation = 0  
    if humidity > 650:
        for y in range(4):
            precipation += weather_data[y]
        
        if precipation > 2:
            print("It will rain soon, postponing watering")
            post_humidity(humidity, "Dry", time)
        else:
            print("Watering commencing")
            activation_date(time)
            post_humidity(humidity, "Dry", time)
            board.digital[10].write(1)
            t.sleep(5)
            board.digital[10].write(0)

    else:
        print("No watering needed")
        post_humidity(humidity, "Wet", time)
        board.digital[10].write(0)

def get_weather():
    r = requests.get('https://node-red-hyw-frej.eu-gb.mybluemix.net/weather_data')
    weather = r.json()
    weather_data = []
    for day in weather[0]["forecasts"]:
        try:
            weather_data.append(day["day"]["qpf"])
        except Exception:
            pass
        try:
            weather_data.append(day["night"]["qpf"])
        except Exception:
            pass
    return weather_data
    
    

if __name__ == "__main__":
    while True:
        humidity = get_humidity()
        weather_data = get_weather()
        pump_control(humidity, weather_data)
