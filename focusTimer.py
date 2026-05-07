import time
import customtkinter as tk
#import font library
from tkinter import font, StringVar

#initalize mode
currentMode = "Focus"

#initalize window with name and make it fullscreen and the background color purple
root = tk.CTk(screenName="Focus Timer", baseName="Productivity")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.geometry("%dx%d" % (width,height))

root.title("Productivity")

root.config(background="#160F37")

#initlizing timers for each mode in seconds
focusTime = 25*60
shortBreakTime = 5*60
longBreakTime = 10*60

#initalizing the session counter
sessions = 0

timeRemaining = 0 #initalizing time remaining variable
timeRunning = ""
timerDisplayTxt = StringVar(root,value="00:00")# timer display text initalized as a Tkinter variable

#creating Timer Display label
timerDisplay = tk.CTkLabel(root, textvariable=timerDisplayTxt, text_color="#5DB69F", font=tk.CTkFont(family="Consolas", size=200),fg_color="#160F37")
timerDisplay.pack()

startBtn = tk.CTkButton(root, text="Start", fg_color="#322952", text_color="#FFFFFF", font=tk.CTkFont(family="Consolas",size=20), border_spacing=10, hover_color="#392E5E", width=10, height=2,corner_radius=1000)
startBtn.pack()


#logic to select timer amount to match the mode
def setTimer():
    global currentMode, timeRemaining
    if currentMode == "Focus":
        timeRemaining = focusTime
    elif currentMode == "Short Break":
        timeRemaining = shortBreakTime
    elif currentMode == "Long Break":
        timeRemaining = longBreakTime

#logic to switch mode based on the previous mode and the number of sessions completed
def switchMode():
    global sessions, currentMode
    if currentMode == "Focus":
        sessions += 1
        if sessions == 4: #once four sessions are complete, long break starts
            currentMode = "Long Break"
            setTimer()
            sessions = 0
        elif sessions<4:
            currentMode = "Short Break"
            print("Session count: " + str(sessions)) #for testing that the session counter updates
    else:
        currentMode = "Focus"

setTimer()

#countdown function created
while True:
    root.mainloop()
    while timeRemaining!=0:
        timeRunning = "{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60)
        timerDisplayTxt.set(timeRunning)#format timer display so it appears as XX:XX
        time.sleep(1)
        timeRemaining-=1
    #after timer ends, mode is switched and the timer is reset
    switchMode()
    setTimer()


