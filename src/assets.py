# Contains the assets used in the game.
# e.g. Buttons, SoundPlayers, ImageBoxes, ect.

import tkinter as tk
from main import MainApp

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





class GameMaster:
    def __init__(self,master_app:tk.Tk):
        self.master_app:MainApp = master_app
        
        # Question related variables
        self.q_counter:int = -1 # If -1: no game is active; 0: first question
        self.q_max:int = 2

        self.end_of_game:bool = False

        self.questions = [None]

        self.helps:dict = {'fitfy':False,'phone':False,'crowd':False}
        self.disabled_helps:dict = self.helps.copy()
        self.resetAllHelp()
        print(self.helps)

    def __del__(self):
        self.master_app.changeFrame('start')
        return self is None
        


    # Starts the game -> chooses the questions for each level and loads them into a list
    def startGame(self):
        print("Started Game")
        # read 1 question for each difficulty
        # add later: choose the difficulty
        self.questions = ["Wiwiwi","Wuwuwi"]


        #jumps to first question
        self.nextQuestion()



    def toChoice(self):
        if self.q_counter+1 >= self.q_max:
            self.nextQuestion()
        else:
            self.master_app.changeFrame('choice')

    # QUESTION RELATED FUNCTIONS
    # Jumps to next question, called after correct answer
    def nextQuestion(self):
        self.q_counter += 1

        #if this condition is true, it is the end of the game, jumps to reward screen
        if self.q_counter >= self.q_max:
            self.q_counter = -1
            self.master_app.changeFrame('win')
            return 1

        print(self.q_counter)
        self.master_app.changeFrame('question')

    # Jumps to previous question
    def previousQuestion(self):
        self.q_counter -= 1
        if self.q_counter < 0:
            self.q_counter = 0

        print(self.q_counter)
        self.master_app.changeFrame('question')

    # Jumps to specific question
    def goToQuestion(self, question_number:int):
        self.q_counter = question_number
        if self.q_counter >= self.q_max:
            self.q_counter = -1
            self.master_app.changeFrame('win')
            return 1

        print(self.q_counter)
        self.master_app.changeFrame('question')
    # Jumps back to the first question
    def resetQuestions(self):
        self.q_counter = 0
        print(self.q_counter)
        self.master_app.changeFrame('question')

    def getQuestion(self):
        return self.q_counter +1, self.questions[self.q_counter]



    # HELP RELATED FUNCTIONS
    # Uses 
    def useHelp(self, help:str):
        if help not in self.helps.keys():
            return 1
        self.helps[help] = False

    def resetHelp(self, help:str):
        self.helps[help] = True

    def resetAllHelp(self):
        for help in self.helps:
            if not self.disabled_helps[help]: self.helps[help] = True



class MusicPlayer:
    def __init__(self):
        pass

    def playSound(self):
        pass

