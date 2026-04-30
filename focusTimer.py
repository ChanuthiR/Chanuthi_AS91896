import time

#initalize mode
currentMode = "Focus"


#initlizing timers for each mode in seconds
focusTime = 20
shortBreakTime = 5
longBreakTime = 10

#initalizing the session counter
sessions = 0

timeRemaining = 0 #initalizing time remaining variable
timerDisplay = "" # timer display text initalized

print("Timer started")

#logic to select timer amount to match the mode

def setTimer():
    global currentMode, timeRemaining
    if currentMode == "Focus":
        timeRemaining = focusTime
    elif currentMode == "Short Break":
        timeRemaining = shortBreakTime
    else:
        timeRemaining = longBreakTime

#logic to switch mode based on the previous mode and the number of sessions completed
def switchMode():
    global sessions, currentMode
    if sessions != 4:
        if currentMode == "Focus":
            currentMode = "Short Break"
        else:
            currentMode = "Focus"
    else:
        currentMode = longBreakTime
        sessions = 0
setTimer()

#countdown function created
while True:
    while timeRemaining>0:
        timerDisplay = "{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60) #format timer display so it appears as 00:00
        time.sleep(1)
        timeRemaining-=1
        print(timerDisplay)

    #after timer ends, mode is switched and the timer is reset
    switchMode()
    setTimer()


