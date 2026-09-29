# Contains the assets used in the game.
# e.g. Buttons, SoundPlayers, ImageBoxes, ect.

import tkinter as tk

class Button(tk.Button):
    def __init__(self):
        pass


class AnswerButton(tk.Button):
    def __init__(self, image):
        self.pic_selected = None
        self.pic_deselected = None

        self.selected:bool = False

        self.configure(command=self.on_click)

    def set_answer(self, answer):
        pass

    # This is the function called when clicking on an answer option
    def on_click(self):
        if self.selected:
            self.selected = False

        else:
            self.selected = True



class MusicPlayer:
    def __init__(self):
        pass

    def playSound(self):
        pass

