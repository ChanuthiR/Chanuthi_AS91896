import time

#initalize mode
currentMode = "Focus"


#initlizing timers for each mode in seconds
focusTime = 1500
shortBreakTime = 300
longBreakTime = 600

#initalizing the session counter
sessions = 0

timeRemaining = 0 #initalizing time remaining variable
timerDisplay = "" # timer display text initalized

print("Timer started")

#logic to select timer amount to match the mode

def switchMode():
    if currentMode == "Focus":
        timeRemaining = focusTime
    elif currentMode == "Short Break":
        timeRemaining = shortBreakTime
    else:
        timeRemaining = longBreakTime

#countdown function created
while timeRemaining>0:
    timerDisplay = "{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60) #format timer display so it appears as 00:00
    time.sleep(1)
    timeRemaining-=1
    print(timerDisplay)

switchMode()

print("Timer ends")

