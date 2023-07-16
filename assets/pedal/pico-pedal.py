import time
import board
import terminalio
import busio
import digitalio
import usb_midi
import usb_hid
import adafruit_midi
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

###
pin = board.GP6

keyboard = Keyboard(usb_hid.devices)

button = digitalio.DigitalInOut(pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN
           

#  note states
space_pressed = False


while True:

    if button.value and not space_pressed:
        keyboard.press(Keycode.SPACE)
        time.sleep(0.1)
        keyboard.release(Keycode.SPACE)
        space_pressed = True
    elif not button.value and space_pressed:
        space_pressed = False
