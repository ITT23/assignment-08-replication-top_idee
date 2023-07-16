# This is an implementation of the paper: PianoText: redesigning the piano keyboard for text entry
# At first you have to enter your input device and if you like that the sound of the piano is played back to you
# Than you can enter text with the piano in any application that allows keyboard entry
# You can view the mapping in the documentation (we decided that accords should be playable between octaves)
# You can quit the application by pressing esc and then closing it in the terminal
# (The mapping is set to the piano from the techbase)
import mido
from pynput.keyboard import Controller, Key
from pynput import keyboard
import pygame.midi
import time

keyboard = Controller()

FIRST_E_PIANO_NOTE = 12
BACKSPACE_NOTE = 72
RETURN_NOTE = 71
PIANO_NOTES = ['C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G', 'A', '#A', 'B']
INSTRUMENT = 0
# We considered that notes played with each other should only be considered an accord if they are in proximity of time
# The time frame can be set with this constant
TIME_FOR_NOTES_IN_ACCORD = 0.1

last_word = ''
notes = []
accords = []
current_notes = []
selected_device = None
midi_out = None

# reads in the mappings and has the system loop
def main(input_device, use_sound):
    global current_notes, last_word
    last_input_accord = False
    #setup
    read_accords()
    read_notes()
    create_out_put()
    with mido.open_input(input_device) as inport:
        # process loop
        for msg in inport:
            # There only should be output when a key is pressed
            if(msg.type == 'note_on'):
                # extended mapping to delete wrong input and have a return key
                if(msg.note == BACKSPACE_NOTE):
                    press_key(Key.backspace)
                if(msg.note == RETURN_NOTE):
                    press_key(Key.enter)
                # plays the note
                if(use_sound):
                    midi_out.note_on(msg.note, msg.velocity)
                #?
                if(msg.note - FIRST_E_PIANO_NOTE >= len(notes)):
                    continue
                # gets the current note and maps it to the key presses
                current_notes.append((get_note_value(msg.note), time.time()))
                # check if a existing accord is played
                if(len(current_notes) > 1):
                    if(accord_exists()):
                        word = check_accord()
                        if(word == None):
                            continue
                        if not last_input_accord:
                            press_key(Key.backspace)
                        # when a accord with three notes is played we have to delete the input form the accord with two notes
                        if(check_accord_three_notes()):
                            for char in last_word:
                                press_key(Key.backspace)
                                time.sleep(0.05)
                        # output the word entered with an accord
                        for char in word:
                            press_key(char)
                            time.sleep(0.05)
                        last_word = word
                        last_input_accord = True
                        continue
                # output letter for note
                press_key(notes[msg.note - FIRST_E_PIANO_NOTE])
                last_input_accord = False
            # when a key is released delete it from the current played notes
            if(msg.type == 'note_off'):
                if(use_sound):
                    midi_out.note_off(msg.note, msg.velocity)
                note = get_note_value(msg.note)
                for current_note in current_notes:
                    if(note == current_note[0]):
                        current_notes.remove(current_note)
                        break

# sets up the midi output
def create_out_put():
    global midi_out
    pygame.midi.init()
    port = pygame.midi.get_default_output_id()
    midi_out = pygame.midi.Output(port, 0, 8)
    midi_out.set_instrument(INSTRUMENT)

# reads the mapping in notes.txt
def read_notes():
    global notes
    with open('notes.txt', encoding='utf8') as file:
        for line in file:
            line = line.strip('\n')
            notes.append(line)

# reads the mapping in accords.txt
def read_accords():
    global accords
    with open('accords.txt', encoding='utf8') as file:
        for line in file:
            line = line.strip('\n')
            tokens = line.split()
            accords.append({
                'word': tokens[0],
                'notes': tokens[1:]
            })

# returns the notation (C - B) for a midi note
def get_note_value(note):
    note -= FIRST_E_PIANO_NOTE
    octave = int(note / 12)
    note -= octave * len(PIANO_NOTES)
    return PIANO_NOTES[note]

# checks if there is an existing accord
def check_accord():
    accord_notes = []
    last_note = current_notes[-1]
    for note in current_notes:
        if(last_note == note):
            continue
        if(last_note[1] - note[1]):
            accord_notes.append(note[0])
    accord_notes.append(last_note[0])
    for accord in accords:
        if (accord['notes'] == accord_notes):
            return accord['word']

# checks if the notes of the accord are entered close enough to each other
def accord_exists():
    accord_time = False
    for i in range(len(current_notes)):
        for j in range(len(current_notes)):
            if(i == j):
                continue
            if((TIME_FOR_NOTES_IN_ACCORD > current_notes[i][1] - current_notes[j][1]) and (-TIME_FOR_NOTES_IN_ACCORD < current_notes[i][1] - current_notes[j][1])):
                accord_time = True
                break
    return accord_time

# checks if there is an accord played consisting of three notes
def check_accord_three_notes():
    accord_notes = []
    last_note = current_notes[-1]
    for note in current_notes:
        if(last_note == note):
            continue
        if(last_note[1] - note[1]):
            accord_notes.append(note[0])
    accord_notes.append(last_note[0])
    if(len(accord_notes) > 2):
        return True
    return False

# Helper function to release key events
def press_key(event):
    keyboard.press(event)
    keyboard.release(event)

# used to quit pygame
def on_press(key):
    if(key == Key.esc):
        pygame.quit()


if __name__ == "__main__":
    devices = mido.get_input_names()
    print("Select input device")
    for index, device in enumerate(devices):
        print(f"{index}: {device}")
    
    selection = int(input())
    selected_device = devices[selection]

    print('Do you want to use sound?')
    print('1 - yes')
    print('2 - no')

    use_sound_answer = int(input())
    if(use_sound_answer):
        use_sound = True
    else:
        use_sound = False
    

    main(selected_device, use_sound)