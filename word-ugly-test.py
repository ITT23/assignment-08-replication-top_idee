import pyglet
import sys
import os
import string
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class GameManger:
    def __init__(self) -> None:
        self.mode = 0
        self.label = pyglet.text.Label(text="",
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
        self.score_text = pyglet.text.Label(text=f"{self.score}",
                                       font_name="Arial",
                                       font_size=10,
                                       color=(255,255,255,255),
                                       x = 20,
                                       y = 20)
        
    def _update_game_stats(self):
        self.score_text.text = f"{self.score}"

    # returns an array with letter and the image path for it
    def _get_mapping_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(".jpg"):
                letter = filename.split("_")[1].split(".")[0]
                complete_path = os.path.join(folder, filename)
                images.append((letter, complete_path))
        return images

    def _get_image_to_show(self, letter, images):
        for mapped_letter in images: #self.images
            if mapped_letter[0] == letter:
                return mapped_letter[1]
            
    def _draw(self):
        self.label.draw()
        self.input_text.draw()
        self.score_text.draw()
            
    # check input?????
    # return True, Ture -> right, maximum word right
    def _check_input(self): 
        input_length = len(self.input_text.text)
        if input_length == len(self.label.text):
            #self.input_text.text = ""
            # change text??? return???
            #self.score += 50
            if self.input_text.text == self.label.text[:input_length]:
                self.score += 50
                self.score_text.color = (0,255,0,255)
                return (True, True)
        if self.input_text.text == self.label.text[:input_length]:
            #self.score += 10
            self.score += 1
            self.score_text.color = (0,255,0,255)
            return (True, False)
        else:
            self.score -= 5
            self.score_text.color = (255,0,0,255)
            return (False, False)
    
#    def _change_input(self, text_to_show):
 #       self.shown_text = text_to_show
  #      print(f"change: {text_to_show}")
        # neuer text, neues image, whatever??


class Level_One:
    def __init__(self, game_mngr) -> None:
        self.game_mngr = game_mngr
        self.images_folder = "./assets/game/mapping"
        self.mapped_images = self.game_mngr._get_mapping_images(self.images_folder)
        self.input_list = string.ascii_uppercase
        self.text_to_show = ""
        self.image_to_show = None
        self._get_new_text()
         
        
    def _get_new_text(self):
        self.text_to_show = random.choice(self.input_list)
        self.game_mngr.label.text = self.text_to_show
        self.image_to_show = pyglet.image.load(self.game_mngr._get_image_to_show(self.text_to_show.lower(), self.mapped_images))


    def _draw(self):
        self.image_to_show.blit(25,200)



class Level_Two:
    def __init__(self, game_mngr) -> None:
        self.game_mngr = game_mngr
        self.input_list = string.ascii_uppercase
        self.text_to_show = ""
        self._get_new_text()
         
    def _get_new_text(self):
        self.text_to_show = random.choice(self.input_list)
        self.game_mngr.label.text = self.text_to_show

    def _draw(self):
        pass
        


window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
game_mngr = GameManger()
lvl_one = Level_One(game_mngr)
lvl_two = Level_Two(game_mngr)

levels = [lvl_one,lvl_two]


@window.event
def on_text(text):
    print(game_mngr.score)
    game_mngr.input_text.text += text.upper()
    current_state_correct, word_correct = game_mngr._check_input()
    if current_state_correct and not word_correct:
        # bist aufm richtigen weg schnuggi
        pass
    elif current_state_correct and word_correct:
        # new word bitch
        game_mngr.input_text.text = ""
        # array abfrage was menu grad fürn modus hat (im game_mngr?)
        levels[game_mngr.mode]._get_new_text()
        #lvl_one._get_new_text()
    else:
        #print(game_mngr.input_text.text)
        game_mngr.input_text.text = ""
        pass

@window.event
def on_draw():
    window.clear()
    game_mngr._update_game_stats()
    game_mngr._draw()
    levels[game_mngr.mode]._draw()

if __name__ == "__main__":
    pyglet.app.run()