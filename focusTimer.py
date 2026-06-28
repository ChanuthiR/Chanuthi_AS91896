import sys

#importing ctk for GUI
import customtkinter as tk

#import string tkinter variable and image library
from tkinter import StringVar

import pygame
from PIL import Image
from customtkinter import CTkImage

#importing messagebox library
from tkinter import messagebox

#importing audio library
from pygame import mixer

#Import library for partial function for checkboxes
from functools import partial

#initalize mode
currentMode = "Focus"

#initlizing timers for each mode in seconds
focusTime = 5
shortBreakTime = 2
longBreakTime = 10

#initalizing the session counter
sessions = 0

#initalize boolean variable of whether timer is running or paused
isTimerRunning = False

timeRemaining = 0  #initalizing time remaining variable

# creating a list of tasks
tasks = []


#creates task list frame that can scroll
class taskList(tk.CTkScrollableFrame):

    def __init__(self, master, values):
        #configuration of task list frame with a single column and dark purple background
        super().__init__(master)
        self.configure(fg_color="#160F37")
        self.grid_columnconfigure((0), weight=1)

        #using the task list as an argument for the update function
        self.values = values
        self.update(self.values)


    #function to update checkbox and remove button display when selected and unselected
    def updateCheckbox(self, taskNo):
        if self.taskVars[taskNo].get():
            self.taskCheckboxes[taskNo].configure(bg_color="#2A2244",text_color="#595E61", font=tk.CTkFont(family="Consolas", size=24, overstrike=True))
            self.removeButtons[taskNo].configure(fg_color="#2A2244",bg_color="#2A2244", hover_color="#2A2244")
        else:
            self.taskCheckboxes[taskNo].configure(bg_color="#744B77", text_color="#FFFFFF",
                                                  font=tk.CTkFont(family="Consolas", size=24, overstrike=False))
            self.removeButtons[taskNo].configure(fg_color="#744B77",bg_color="#744B77",hover_color="#744B77")

    #function to update the remove button depending on whether it is hovered over or not
    def updateRemoveButton(self, isHover, buttonNo, partial):
        if isHover:
            self.removeButtons[buttonNo].configure(image=CTkImage(light_image=Image.open("removeTaskHover.png"), size=(20, 20)))
        else:
            self.removeButtons[buttonNo].configure(image=CTkImage(light_image=Image.open("removeTaskButton.png"), size=(20, 20)))

    def removeTask(self, taskNo):
        #remove task from the task list
        tasks.pop(taskNo)

        #play chime when task is removed
        mixer.Channel(0).play(mixer.Sound("chime.mp3"))

        #update task list
        self.update(tasks)

    #function to update the checkbox display
    def update(self, values):
        #destroy all checkboxes to ensure no garbage collected
        for checkbox in self.winfo_children():
            checkbox.destroy()

        #created a list of the task variables
        self.taskVars =[]

        #create list to hold the checkboxes and respective remove buttons
        self.taskCheckboxes = []
        self.removeButtons = []

        # iterating through the list of tasks to make a task tab for each
        for i, task in enumerate(values):
             # creating a task with a boolean variable to hold checkbox value
            self.taskDone = tk.BooleanVar()
            self.taskVars.append(self.taskDone)

            self.task = tk.CTkCheckBox(self, height=39, width=320,
                                           hover_color="#515658", bg_color="#744B77", text_color="#FFFFFF",
                                           border_color="#595E61", border_width=12,
                                           fg_color="#5DB69F", font=tk.CTkFont(family="Consolas", size=24),
                                           text=task, checkmark_color="#5DB69F",
                                       variable=self.taskVars[i],
                                       command=partial(self.updateCheckbox, i))
            #ensuring the text, no matter the length is visible at a glance
            self.task._text_label.configure(wraplength=300)

            #update geometry manager
            self.task.update()

            #creating remove task button
            #getting the height of the task checkbox and matching it as the height of the remove button
            self.removeTaskButton = tk.CTkButton(self, fg_color="#744B77", text="", bg_color="#744B77",height=self.task.winfo_reqheight(), width=10,
                                       image=CTkImage(light_image=Image.open("removeTaskButton.png"), size=(20,20)), hover_color="#744B77",
                                                 command=partial(taskList.removeTask, self, i))

            # add the created remove button to the remove button array
            self.removeButtons.append((self.removeTaskButton))

            #bindings to have events when the button is hovered over and not hovered over
            self.removeButtons[i].bind("<Enter>", partial(self.updateRemoveButton, True, i))
            self.removeButtons[i].bind("<Leave>",  partial(self.updateRemoveButton, False, i))

            self.removeButtons[i].grid(column=0,row=i,sticky="e")


            # place task in the grid, with each task placed one row below the previous task
            self.task.grid(column=0, row=i, pady=10, padx=20)

            #adding created checkbox to the array
            self.taskCheckboxes.append(self.task)

        #ensuring task vars is visible to outer functions
        return self.taskVars



