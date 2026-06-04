
import customtkinter as tk

#import string tkinter variable and image library
from tkinter import StringVar
from PIL import Image
from customtkinter import CTkImage

#importing audio library with needed requirements
import os
os.environ["PATH"] = (os.path.dirname("C:\\Users\\26352\\PycharmProjects\\Chanuthi_AS91896\\libwinmedia.dll") + os.pathsep +
                      os.environ["PATH"])

from pygame import mixer

#initalize mode
currentMode = "Focus"

#initlizing timers for each mode in seconds
focusTime = 25*60
shortBreakTime = 5*60
longBreakTime = 10*60

#initalizing the session counter
sessions = 0

#initalize boolean variable of whether timer is running or paused
isTimerRunning = False

timeRemaining = 0  #initalizing time remaining variable

#creates task list frame that can scroll
class taskList(tk.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure((0), weight=1)
        self.values = values

        # iterating through the list of tasks to make a task tab for each
        for i, task in enumerate(self.values):
            # creating a task
            self.taskDone = tk.StringVar(value="notDone")
            self.task = tk.CTkCheckBox(self, height=39, width=331,
                                       hover_color="#515658", bg_color="#744B77", text_color="#FFFFFF",
                                       border_color="#595E61", border_width=12,
                                       fg_color="#5DB69F", font=tk.CTkFont(family="Consolas", size=24),
                                       text=task, checkmark_color="#5DB69F",
                                       variable=self.taskDone, onvalue="done", offvalue="notDone")

            # ensuring the text, no matter the length is visible at a glance
            self.task._text_label.configure(wraplength=300)
            # place task in the grid, with each task placed one row below the previous task
            self.task.grid(column=0, row=i, pady=10, padx=20)


#creates task list window
class TaskWindow(tk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Tasks")
        self.configure(fg_color="#160F37")
        #grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        #creating the task label on the the top right corner
        self.taskLabel = tk.CTkLabel(self, fg_color="#160F37", text="Tasks", text_color="#FFFFFF", font= tk.CTkFont(family="Consolas", size= 24))
        self.taskLabel.grid(column=0,row=0,sticky="e", padx=20)

        # creating a list of tasks
        self.tasks = ["Practice drums", "Do math homework", "Finish Macbeth Essay", "something",
                      "something else"]

        #placing the task list frame
        self.taskListFrame = taskList(self, values=self.tasks)
        self.taskListFrame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        #creating task input box
        self.taskInput = tk.CTkEntry(self, width=291, height=39, fg_color="#D9D9D9",font=tk.CTkFont(family="Consolas", size= 20),
                                     placeholder_text="add new task", placeholder_text_color="#030000")
        self.taskInput.grid(column=0,row=2, padx=10, pady=10)

        def updateAddButton(isHover):
            if isHover:
                self.addTaskButton.configure(image=CTkImage(light_image=Image.open("addTaskHover.png"), size=(40, 40)))
            else:
                self.addTaskButton.configure(image=CTkImage(light_image=Image.open("addTaskButton.png"), size=(40, 40)))

        #creating add task button
        self.addTaskButton = tk.CTkButton(self,fg_color="#160F37", text="", bg_color="#160F37",height=25, width=25,
                                       image=CTkImage(light_image=Image.open("addTaskButton.png"), size=(40,40)), hover_color="#160F37")

        self.addTaskButton.bind("<Enter>", lambda hover: updateAddButton(True))
        self.addTaskButton.bind("<Leave>", lambda hover: updateAddButton(False))

        self.addTaskButton.grid(column=0, row=2, padx=10, pady=10, sticky="e")

#creates timer app window
class TimerApp(tk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")

        # initialized window with name and make it fullscreen and the background color purple
        self.title("Productivity")
        self.config(background="#160F37")

        # configuring the grid geometry manager
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.timerDisplayTxt = StringVar(self, value="00:00")  # timer display text initalized as a Tkinter variable

        # creating Timer Display label
        self.timerDisplay = tk.CTkLabel(self, textvariable=self.timerDisplayTxt, text_color="#5DB69F",
                                        font=tk.CTkFont(family="Consolas", size=200), fg_color="#160F37")
        self.timerDisplay.grid(row=1, column=0, columnspan=3, sticky="ew")

        #set up player and load the music
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.set_volume(0.3)
        
        #music switch variable
        self.isMusicPlaying = tk.StringVar(value="off")

        #creating indicators within a list
        self.indicators = []

        #ensures there is no task list visible when program starts
        self.toplevel_window = None

        # creating the start button with a hover effect and linking its functionality
        def timerControl():
            global isTimerRunning
            isTimerRunning = not isTimerRunning
            if isTimerRunning == True:
                self.startBtn.configure(text="Pause")
                countdownTimer()
            else:
                self.startBtn.configure(text="Start")
                countdownTimer()

        #function  to change the button colour after music switch is on
        #plays the music when switch is on and stops music when switch is not on
        def musicControl():
            if self.isMusicPlaying.get() == "on":
                mixer.music.play(-1)
                self.musicSwitch.configure(button_color="white", button_hover_color="#EADDFF")
                self.musicIcon.configure(fg_color="white")
            else:
                mixer.music.pause()
                self.musicSwitch.configure(button_color="#79747E", button_hover_color="#49454F")
                self.musicIcon.configure(fg_color="#E6E0E9")

        #function to set session indicators
        def setIndicator():
            global sessions, currentMode
            for indicator in self.indicators:
                if sessions==4: #making session indicators invisible in long break
                    indicator.configure(fg_color="#160F37")
                elif sessions == 0: #resetting indicators after four sessions are completed
                    indicator.configure(fg_color="#595E61")
                else: #if session counter doesn't equal 4 or 0
                    for session in range(1,sessions+1): #counts sessions from 1-4
                        indicator = self.indicators[session-1] #changes color of indicators
                        # based on number of completed sessions
                        indicator.configure(fg_color= "#5DB69F")


        def openTasks(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists(): #checks if the task list window already exists or not
                self.toplevel_window = TaskWindow()  # create window
            else:
                self.toplevel_window.focus()  # if window exists focus it

        #function to update task button based on whether the button is in a hovering state or not
        def updateTaskButton(isHover):
            if isHover:
                self.taskButton.configure(image=CTkImage(light_image=Image.open("taskListHover.png"), size=(40,40)))
            else:
                self.taskButton.configure(image = CTkImage(light_image=Image.open("taskListButton.png"), size=(40, 40)))

        #creating four indicators and changing the x position
        for x in range(1,5):
            self.indicator=tk.CTkLabel(self, text="",fg_color= "#595E61", corner_radius=15,width=15,
                                       height=15, bg_color="#160F37")
            self.indicator.grid(row=0,column=0,sticky="nw", pady=20, padx=(30*x))
            self.indicators.append(self.indicator)


        self.startBtn = tk.CTkButton(self, text="Start", fg_color="#322952", bg_color="#160F37", text_color="#FFFFFF",
                                     font=tk.CTkFont(family="Consolas", size=20), command=timerControl,
                                     border_spacing=10,
                                     corner_radius=20, width=172, height=42, hover_color="#392E5E")
        self.startBtn.grid(row=2, column=1)

        # creating focus button
        self.focusBtn = tk.CTkButton(self, text="Focus", fg_color="#2A2244", bg_color="#160F37", text_color="#B776BB",
                                     command=lambda: setMode("Focus"), font=tk.CTkFont(family="Consolas", size=20),
                                     border_spacing=10, corner_radius=20, width=172, height=42, hover_color="#392E5E")
        self.focusBtn.grid(row=3, column=0, pady=30, sticky="e")

        # creating short break button
        self.shortBreakBtn = tk.CTkButton(self, text="Short Break", fg_color="#2A2244", bg_color="#160F37",
                                          text_color="#B776BB", command=lambda: setMode("Short Break"),
                                          font=tk.CTkFont(family="Consolas", size=20), border_spacing=10,
                                          corner_radius=20,
                                          width=172, height=42, hover_color="#392E5E")
        self.shortBreakBtn.grid(row=3, column=1, pady=30)

        # creating long break button
        self.longBreakBtn = tk.CTkButton(self, text="Long Break", fg_color="#2A2244", bg_color="#160F37",
                                         text_color="#B776BB", command=lambda: setMode("Long Break"),
                                         font=tk.CTkFont(family="Consolas", size=20), border_spacing=10,
                                         corner_radius=20,
                                         width=172, height=42, hover_color="#392E5E")
        self.longBreakBtn.grid(row=3, column=2, pady=30, sticky="w")

        #creating music switch and adding the music icon
        self.musicSwitch = tk.CTkSwitch(self, text="Music",
                                        variable=self.isMusicPlaying, onvalue="on", offvalue="off", bg_color="#160F37",
                                        button_color="#79747E", fg_color="#E6E0E9",
                                        switch_width=75, text_color="#160F37", switch_height=35,
                                        progress_color="#6750A4", command=musicControl, button_hover_color="#49454F")

        self.musicIcon = tk.CTkLabel(self,text_color="#160F37",image=CTkImage(light_image=Image.open("musicNote.png"),
                                                    size=(15,15)), width=2, height=5, fg_color="#E6E0E9",text="")
        self.musicIcon.place(x=670,y=24)
        self.musicSwitch.grid(row=0, column=2, pady=10, padx=10)

        self.taskButton = tk.CTkButton(self,fg_color="#160F37", text="Tasks", bg_color="#160F37",height=25, width=25,
                                       image=CTkImage(light_image=Image.open("taskListButton.png"), size=(40,40)), hover_color="#160F37", command=lambda: openTasks(self))
        self.taskButton.grid(row=0,column=2, sticky="ne", pady=10)

        self.taskButton.bind("<Enter>", lambda hover: updateTaskButton(True))
        self.taskButton.bind("<Leave>",lambda hover: updateTaskButton(False))

        # function for user to set the mode manually based on input from the buttons
        def setMode(newMode):
            global currentMode, isTimerRunning
            currentMode = newMode
            isTimerRunning = False
            self.startBtn.configure(text="Start")
            setTimer()


        # logic to select timer amount to match the mode, and changes the display colours of the mode buttons to showcase active mode
        def setTimer():
            global currentMode, timeRemaining
            if currentMode == "Focus":
                self.focusBtn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")
                self.shortBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.longBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                timeRemaining = focusTime
            elif currentMode == "Short Break":
                timeRemaining = shortBreakTime
                self.focusBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.shortBreakBtn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")
                self.longBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
            elif currentMode == "Long Break":
                timeRemaining = longBreakTime
                self.focusBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.shortBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.longBreakBtn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")

        # logic to switch mode based on the previous mode and the number of sessions completed
        def switchMode():
            global sessions, currentMode, isTimerRunning
            mixer.Channel(0).play(mixer.Sound("chime.mp3"))
            isTimerRunning = False
            self.startBtn.configure(text="Start")
            if currentMode == "Focus":
                sessions += 1
                if sessions == 4: # once four sessions are complete, long break starts
                    currentMode = "Long Break"
                    setTimer()
                elif sessions < 4:
                    currentMode = "Short Break"
            elif currentMode == "Long Break": #resetting counter at end of long break
                sessions = 0
                currentMode = "Focus"
            else:
                currentMode = "Focus"

        setTimer()

        # countdown function created
        def countdownTimer():
            global timeRemaining, isTimerRunning
            while timeRemaining != 0:
                self.timerDisplayTxt.set(
                    "{:02d}:{:02d}".format(timeRemaining // 60, timeRemaining % 60))  # update the timer display text
                self.update()  # updates the timer display
                if isTimerRunning:
                    timeRemaining -= 1
                self.after(1000)  # using after() function to wait 1 second before updating

            # after timer ends, mode is switched and the timer is reset

            switchMode()
            setIndicator()
            setTimer()


        countdownTimer()


root = TimerApp()
root.mainloop()
