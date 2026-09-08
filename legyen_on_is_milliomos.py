import tkinter as tk
from tkinter.ttk import Style
import random
import csv
import time
import winsound
from PIL import ImageTk, Image

class Question:
    def __init__(self,question,answer_a,answer_b,answer_c,answer_d,difficulty):
        self.question = question
        self.answer_a = answer_a
        self.answer_b = answer_b
        self.answer_c = answer_c
        self.answer_d = answer_d
        self.difficulty = difficulty

class MainApp(tk.Tk): #alap ablak
    def __init__(self):
        tk.Tk.__init__(self)

        self.attributes('-fullscreen',True)

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry("%dx%d" % (self.width,self.height))
        self.title("Legyen Ön is Milliomos")
        
        self.playSound(opening_music)
        
        self._frame = None
        
        self.openFile('Data/questions.csv')
        self.getRewards('Data/rewards.csv')
        self.questions_sorted = self.getQuestions(self.questions,"difficulty") #kérdések nehézség szerint válogatva
        self.question_number = 1 #kérdés sorszáma
        self.selected = None #kiválasztott válasz
        self.correct = None #helyes válasz
        self.reward_amount = 0 #nyeremény mennyisége
        self.reward_type = "cukorka" #nyeremény típus

        self.help_phone_state = 'normal'
        self.help_crowd_state = 'normal'
        self.help_halfer_state = 'normal'
        
    def switchFrame(self, frame_class): #lap váltás
        new_frame = frame_class(self) #az új frame létrehozása
        if self._frame is not None:
            self._frame.destroy() #törli az előző framet           
        self._frame = new_frame #a jelenlegi frame az új lesz
        self._frame.pack(fill='both', expand=True)

    def rightAnswer(self): #jó válasz
        self.playSound(correct_music)
        if self.question_number == 15:
            self.reward_amount = self.reward[14]
            self.switchFrame(RewardPage)
        else:
            self.switchFrame(DecisionPage)

    def wrongAnswer(self): #rossz válasz
        self.playSound(incorrect_music)
        DecisionPage.suddenLoss(self,self)

    def chooseAnswer(self,button): #válasz választása
        if button == self.selected: #azt nyomták meg, ami meg volt jelölve
            if button == self.correct:
                self.rightAnswer()
            else:
                self.wrongAnswer()
            return
        if self.selected is not None:
            self.selected.configure(image=image_button,fg="#ffffff")
        self.selected = button
        self.selected.configure(image=image_button_selected,fg="#000000")
        #print("mas")
            
    def playSound(self,sound): #hangeffekt lejátszása
        winsound.PlaySound(None, winsound.SND_PURGE) #leállítja a korábban játszott hangeffektet
        winsound.PlaySound(sound, winsound.SND_FILENAME|winsound.SND_ASYNC) #elindítja a hangeffektet

    def openFile(self,file):
        questions_file = open(file,encoding='utf-8') #megnyitja a .csv adatbázist
        question_csv = csv.reader(questions_file,delimiter=",") #olvassa az adatbázist
        self.questions = [] #kérdések+válaszok: [[kérdés],[válasz_a],[válasz_b],[válasz_c],[válasz_d],[nehézség(1-15)]]
        for row in question_csv:
            self.questions.append(Question(row[0],row[1],row[2],row[3],row[4],row[5])) #hozzáad egy kérdést
        questions_file.close()

    def getRewards(self,file):
        reward_file = open(file,encoding='utf-8')
        reward_csv = csv.reader(reward_file,delimiter=",")
        self.reward = []
        for row in reward_csv:
            self.reward.append(int(row[0]))
        reward_file.close()

    def getQuestions(self,objects,key):
        matching = {}
        for obj in objects:
            matching.setdefault(getattr(obj,key),[]).append(obj)
        return matching
        
class StartPage(tk.Frame): #kezdő lap
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.background = tk.Label(self)
        self.background.config(image=image_start_background,anchor="nw")
        self.background.image = image_background
        self.background.place(x=0,y=0)

        master.help_phone_state = 'normal'
        master.help_crowd_state = 'normal'
        master.help_halfer_state = 'normal'
        
        self.style = Style(self)
        master.question_number = 1
        self.style.configure("TLabel",font=('Arial',25))
        tk.Label(self,text="START",**style_label).place(anchor='center',rely=0.2,relx=0.5)
        tk.Button(self,image=image_start,command=lambda: master.switchFrame(QuestionPage)).place(anchor='center',relx=0.5,rely=0.5)
        
