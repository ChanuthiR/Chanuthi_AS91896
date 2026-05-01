import time

#initalize mode
currentMode = "Focus"


#initlizing timers for each mode in seconds
focusTime = 10
shortBreakTime = 2
longBreakTime = 5

#initalizing the session counter
sessions = 0

timeRemaining = 0 #initalizing time remaining variable
timerDisplay = "" # timer display text initalized

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
            sessions += 1
            print("Session count: " + str(sessions)) #for testing that the session counter updates
        else:
            currentMode = "Focus"
    else:
        currentMode = "Long Break"
        sessions = 0



#countdown function created
while True:
    while timeRemaining!=0:
        timerDisplay = "{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60) #format timer display so it appears as 00:00
        time.sleep(1)
        timeRemaining-=1
        print(timerDisplay)

    #after timer ends, mode is switched and the timer is reset
    switchMode()
    setTimer()


