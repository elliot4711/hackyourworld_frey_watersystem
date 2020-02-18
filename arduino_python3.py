import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

board.digital[12].mode = pyfirmata.INPUT

for _ in range(30):
    sw = board.digital[12].read()
    print(sw)
    time.sleep(1)