import pyfirmata
import time
import requests
import sys


board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

board.analog[0].mode = pyfirmata.INPUT

while True:
    time.sleep(3)
    humidity = board.analog[0].read()
    humidity = round(humidity * 1023)
    
    print(humidity)
    
    r = requests.post('https://node-red-hyw-frej.eu-gb.mybluemix.net/humidity_endpoint', json={"humidity": humidity})
   #print(r.status_code)
    
    if humidity > 650:
        board.digital[10].write(1)
        time.sleep(5)
        board.digital[10].write(0)
    
    else:
        board.digital[10].write(0)
        
