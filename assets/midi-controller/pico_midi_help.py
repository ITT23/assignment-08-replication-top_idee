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
midi_notes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]

###

#  button pins, all pins in order skipping GP15
#note_pins = [board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
#             board.GP12, board.GP13]
note_pins = [board.GP6, board.GP7, board.GP8]


note_buttons = []

for pin in note_pins:
    note_pin = digitalio.DigitalInOut(pin)
    #note_pin.direction = digitalio.Direction.INPUT
    note_pin.direction = digitalio.Direction.OUTPUT
    #note_pin.pull = digitalio.Pull.UP
    note_pin.switch_to_input(pull=digitalio.Pull.DOWN)
    note_buttons.append(note_pin)

#  note states
note0_pressed = False
note1_pressed = False
note2_pressed = False
note3_pressed = False
note4_pressed = False
note5_pressed = False
note6_pressed = False
note7_pressed = False
note8_pressed = False

#  array of note states
note_states = [note0_pressed, note1_pressed, note2_pressed, note3_pressed,
               note4_pressed, note5_pressed, note6_pressed, note7_pressed,
               note8_pressed]



while True:
    for i, button in enumerate(note_buttons):
        if button.value and note_states[i] is False:
            midi.send(NoteOn(midi_notes[i], 120))
            print(f"{midi_notes[i]}, on")
            note_states[i] = True
        if not button.value and note_states[i] is True:
            midi.send(NoteOff(midi_notes[i], 120))
            print(f"{midi_notes[i]}, off")
            note_states[i] = False