#creates task list window
class taskWindow(tk.CTkToplevel):
    global tasks
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        #ensure window cannot be resized
        self.resizable(False, False)
        self.title("Tasks")
        self.configure(fg_color="#160F37")
        #grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        #ensure window stays on top of other windows
        self.wm_attributes("-topmost", 1)

        #creating the task label on the the top right corner
        self.taskLabel = tk.CTkLabel(self, fg_color="#160F37", text="Tasks", text_color="#FFFFFF", font= tk.CTkFont(family="Consolas", size= 24))
        self.taskLabel.grid(column=0,row=0,sticky="e", padx=20)

        #creating task variable
        self.tasks = tasks

        #placing the task list frame
        self.taskListFrame = taskList(self, values=self.tasks)
        self.taskListFrame.grid(row=1, column=0, padx=10, sticky="nsew")

        #creating task input box
        self.taskInput = tk.CTkEntry(self, width=291, height=39, fg_color="#D9D9D9",font=tk.CTkFont(family="Consolas", size= 20),
                                     placeholder_text="add new task", placeholder_text_color="#030000")
        self.taskInput.grid(column=0,row=2, padx=10, pady=10)

        #updating add task button depending on if the user is hovering or not
        def updateAddButton(isHover):
            if isHover:
                self.addTaskButton.configure(image=CTkImage(light_image=Image.open("addTaskHover.png"), size=(40, 40)))
            else:
                self.addTaskButton.configure(image=CTkImage(light_image=Image.open("addTaskButton.png"), size=(40, 40)))


        #function to add a task
        def addTask():
            #input validation of task input, should not be empty string and should only contain alphanumeric characters
            if self.taskInput.get()=="":
                messagebox.askretrycancel("Invalid Input","Input cannot be empty")
            #removes spaces which are considered special characters before checking whether all characters are alphanumeric
            elif not self.taskInput.get().replace(" ","").isalnum():
                messagebox.askretrycancel("Invalid Input","Input should not contain special characters ")
            else:
                tasks.append(self.taskInput.get())
                #update the task list frame
                taskList.update(self.taskListFrame, values=self.tasks)
                #remove input from entry box
            self.taskInput.delete(0,len(self.taskInput.get()))

        #creating add task button
        self.addTaskButton = tk.CTkButton(self,fg_color="#160F37", text="", bg_color="#160F37",height=25, width=25,
                                       image=CTkImage(light_image=Image.open("addTaskButton.png"), size=(40,40)),
                                          hover_color="#160F37", command=addTask)
        #adding binding for events for when the button is hovered over or not
        self.addTaskButton.bind("<Enter>", lambda hover: updateAddButton(True))
        self.addTaskButton.bind("<Leave>", lambda hover: updateAddButton(False))

        self.addTaskButton.grid(column=0, row=2, padx=10, pady=10, sticky="e")


