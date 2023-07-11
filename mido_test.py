import mido

input_devices = mido.get_input_names()
print(input_devices[0])

with mido.open_input(input_devices[0]) as inport:
    for msg in inport:
        print(msg)