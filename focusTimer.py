import time

focusTime = 150  #time set for focus timer
timeRemaining = 0 #initalizing time remaining variable
timerDisplay = "" # timer display text initalized

print("Timer started")
timeRemaining = focusTime #setting the timer for the focus mode

#countdown function created
while timeRemaining>0:
    time.sleep(1)
    timeRemaining-=1

print("Timer ends")

