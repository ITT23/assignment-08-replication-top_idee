import pyglet
import sys
import os
import string
import random
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
COLOR_WHITE = (245, 241, 224, 255)
COLOR_BLACK = (51, 51, 51,255)
COLOR_GREY = (102, 106, 134, 255)
COLOR_BLUE = (149, 184, 209, 255)
COLOR_RED = (237, 175, 184, 255)
#COLOR_GREEN_LIGHT = (159, 204, 46, 255)
COLOR_GREEN = (68, 118, 4, 255)

class GameManger:
    def __init__(self) -> None:
        self.mode = 0
        self.background = pyglet.shapes.Rectangle(x = 0, y = 0,
                                                  width= WINDOW_WIDTH,
                                                  height= WINDOW_HEIGHT,
                                                  color = COLOR_WHITE)
        self.label = pyglet.text.Label(text="",
                                       font_name="Arial",
                                       font_size=20,
                                       color= COLOR_BLACK,
                                       x = WINDOW_WIDTH // 2,
                                       y = WINDOW_HEIGHT // 2 - 40,
                                       anchor_x='center')
        self.input_text = pyglet.text.Label(text="",
                                       font_name="Arial",
                                       font_size=20,
                                       color=COLOR_GREEN,
                                       x = WINDOW_WIDTH // 2,
                                       y = WINDOW_HEIGHT // 2 - 130,
                                       anchor_x='center',
                                       anchor_y='center')
        self.score = 0
        self.score_text = pyglet.text.Label(text=f"Score: {self.score}",
                                       font_name="Arial",
                                       font_size=20,
                                       color= COLOR_BLACK,
                                       x = 20,
                                       y = 20)
        
    def _update_game_stats(self):
        self.score_text.text = f"Score: {self.score}"

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
            
    def _read_file(self, path):
        saved_words = []
        with open(path, "r") as words:
            for line in words:
                saved_words.append(line.upper().split("\n")[0])
        return saved_words
            
    def _draw(self):
        self.background.draw()
        self.label.draw()
        self.input_text.draw()
        self.score_text.draw()
            
    # return True, Ture -> right, maximum word right
    def _check_input(self): 
        input_length = len(self.input_text.text)
        if input_length == len(self.label.text):
            #self.input_text.text = ""
            # change text??? return???
            #self.score += 50
            if self.input_text.text == self.label.text[:input_length]:
                self.score += 50
                self.score_text.color = COLOR_GREEN
                return (True, True)
        if self.input_text.text == self.label.text[:input_length]:
            #self.score += 10
            self.score += 1
            self.score_text.color = COLOR_GREEN
            return (True, False)
        else:
            self.score -= 5
            self.score_text.color = COLOR_RED
            return (False, False)
    
    def _reset_stats(self):
        self.score = 0
        self.score_text.color = COLOR_BLACK
    

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

class Level_Three: 
    def __init__(self, game_mngr) -> None:
        self.game_mngr = game_mngr
        self.words_path = "./assets/game/words.txt"
        self.words = game_mngr._read_file(self.words_path)
    
    def _get_new_text(self):
        self.text_to_show = random.choice(self.words)
        self.game_mngr.label.text = self.text_to_show

    def _draw(self):
        pass



class Level_Four:
    def __init__(self, game_mngr) -> None:
        self.game_mngr = game_mngr
        self.words_path = "./assets/game/sentences.txt"
        self.words = game_mngr._read_file(self.words_path)
    
    def _get_new_text(self):
        self.text_to_show = random.choice(self.words)
        self.game_mngr.label.text = self.text_to_show

    def _draw(self):
        pass


class Level_Five:
    def __init__(self, game_mngr) -> None:
        self.game_mngr = game_mngr
        self.images_folder = "./assets/game/chords"
        self.chords_path = "./assets/game/chords.txt"
        self.mapped_images = self.game_mngr._get_mapping_images(self.images_folder)
        self.input_list = game_mngr._read_file(self.chords_path)
        self.text_to_show = ""
        self.image_to_show = None
        self._get_new_text()
        
    def _get_new_text(self):
        self.text_to_show = random.choice(self.input_list)
        self.game_mngr.label.text = self.text_to_show
        self.image_to_show = pyglet.image.load(self.game_mngr._get_image_to_show(self.text_to_show.lower(), self.mapped_images))

    def _draw(self):
        self.image_to_show.blit(25,200)



