import mido
from pynput.keyboard import Controller, Key
import pygame.midi
import time

keyboard = Controller()

notes = []
accords = []
current_notes = []


FIRST_E_PIANO_NOTE = 12
BACKSPACE_NOTE = 73
PIANO_NOTES = ['C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G', 'A', '#A', 'B']
last_word = ''

# accorde should only be playble in the octive
def main():
    global current_notes, last_word
    last_input_accord = False
    read_accords()
    read_notes()
    GRAND_PIANO = 0
    insturment = GRAND_PIANO
    pygame.midi.init()
    port = pygame.midi.get_default_output_id()
    midi_out = pygame.midi.Output(port, 0, 8)
    midi_out.set_instrument(insturment)
    with mido.open_input() as inport:
        for msg in inport:
            if(msg.type == 'note_on'):
                if(msg.note == BACKSPACE_NOTE):
                    keyboard.press(Key.backspace)
                    keyboard.release(Key.backspace)
                midi_out.note_on(msg.note, msg.velocity)
                #?
                if(msg.note - FIRST_E_PIANO_NOTE >= len(notes)):
                    continue
                current_notes.append((get_note_value(msg.note), time.time()))
                if(len(current_notes) > 1):
                    if(accord_exists()):
                        word = check_accord()
                        if(word == None):
                            continue
                        if not last_input_accord:
                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)
                        if(check_accord_three_notes()):
                            for char in last_word:
                                keyboard.press(Key.backspace)
                                keyboard.release(Key.backspace)
                                time.sleep(0.05)
                        for char in word:
                            keyboard.press(char)
                            keyboard.release(char)
                            time.sleep(0.05)
                        last_word = word
                        last_input_accord = True
                        continue
                keyboard.press(notes[msg.note - FIRST_E_PIANO_NOTE])
                keyboard.release(notes[msg.note - FIRST_E_PIANO_NOTE])
                last_input_accord = False
            if(msg.type == 'note_off'):
                midi_out.note_off(msg.note, msg.velocity)
                #?
                #if(msg.note - FIRST_E_PIANO_NOTE >= len(notes)):
                    #continue
                note = get_note_value(msg.note)
                for current_note in current_notes:
                    if(note == current_note[0]):
                        current_notes.remove(current_note)
                        break
                #current_notes.remove(note)


def read_notes():
    global notes
    with open('notes.txt', encoding='utf8') as file:
        for line in file:
            line = line.strip('\n')
            notes.append(line)

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

def get_note_value(note):
    note -= FIRST_E_PIANO_NOTE
    octave = int(note / 12)
    note -= octave * len(PIANO_NOTES)
    return PIANO_NOTES[note]

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
        #if(accord['notes'] == current_notes):
        if (accord['notes'] == accord_notes):
            return accord['word']


def accord_exists():
    accord_time = False
    for i in range(len(current_notes)):
        for j in range(len(current_notes)):
            if(i == j):
                continue
            if((0.1 > current_notes[i][1] - current_notes[j][1]) and (-0.1 < current_notes[i][1] - current_notes[j][1])):
                accord_time = True
                break
    return accord_time


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


main()