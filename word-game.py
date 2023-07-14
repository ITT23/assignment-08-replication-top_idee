import pyglet
import sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class Game:

    def __init__(self) -> None:
        self.current_sentece = "ja moin diggah".upper()
        self.correct_characters = 0
        self.label = pyglet.text.Label(text=self.current_sentece,
                                       font_name="Arial",
                                       font_size=20,
                                       x = WINDOW_WIDTH // 2,
                                       y = WINDOW_HEIGHT // 2,
                                       anchor_x='center',
                                       anchor_y='center')
        self.input_text = pyglet.text.Label(text="",
                                       font_name="Arial",
                                       font_size=20,
                                       color=(200,225,120,255),
                                       x = WINDOW_WIDTH // 2,
                                       y = WINDOW_HEIGHT // 2 - 100,
                                       anchor_x='center',
                                       anchor_y='center')
        self.score = 0
        self.score_text = pyglet.text.Label(text="",
                                       font_name="Arial",
                                       font_size=10,
                                       color=(255,255,255,255),
                                       x = 20,
                                       y = WINDOW_HEIGHT - 20,)
        
    def _draw(self):
        self.label.draw()
        self.input_text.draw()
        self.score_text.draw()

    def _check_input(self):
        input_lenght = len(self.input_text.text)
        if self.input_text.text == self.current_sentece[:input_lenght]:
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