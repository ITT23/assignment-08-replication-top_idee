# Documentation

## 1. Paper-Stuff

First step was to find a paper that suits the requirements. We had read a few papers we found interesting:

* Preemptive Action: Accelerating Human Reaction using Electrical Muscle Stimulation Without Compromising Agency
  * Kasahara et al., 2019 | [https://doi.org/10.1145/3290605.3300873](https://doi.org/10.1145/3290605.3300873)
  * Reasons against it:
    * time - research about how to trigger the right muscle contraction
    * hardware - EMS TENS not available; we bought a cheap one just for fun but it lacks in control functionality
* Purring Wheel: Thermal and Vibrotactile Notifications on the Steering Wheel
  * San Vito et al., 2020 | [https://doi.org/10.1145/3382507.3418825](https://doi.org/10.1145/3382507.3418825)
  * Reasons against it:
    * hardware - sensors not available
    * application - just not cool enought
* Tactile Wayfinder: A Non-Visual Support System for Wayfinding
  * Heuten et al., 2008 | [https://doi.org/10.1145/1463160.1463179](https://doi.org/10.1145/1463160.1463179)
  * Reasons against it:
    * hardware - vibration modules to buy
    * application - just another navigation application
* TeslaTouch: electrovibration for touch surfaces
  * Bau et al., 2010 | [https://doi.org/10.1145/1866029.1866074](https://doi.org/10.1145/1866029.1866074)
  * Reasons against it:
    * hardware - no idea what we would've needed for it
* Touché: enhancing touch interaction on humans, screens, liquids, and everyday objects
  * Sato et al., 2012 | [https://doi.org/10.1145/2207676.2207743](https://doi.org/10.1145/2207676.2207743)
  * our favorite for a long time
  * Reasons against it:
    * hardware - no idea what sensors we needed + where to get them in the short time
* An Intuitive Tangible Game Controller
  * Foottit et al., 2014 | [https://doi.org/10.1145/2677758.2677774](https://doi.org/10.1145/2677758.2677774)
  * Reasons against it:
    * hardware - lot of sensors (all available, but the more sensors we have to put together the more could get wrong)

**Our decision**:

PianoText: redesigning the piano keyboard for text entry | Feit et al., 2014 | [https://doi.org/10.1145/2598510.2598547](https://doi.org/10.1145/2598510.2598547)

*insert short summary here*


## 2. Preparation

For replicating the interaction technique in the paper we needed a few things:

Hardware:

* Piano - we stole it from the media informatics lab
* a second MIDI Controller - because Christoph and Sabrina are seeing each other too often, the village is already talking about them; two controllers = everyone can work on MIDI input on their own
* Foot pedal - since the stolen piano didn't have one

Software-related:

* MIDI - knowledge
* mapping of MIDI-notes to the alphabet
* a nice application

### Hardware-Stuff

As mentioned we stole the piano from the media informatics lab. (some specifications here).

Since we feared that the village talk was getting out of hand, we decided to quickly assemble a miniature MIDI controller based on a Raspberry Pi Pico running on CircuitPython. You can see the code in the `midi-controller`-folder. Things needed:

* Raspberry Pi Pico
* 5 Buttons
* 10 Jumpercables

In the paper it was mentioned that the space-bar was not mapped on the keys, but on the foot pedal of the piano. Our stolen keyboard didn't had a foot pedal though, so we decided to assemble a pedal on our own. Like the test-midi-controller we build the pedal on a Raspberry Pi Pico running with? CircuitPython. We invested time and hard work to design, build and code the pedal box. 

Things you need:

* Raspberry Pi Pico
* Button - preferably an Arcade-Button
* 4x M2 screws
* 4x M2 nuts
* 2x M3 screws
* 2x M3 nuts
* 2x cable
* Solder-stuff
* 3D Printer to print the box itself

![1689355382333](image/documentation/1689355382333.png)

#### Design

The Pedal was designed in Blender with focus on easy assembly. The top has a slope to mimic a foot pedal and a hole to put in a Aracade-Button with 30mm diameter. On the bottom holes were included to secure a Raspberry Pi Pico and two flaps were designed to screw the bottom and top together. 

![1689354234309](image/documentation/1689354234309.png)

#### Code

On the Pico we imported the `adafruit-midi`-library to have a MIDI-output. Through the button press the MIDI-note 0 will get played/streamed, since this note is not likely to be played on normal pianos. The code can be seen in the `pico-pedal.py`-file in the `pedal`-folder. The library used is also linked. For the button input we chose the GPIO-Pin-6. 

#### Assembly

After two iterations of printing, we decided to let it be and do the missing things (place for nuts to be hold) with hot glue instead. Like in the code mentioned one button pin is soldered to the GPIO-pin-6 of the Pico and the other one to the 3.3V out (Pin 36). The Pico is then screwed on to the bottom with four M2 screws and nuts and the button is firmly placed in the top-hole. We then put glue on the inside of the button to prevent jiggly pressed and also glued on the M3 nuts onto the inside of the screw flaps of the bottom part. Bottom and top part were then put together and secured with the M3 screws.

![1689355388252](image/documentation/1689355388252.png)

### Software-Stuff

ToDo:

- mido
- pyaudio
- game