class QuestionPage(tk.Frame): #kérdés lap
    def __init__(self,master):
        tk.Frame.__init__(self,master) #létrehozza a lapot

        self.background = tk.Label(self)
        self.background.config(image=image_background,anchor="nw")
        self.background.image = image_background
        self.background.place(x=0,y=0)

        master.playSound(question_music) #zene bejátszása
        master.selected = None #változó ürítése
        
        #print(master.question_number)
        ditch = master.questions_sorted[str(master.question_number)]
        question_class = random.choice(ditch) #kérdés kiválasztása
        question = question_class.question
        question_index = master.questions.index(question_class)

        #válaszok kiválasztása
        answer_a = master.questions[question_index].answer_a
        answer_b = master.questions[question_index].answer_b
        answer_c = master.questions[question_index].answer_c
        answer_d = master.questions[question_index].answer_d

        #print(answer_a)
        
        label = tk.Label(self,text=f"{master.question_number}. {question}",image=image_question,**style_label,wraplength=master.width-300) #Kérdés
        label.place(anchor="center",relx=0.5,rely=0.15)
        
        self.button_a = tk.Button(self,state='normal',image=image_button,**style_button,text=answer_a,command=lambda:master.chooseAnswer(self.button_a))#Helyes válasz
        self.button_b = tk.Button(self,state='normal',image=image_button,**style_button,text=answer_b,command=lambda:master.chooseAnswer(self.button_b))#Rossz válasz
        self.button_c = tk.Button(self,state='normal',image=image_button,**style_button,text=answer_c,command=lambda:master.chooseAnswer(self.button_c))#Rossz válasz
        self.button_d = tk.Button(self,state='normal',image=image_button,**style_button,text=answer_d,command=lambda:master.chooseAnswer(self.button_d))#Rossz válasz

        master.correct = self.button_a
        
        buttons = [self.button_a,self.button_b,self.button_c,self.button_d]

        random.shuffle(buttons) #válaszok megkeverése

        #válaszok kiírása
        """buttons[0].pack(padx=20,pady=10)
        buttons[1].pack(padx=20,pady=10)
        buttons[2].pack(padx=20,pady=10)
        buttons[3].pack(padx=20,pady=10)"""

        buttons[0].place(relx=0.25,rely=0.4,anchor="center")
        buttons[1].place(relx=0.75,rely=0.4,anchor="center")
        buttons[2].place(relx=0.25,rely=0.7,anchor="center")
        buttons[3].place(relx=0.75,rely=0.7,anchor="center")

        self.help_phone = tk.Button(self,image=image_phone_help,state=master.help_phone_state,command=lambda:self.use_help_phone(master))
        self.help_crowd = tk.Button(self,image=image_audience_help,state=master.help_crowd_state,command=lambda:self.use_help_crowd(master))
        self.help_halfer = tk.Button(self,image=image_half_help,state=master.help_halfer_state,command=lambda:self.use_help_halfer(master))
        self.help_phone.pack()
        self.help_crowd.pack()
        self.help_halfer.pack()

        tk.Button(self,text="csalás",command=lambda:DecisionPage.continueGame(None,master)).place(anchor="center",relx=0.97,rely=0.97)

        self.help_phone.place(relx=0.1,rely=0.9)
        self.help_crowd.place(relx=0.15,rely=0.9)
        self.help_halfer.place(relx=0.2,rely=0.9)

    def use_help(self,master,button_state,button):
        setattr(master,button_state,'disabled')
        button.config(state='disabled')

    def use_help_halfer(self,master):
        master.playSound(hosthelp_music)
        setattr(master,"help_halfer_state",'disabled')
        self.help_halfer.configure(state='disabled')

        self.button_b.configure(state='disabled')
        self.button_c.configure(state='disabled')
        self.button_d.configure(state='disabled')
        decoy = random.choice([self.button_b,self.button_c,self.button_d])
        decoy.configure(state='normal')
        #print(decoy)

    def use_help_phone(self,master):
        master.playSound(phonehelp_music)
        setattr(master,"help_phone_state",'disabled')
        self.help_phone.configure(state='disabled')

    def use_help_crowd(self,master):
        master.playSound(audiencehelp_music)
        setattr(master,"help_crowd_state",'disabled')
        self.help_crowd.configure(state='disabled')
        #tk.Button(self,text="Vissza",command=lambda: master.switchFrame(StartPage)).grid(row=4)

