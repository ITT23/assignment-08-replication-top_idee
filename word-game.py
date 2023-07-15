import pyglet
import sys
import os
import string
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class Game:

    def __init__(self) -> None:
        self.correct_characters = 0
        self.image_folder = "./assets/game/mapping"
        self.images = self._get_mapping_images(self.image_folder)
        self.shown_text = random.choice(string.ascii_uppercase)
        self.shown_image = pyglet.image.load(self._get_image_to_show(self.shown_text.lower()))

        self.label = pyglet.text.Label(text=self.shown_text,
                                       font_name="Arial",
                                       font_size=20,
                                       x = WINDOW_WIDTH // 2,
                                       y = WINDOW_HEIGHT // 2 - 50,
                                       anchor_x='center')
        self.input_text = pyglet.text.Label(text="",
                                       font_name="Arial",
                                       font_size=20,
                                       color=(200,225,120,255),
                                       x = WINDOW_WIDTH // 2,
                                       y = WINDOW_HEIGHT // 2 - 150,
                                       anchor_x='center',
                                       anchor_y='center')
        self.score = 0
        self.score_text = pyglet.text.Label(text="",
                                       font_name="Arial",
                                       font_size=10,
                                       color=(255,255,255,255),
                                       x = 20,
                                       y = WINDOW_HEIGHT - 20)
        
    def _get_mapping_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(".jpg"):
                letter = filename.split("_")[1].split(".")[0]
                complete_path = os.path.join(folder, filename)
                images.append((letter, complete_path))
        return images

    def _get_image_to_show(self, letter):
        for mapped_letter in self.images:
            if mapped_letter[0] == letter:
                return mapped_letter[1]


    def _draw(self):
        self.label.draw()
        self.input_text.draw()
        self.score_text.draw()
        self.shown_image.blit(25,200)

    def _check_input(self):
        input_lenght = len(self.input_text.text)
        if input_lenght == len(self.shown_text):
            self.input_text.text = ""
            self.shown_text = random.choice(string.ascii_uppercase)
            self.shown_image = pyglet.image.load(self._get_image_to_show(self.shown_text.lower()))
            self.label.text = self.shown_text
        elif self.input_text.text == self.shown_text[:input_lenght]:
            self.score += 20
        else:
            self.input_text.color = (255,0,0,255)
            print("wrong")

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
game = Game()

@window.event
def on_text(text):
    game.input_text.text += text.upper()
    game._check_input()

# @window.event
# def on_key_press(symbol, modifiers):
#     if symbol == pyglet.window.key.ESCAPE:
#         sys.exit(0)

@window.event
def on_draw():
    window.clear()
    game._draw()

if __name__ == "__main__":
    pyglet.app.run()