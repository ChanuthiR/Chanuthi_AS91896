import time
import tkinter as tk
#import font library
from tkinter import font

#initalize mode
currentMode = "Focus"

#initlizing timers for each mode in seconds
focusTime = 3
shortBreakTime = 1
longBreakTime = 2

#initalizing the session counter
sessions = 0

timeRemaining = 0 #initalizing time remaining variable
timerDisplayTxt = "" # timer display text initalized



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
    while timeRemaining!=0:
        timerDisplayTxt = "{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60) #format timer display so it appears as 00:00
        time.sleep(1)
        timeRemaining-=1
        print(timerDisplayTxt)

    #after timer ends, mode is switched and the timer is reset
    switchMode()
    setTimer()


