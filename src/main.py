import os
import tkinter as tk

from assets import *


class MainApp (tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Create window with starting size of half the screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width//2}x{height//2}")

        # Remove from comment to start in bordered fullscreen
        # self.state('zoomed')
        # Remove from comment to start in borderless fullscreen
        # self.state('fullscreen')

        # Set title for window
        # TODO: Changes based on language options
        self.title("Legyen Ön is Milliomos")

        # creates the GameMaster handling all gameplay related actions
        # e.g. tracking correct answers, choosing question, randomizing answers
        self.GM = GameMaster(self)

        # switch to the Homepage when window is created
        self.fr_active = None
        self.changeFrame('start')

    # Changes from current frame to given frame
    # frame:str -> the name of the frame to change to ['start','question','win','lose']
    # TODO: more intuitive input (e.g. Class as input, always create frame with MainApp parent)
    def changeFrame(self, frame:str):
        fr_prev = self.fr_active
        self.fr_active = self.createFrame(frame)
        if fr_prev is not None: fr_prev.destroy()

        self.fr_active.pack(fill='both', expand=True)


    # Returns frame based on the frame name
    # frame:str -> the name of the frame to create ['start','question','win','lose']
    def createFrame(self, frame:str):
        match frame:
            case 'start':
                return StartPage(self)
            case 'question':
                return QuestionPage(self)
            case 'choice':
                return ChoicePage(self)
            case 'win':
                return WinPage(self)
            case 'lose':
                return LosePage(self)





# The Homepage of the game
# This is the default frame when the window is created
class StartPage(tk.Frame):
    def __init__(self, master:tk.Tk):
        tk.Frame.__init__(self, master)

        
        print("SP")

        l_title = tk.Label(self,text="Who Wants to be a Millionaire?")
        l_title.pack()

        b_start = tk.Button(self,text="START",command=master.GM.startGame)
        b_start.pack()





# Frame for the questions
# Displays the question and the possible answers, the usable helps
class QuestionPage(tk.Frame):
    def __init__(self, master:MainApp):
        tk.Frame.__init__(self, master)

        q_num, question = master.GM.getQuestion()
        l_q_number = tk.Label(self,text=f"{q_num}. Question")
        l_question = tk.Label(self,text=question)

        l_q_number.pack()
        l_question.pack()

        b_start = tk.Button(self,text="NEXT",command=master.GM.toChoice)
        b_start.pack()



class ChoicePage(tk.Frame):
    def __init__(self, master:MainApp):
        tk.Frame.__init__(self, master)

        b_next = tk.Button(self,text="CONTINUE",command=master.GM.nextQuestion)
        b_next.pack()
        b_end = tk.Button(self,text="END GAME",command=lambda:master.GM.goToQuestion(999))
        b_end.pack()






class WinPage(tk.Frame):
    def __init__(self, master:MainApp):
        tk.Frame.__init__(self, master)

        l_q_number = tk.Label(self,text="Congratulations!")
        l_question = tk.Label(self,text="You won!")

        l_q_number.pack()
        l_question.pack()

        b_start = tk.Button(self,text="BACK TO HOME",command=self.endGame)
        b_start.pack()

    def endGame(self):
        self.master.GM = GameMaster(self.master)



class LosePage(tk.Frame):
    def __init__(self, master:MainApp):
        tk.Frame.__init__(self, master)

        l_q_number = tk.Label(self,text="Congratulations!")
        l_question = tk.Label(self,text="You won!")

        l_q_number.pack()
        l_question.pack()

        b_start = tk.Button(self,text="BACK TO HOME",command=self.endGame)
        b_start.pack()

    def endGame(self):
        self.master.GM = GameMaster(self.master)




class SettingsPage(tk.Frame):
    def __init__(self, master:MainApp):
        tk.Frame.__init__(self)





class CheatsPage(tk.Frame):
    def __init__(self, master:MainApp):
        tk.Frame.__init__(self)





# MAIN LOOP
if __name__ == "__main__":
    root = MainApp()
    root.mainloop()