#creates timer app window
class TimerApp(tk.CTk):
    def __init__(self):
        super().__init__()

        # initialized window with name and make it fullscreen and the background color purple
        self.title("Productivity")
        self.config(background="#160F37")
        self.geometry("800x500")

        # ensure window cannot be resized
        self.resizable(False, False)

        #ensure window stays on top of other windows
        self.wm_attributes("-topmost", 1)

        # configuring the grid geometry manager
        self.grid_columnconfigure((1), weight=2)
        self.grid_columnconfigure((0), weight=0)
        self.grid_columnconfigure((2), weight=1)


        self.timerDisplayTxt = StringVar(self, value="00:00")  # timer display text initalized as a Tkinter variable

        # creating Timer Display label
        self.timerDisplay = tk.CTkLabel(self, textvariable=self.timerDisplayTxt, text_color="#5DB69F",
                                        font=tk.CTkFont(family="Consolas", size=200), fg_color="#160F37")
        self.timerDisplay.grid(row=1, column=0, columnspan=3, sticky="ew")

        #set up player, volume, and load the music
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.set_volume(0.3)
        
        #music switch variable
        self.isMusicPlaying = tk.StringVar(value="off")

        #creating indicators within a list
        self.indicators = []

        #ensures there is no task list visible when program starts
        self.toplevel_window = None

        #function to control the timer and update the start button GUI
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
                if sessions==4: #making session indicators invisible when sessions are complete
                    indicator.configure(fg_color="#160F37")
                    self.indicatorLabel.configure(text_color="#160F37")
                elif sessions == 0: #resetting indicators after long break is completed
                    indicator.configure(fg_color="#595E61")
                    self.indicatorLabel.configure(text_color="#5DB69F")
                else: #if session counter doesn't equal 4 or 0
                    for session in range(1,sessions+1): #counts sessions from 1-4
                        indicator = self.indicators[session-1] #changes color of indicators
                        # based on number of completed sessions
                        indicator.configure(fg_color= "#5DB69F")
                        self.indicatorLabel.configure(text="{}/4".format(sessions))

            self.indicatorLabel.update()

    #function to open task window
        def openTasks(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists(): #checks if the task list window already exists or not
                self.toplevel_window = taskWindow()  # create window
            else:
                self.toplevel_window.focus()  # if window exists focus it

        #function to update task button based on whether the button is in a hovering state or not
        def updateTaskButton(isHover):
            if isHover:
                self.taskButton.configure(image=CTkImage(light_image=Image.open("taskListHover.png"), size=(40,40)))
            else:
                self.taskButton.configure(image = CTkImage(light_image=Image.open("taskListButton.png"), size=(40, 40)))

        #creating four indicators using a for and changing the x position for each so it shifts to the right for each indicator
        self.indicatorLabel = tk.CTkLabel(self, text="0/4",fg_color= "#160F37",width=15,
                                       height=15, bg_color="#160F37", font=tk.CTkFont(family="Consolas", size=20)
                                          , text_color="#5DB69F")
        self.indicatorLabel.grid(row=0, column=0, sticky="w", pady=(10,24), padx=28)

        for x in range(1,5):
            self.indicator=tk.CTkLabel(self, text="",fg_color= "#595E61", corner_radius=15,width=15,
                                       height=15, bg_color="#160F37")
            self.indicator.grid(row=0,column=0,sticky="nw", pady=20, padx=(40+(30*x)))
            self.indicators.append(self.indicator)

        # creating the start button with a hover effect and linking its functionality
        self.startBtn = tk.CTkButton(self, text="Start", fg_color="#322952", bg_color="#160F37", text_color="#FFFFFF",
                                     font=tk.CTkFont(family="Consolas", size=20), command=timerControl,
                                     border_spacing=10,
                                     corner_radius=20, width=172, height=42, hover_color="#392E5E")
        self.startBtn.place(x=320, y=300)

        # creating focus button
        self.focusBtn = tk.CTkButton(self, text="Focus", fg_color="#2A2244", bg_color="#160F37", text_color="#B776BB",
                                     command=lambda: setMode("Focus"), font=tk.CTkFont(family="Consolas", size=20),
                                     border_spacing=10, corner_radius=20, width=172, height=42, hover_color="#392E5E")
        self.focusBtn.place(x=120, y=390)

        # creating short break button
        self.shortBreakBtn = tk.CTkButton(self, text="Short Break", fg_color="#2A2244", bg_color="#160F37",
                                          text_color="#B776BB", command=lambda: setMode("Short Break"),
                                          font=tk.CTkFont(family="Consolas", size=20), border_spacing=10,
                                          corner_radius=20,
                                          width=172, height=42, hover_color="#392E5E")
        self.shortBreakBtn.place(x=320, y=390)

        # creating long break button
        self.longBreakBtn = tk.CTkButton(self, text="Long Break", fg_color="#2A2244", bg_color="#160F37",
                                         text_color="#B776BB", command=lambda: setMode("Long Break"),
                                         font=tk.CTkFont(family="Consolas", size=20), border_spacing=10,
                                         corner_radius=20,
                                         width=172, height=42, hover_color="#392E5E")
        self.longBreakBtn.place(x=520, y=390)

        #creating music switch and adding the music icon
        self.musicSwitch = tk.CTkSwitch(self, text="Music",
                                        variable=self.isMusicPlaying, onvalue="on", offvalue="off", bg_color="#160F37",
                                        button_color="#79747E", fg_color="#E6E0E9",
                                        switch_width=75, text_color="#160F37", switch_height=35,
                                        progress_color="#6750A4", command=musicControl, button_hover_color="#49454F")

        self.musicIcon = tk.CTkLabel(self,text_color="#160F37",image=CTkImage(light_image=Image.open("musicNote.png"),
                                                    size=(15,15)), width=2, height=5, fg_color="#E6E0E9",text="")
        self.musicIcon.place(x=650,y=24)
        self.musicSwitch.grid(row=0, column=2, pady=10, padx=(0,30))

        #creating task button and linking hover updates
        self.taskButton = tk.CTkButton(self,fg_color="#160F37", text="Tasks", bg_color="#160F37",height=25, width=25,
                                       image=CTkImage(light_image=Image.open("taskListButton.png"), size=(40,40)), hover_color="#160F37",
                                       command=lambda: openTasks(self))
        self.taskButton.grid(row=0,column=2, sticky="ne", pady=10)

        self.taskButton.bind("<Enter>", lambda hover: updateTaskButton(True))
        self.taskButton.bind("<Leave>",lambda hover: updateTaskButton(False))

        # function for user to set the mode manually based on input from the buttons
        def setMode(newMode):
            global currentMode, isTimerRunning
            currentMode = newMode

            #set the timer boolean to false
            isTimerRunning = False
            #upate start button GUIT when mode switches
            self.startBtn.configure(text="Start")

            #set the timer amount
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
            #play chime after a session ends
            mixer.Channel(0).play(mixer.Sound("chime.mp3"))
            #set the timer to not run
            isTimerRunning = False
            self.startBtn.configure(text="Start")
            if currentMode == "Focus":
                sessions += 1 #increment session counter
                if sessions == 4: # once four sessions are complete, long break starts
                    currentMode = "Long Break"
                    setTimer() #set timer for switched mode
                elif sessions < 4: #if focus session completed, and four sessions have not yet completed
                    currentMode = "Short Break"
            elif currentMode == "Long Break": #resetting counter at end of long break
                sessions = 0
                currentMode = "Focus"
            else:
                currentMode = "Focus" #if its a break mode, switch to focus mode

        setTimer()

        # countdown function created
        def countdownTimer():
            global timeRemaining, isTimerRunning
            global after_id
            #updates timer label based on countdown
            while timeRemaining != 0:
                self.timerDisplayTxt.set(
                    "{:02d}:{:02d}".format(timeRemaining // 60, timeRemaining % 60))  # update the timer display text
                self.update()  # updates the timer display
                if isTimerRunning:
                    timeRemaining -= 1
                after_id = self.after(1000) # using after() function to wait 1 second before updating

            # after timer ends, mode is switched and the timer is reset
            switchMode()
            setIndicator()
            setTimer()

        #run countdown timer
        countdownTimer()


#function to exit the program
def onExit():
    root.after_cancel(after_id)
    root.withdraw()
    root.quit()
    sys.exit()

if __name__ == '__main__':
    root = TimerApp()
    # add protocol to quit program when exit button clicked
    root.protocol("WM_DELETE_WINDOW", onExit)
    root.mainloop()


