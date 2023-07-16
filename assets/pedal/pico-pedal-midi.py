import time
import board
import terminalio
import busio
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

#  array of default MIDI notes
midi_note = 0

###
pin = board.GP6

button = digitalio.DigitalInOut(pin)
button.switch_to_input(pull=digitalio.Pull.DOWN)


#  note states
note0_pressed = False


while True:

    if button.value and note0_pressed is False:
        midi.send(NoteOn(midi_note, 120))
        print(f"{midi_note}, on")
        note0_pressed = True
    if not button.value and note0_pressed is True:
        midi.send(NoteOff(midi_note, 120))
        print(f"{midi_note}, off")
        note0_pressed = False