class RewardPage(tk.Frame): #jutalom lap
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        
        self.background = tk.Label(self)
        self.background.config(image=image_background,anchor="nw")
        self.background.image = image_background
        self.background.place(x=0,y=0)
        

        tk.Label(self,text=f"Gratulálok! \n Nyereményed: {master.reward_amount} {master.reward_type}!",**style_label).place(anchor="center",rely=0.2,relx=0.5)
        #tk.Label(self,text="(1 csoki = 5 cukorka)",fg="#ffffff",compound="center",bg="#0000ff",font=('Copperplate Gothic Bold',20)).place(anchor="center",rely=0.3,relx=0.5)
        tk.Button(self,text="Új játék",**style_button,command=lambda: master.switchFrame(StartPage)).place(anchor="center",rely=0.4,relx=0.5)

class DecisionPage(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.background = tk.Label(self)
        self.background.config(image=image_background,anchor="nw")
        self.background.image = image_background
        self.background.place(x=0,y=0)
        
        tk.Label(self,text="Folytatod a játékot?",image=image_question,**style_label).place(anchor='center',relx=0.5,rely=0.15)
        tk.Button(self,text="Igen",image=image_button,**style_button,command=lambda: self.continueGame(master)).place(anchor="center",rely=0.5,relx=0.25)
        tk.Button(self,text="Nem",image=image_button,**style_button,command=lambda:self.checkOut(master)).place(anchor="center",rely=0.5,relx=0.75)

    def continueGame(self,master):
        master.question_number += 1
        master.switchFrame(QuestionPage)
        
    def checkOut(self,master):
        master.reward_amount = master.reward[master.question_number-1]
        master.switchFrame(RewardPage)
        
    def suddenLoss(self,master):
        if master.question_number<5:
            master.reward_amount = 0
        elif master.question_number<10:
            master.reward_amount = master.reward[4]
        elif master.question_number<15:
            master.reward_amount = master.reward[9]

        master.switchFrame(RewardPage)


opening_music = 'Music/opening.wav'
question_music = 'Music/question.wav'
rules_music = 'Music/rules.wav'
correct_music = 'Music/correct.wav'
incorrect_music = 'Music/incorrect.wav'
reward_music = 'Music/reward.wav'
noreward_music = 'Music/noreward.wav'
reflector_music = 'Music/reflector.wav'
phonehelp_music = 'Music/phonehelp.wav'
hosthelp_music = 'Music/hosthelp.wav'
audiencehelp_music = 'Music/audiencehelp.wav'

style_button = {'font':('Copperplate Gothic Bold',20,'bold'),'fg':"#ffffff",'compound':"center",'wraplength':300,'borderwidth':0,'bg':"#0000ff"}
style_label = {'font':('Copperplate Gothic Bold',30,'bold'),'fg':"#ffffff",'compound':"center",'bg':"#0000ff"}


if __name__ == "__main__": #MAIN
    root = MainApp()

    img_start = Image.open('Graphics/start_button.png')
    img_start = img_start.resize((root.width//3,root.height//3))
    image_start = ImageTk.PhotoImage(img_start)

    img_phone_help = Image.open('Graphics/phone_help.png')
    image_phone_help = ImageTk.PhotoImage(img_phone_help)
    
    img_half_help = Image.open('Graphics/half_help.png')
    image_half_help = ImageTk.PhotoImage(img_half_help)
    
    img_audience_help = Image.open('Graphics/audience_help.png')
    image_audience_help = ImageTk.PhotoImage(img_audience_help)
    
    img_button = Image.open('Graphics/button.png')
    image_button = ImageTk.PhotoImage(img_button)
    
    img_button_selected = Image.open('Graphics/button_selected.png')
    image_button_selected = ImageTk.PhotoImage(img_button_selected)
    
    img_question = Image.open('Graphics/question.png')
    img_question = img_question.resize((root.width-200,root.height//4))
    image_question = ImageTk.PhotoImage(img_question)

    img_background = Image.open('Graphics/background.png')
    img_background = img_background.resize((root.width,root.height))
    image_background = ImageTk.PhotoImage(img_background)

    img_start_background = Image.open('Graphics/start_background.png')
    img_start_background = img_start_background.resize((root.width,root.height))
    image_start_background = ImageTk.PhotoImage(img_start_background)

    root.switchFrame(StartPage)

    
    root.mainloop()
