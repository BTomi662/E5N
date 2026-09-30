import os
import tkinter as tk

from assets import *


class MainApp (tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry("1280x720")
        #self.state('zoomed')
        self.title("Legyen Ön is Milliomos")

        self.fr_active = None
        self.GM = GameMaster(self)

        self.changeFrame('start')

    def changeFrame(self, frame:str):
        fr_prev = self.fr_active
        self.fr_active = self.createFrame(frame)
        if fr_prev is not None: fr_prev.destroy()

        self.fr_active.pack(fill='both', expand=True)

    def createFrame(self, frame:str):
        match frame:
            case 'start':
                return StartPage(self)
            case 'end':
                return EndPage(self)
            case 'question':
                return QuestionPage(self, self.GM)





class StartPage(tk.Frame):
    def __init__(self, master:tk.Tk):
        tk.Frame.__init__(self, master)

        
        print("SP")

        l_title = tk.Label(self,text="Who Wants to be a Millionaire?")
        l_title.pack()

        b_start = tk.Button(self,text="START",command=master.GM.startGame)
        b_start.pack()





class QuestionPage(tk.Frame):
    def __init__(self, master:tk.Tk, GM:GameMaster):
        tk.Frame.__init__(self, master)

        q_num, question = GM.getQuestion()
        l_q_number = tk.Label(self,text=f"{q_num}. Question")
        l_question = tk.Label(self,text=question)

        l_q_number.pack()
        l_question.pack()

        b_start = tk.Button(self,text="NEXT",command=GM.nextQuestion)
        b_start.pack()





class EndPage(tk.Frame):
    def __init__(self, master:tk.Tk):
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
    def __init__(self):
        tk.Frame.__init__(self)





class CheatsPage(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)





# MAIN LOOP
if __name__ == "__main__":
    root = MainApp()
    root.mainloop()