class Menu():

    def __init__(self, game_mngr):
        self.menu_visible = True
        self.color_unselected = COLOR_GREY
        self.color_selected = COLOR_GREEN
        self.menu_item_width = 250
        self.menu_item_height = 50
        self.x_pos = WINDOW_WIDTH // 2 - self.menu_item_width // 2
        self.menu_items = [pyglet.shapes.Rectangle(x=self.x_pos, y=280, width=self.menu_item_width, height=self.menu_item_height, color=self.color_selected),
                           pyglet.shapes.Rectangle(x=self.x_pos, y=220, width=self.menu_item_width, height=self.menu_item_height, color=self.color_unselected),
                           pyglet.shapes.Rectangle(x=self.x_pos, y=160, width=self.menu_item_width, height=self.menu_item_height, color=self.color_unselected),
                           pyglet.shapes.Rectangle(x=self.x_pos, y=100, width=self.menu_item_width, height=self.menu_item_height, color=self.color_unselected),
                           pyglet.shapes.Rectangle(x=self.x_pos, y=40, width=self.menu_item_width, height=self.menu_item_height, color=self.color_unselected)
                           ]
        self.menu_labels = [pyglet.text.Label(text="Train mapping", font_name="Arial", font_size=20, color= COLOR_WHITE, x = WINDOW_WIDTH // 2, y = 295, anchor_x='center'),
                            pyglet.text.Label(text="Exercise mapping", font_name="Arial", font_size=20, color= COLOR_WHITE, x = WINDOW_WIDTH // 2, y = 235, anchor_x='center'),
                            pyglet.text.Label(text="Write words", font_name="Arial", font_size=20, color= COLOR_WHITE, x = WINDOW_WIDTH // 2, y = 175, anchor_x='center'),
                            pyglet.text.Label(text="Write sentences", font_name="Arial", font_size=20, color= COLOR_WHITE, x = WINDOW_WIDTH // 2, y = 115, anchor_x='center'),
                            pyglet.text.Label(text="Train chords", font_name="Arial", font_size=20, color= COLOR_WHITE, x = WINDOW_WIDTH // 2, y = 55, anchor_x='center'),
                            pyglet.text.Label(text="Select Level with arrow keys,\nstart with space / foot pedal", font_size = 12, color = COLOR_BLACK, x = 30, y = WINDOW_HEIGHT // 2, 
                                              width=self.menu_item_width, anchor_y='center', multiline=True)
                            ]
        self.background = pyglet.shapes.Rectangle(x = 0, y = 0,
                                                  width= WINDOW_WIDTH,
                                                  height= WINDOW_HEIGHT,
                                                  color = COLOR_WHITE)
        self.selected_item = 0 # top one

    def draw_menu(self):
        self.background.draw()
        for item in self.menu_items:
            item.draw()
        for label in self.menu_labels:
            label.draw()

    def reset_colors(self):
        for item in self.menu_items:
            item.color = self.color_unselected
    
    # visually sets the menu item as marked/selected
    def update_menu(self, direction: int):
        if self.selected_item + direction < len(self.menu_items) and self.selected_item + direction >= 0: # index must stay in boundaries of list-items
            self.selected_item += direction 
            self.reset_colors()
            self.menu_items[self.selected_item].color = self.color_selected
            #game_mngr.mode = self.selected_item



window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

game_mngr = GameManger()
menu = Menu(game_mngr)
lvl_one = Level_One(game_mngr)
lvl_two = Level_Two(game_mngr)
lvl_three = Level_Three(game_mngr)
lvl_four = Level_Four(game_mngr)
lvl_five = Level_Five(game_mngr)

levels = [lvl_one,lvl_two, lvl_three, lvl_four, lvl_five]


@window.event
def on_text(text):
    if not menu.menu_visible:
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
def on_key_press(symbol, modifier): 
    if menu.menu_visible:       
        if symbol == pyglet.window.key.UP:
            menu.update_menu(-1) # upwards direction
        elif symbol == pyglet.window.key.DOWN:
            menu.update_menu(1) # downwards direction
    if game_mngr.mode == 4:
        time.sleep(0.2)

@window.event
def on_key_release(symbol, modifier):         
    if symbol == pyglet.window.key.SPACE and menu.menu_visible:
        game_mngr.mode = menu.selected_item
        levels[game_mngr.mode]._get_new_text()
        game_mngr._reset_stats()
        menu.menu_visible = False


@window.event
def on_draw():
    window.clear()
    if menu.menu_visible:
        menu.draw_menu()
    else:
        game_mngr._update_game_stats()
        game_mngr._draw()
        levels[game_mngr.mode]._draw()

@window.event
def on_show():
    levels[game_mngr.mode]._get_new_text()


if __name__ == "__main__":
    pyglet.app.run()