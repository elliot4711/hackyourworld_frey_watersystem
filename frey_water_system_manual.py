import pyfirmata
import time
import requests
import sys


board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

board.analog[0].mode = pyfirmata.INPUT

def get_humidity():
    time.sleep(3)
    humidity = board.analog[0].read()
    humidity = round(humidity * 1023)
    print(humidity)
    return humidity

def post_humidity(humidity):
    r = requests.post('https://node-red-hyw-frej.eu-gb.mybluemix.net/humidity_endpoint', json={"humidity": humidity})
    print("post status: " + str(r.status_code))

def pump_control(humidity, weather_data): 
    precipation = 0  
    if humidity > 650:
        for y in range(4):
            precipation += weather_data[y]
        
        if precipation > 2:
            print("It will rain soon, postponing watering")
        else:
            print("Watering commencing")
            board.digital[10].write(1)
            time.sleep(5)
            board.digital[10].write(0)

    else:
        print("No watering needed")
        board.digital[10].write(0)

def get_weather():
    weather_data = [0, 6.5, 7, 0]
    return weather_data
    
    

if __name__ == "__main__":
    while True:
        humidity = get_humidity()
        post_humidity(humidity)
        weather_data = get_weather()
        pump_control(humidity, weather_data)
