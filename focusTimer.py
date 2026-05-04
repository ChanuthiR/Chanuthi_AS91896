import time
import tkinter as tk
#import font library
from tkinter import font

#initalize mode
currentMode = "Focus"

#initalize window with name and make it fullscreen and the background color purple
root = tk.Tk(screenName="Focus Timer", baseName="Productivity")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.geometry("%dx%d" % (width,height))

root.title("Productivity")

root.config(background="#160F37")

#initlizing timers for each mode in seconds
focusTime = 3
shortBreakTime = 1
longBreakTime = 2

#initalizing the session counter
sessions = 0

timeRemaining = 0 #initalizing time remaining variable
timerDisplayTxt = "00:00" # timer display text initalized

#creating Timer Display label
timerDisplay = tk.Label(text=timerDisplayTxt, fg="#5DB69F", font=font.Font(family="Consolas", size=100),bg="#160F37")
timerDisplay.grid(row=2,column=1,padx=10,pady=10)

startBtn = tk.Button(text="Start",bg="#322952", fg="#FFFFFF",activebackground="#392E5E", activeforeground="#FFFFFF",relief=tk.FLAT, width=10, height=2)
startBtn.grid(row=3,column=1,pady=10,padx=10)


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
        timerDisplay.config(text=timerDisplayTxt)
        timerDisplayTxt = "{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60) #format timer display so it appears as 00:00
        time.sleep(1)
        timeRemaining-=1
        print(timerDisplayTxt)

    #after timer ends, mode is switched and the timer is reset
    switchMode()
    setTimer()


