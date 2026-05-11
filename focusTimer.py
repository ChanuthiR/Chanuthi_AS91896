import customtkinter as tk
#import string tkinter variable
from tkinter import StringVar

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

#initalize boolean variable of whether timer is running or paused
isTimerRunning = False

timeRemaining = 0 #initalizing time remaining variable
timerDisplayTxt = StringVar(root,value="00:00")# timer display text initalized as a Tkinter variable


#creating Timer Display label
timerDisplay = tk.CTkLabel(root, textvariable=timerDisplayTxt, text_color="#5DB69F", font=tk.CTkFont(family="Consolas", size=200),fg_color="#160F37")
timerDisplay.pack( )


#creating the start button with a hover effect and linking its functionality
def timerControl():
   global isTimerRunning
   isTimerRunning = not isTimerRunning
   if isTimerRunning == True:
       startBtn.configure(text="Pause")
       countdownTimer()
   else:
       startBtn.configure(text="Start")
       countdownTimer()

#function for user to set the mode manually based on input from the buttons
def setMode(newMode):
    global  currentMode, isTimerRunning
    currentMode = newMode
    isTimerRunning=False
    startBtn.configure(text="Start")
    setTimer()



startBtn = tk.CTkButton(root, text="Start", fg_color="#322952", bg_color= "#160F37", text_color="#FFFFFF", font=tk.CTkFont(family="Consolas",size=20), command=timerControl,border_spacing=10, corner_radius=20, width= 172, height=42,hover_color="#392E5E")
startBtn.pack()

#creating focus button
focusBtn = tk.CTkButton(root, text="Focus", fg_color="#2A2244", bg_color= "#160F37", text_color="#B776BB", command=lambda: setMode("Focus"), font=tk.CTkFont(family="Consolas",size=20),border_spacing=10, corner_radius=20, width= 172, height=42,hover_color="#392E5E")
focusBtn.pack()

#creating short break button
shortBreakBtn = tk.CTkButton(root, text="Short Break", fg_color="#2A2244", bg_color= "#160F37", text_color="#B776BB", command=lambda: setMode("Short Break"),font=tk.CTkFont(family="Consolas",size=20),border_spacing=10, corner_radius=20, width= 172, height=42,hover_color="#392E5E")
shortBreakBtn.pack()

#creating long break button
longBreakBtn = tk.CTkButton(root, text="Long Break", fg_color="#2A2244", bg_color= "#160F37", text_color="#B776BB",command=lambda : setMode("Long Break"), font=tk.CTkFont(family="Consolas",size=20),border_spacing=10, corner_radius=20, width= 172, height=42,hover_color="#392E5E")
longBreakBtn.pack()

#logic to select timer amount to match the mode, and changes the display colours of the mode buttons to showcase active mode
def setTimer():
   global currentMode, timeRemaining
   if currentMode == "Focus":
       focusBtn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")
       shortBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
       longBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
       timeRemaining = focusTime
   elif currentMode == "Short Break":
       timeRemaining = shortBreakTime
       focusBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
       shortBreakBtn.configure(fg_color="#744B77",text_color="#FFFFFF", hover_color="#905994")
       longBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
   elif currentMode == "Long Break":
       timeRemaining = longBreakTime
       focusBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
       shortBreakBtn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
       longBreakBtn.configure(fg_color="#744B77",text_color="#FFFFFF", hover_color="#905994")


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
def countdownTimer():
   global timeRemaining, timerDisplayTxt, isTimerRunning
   while timeRemaining!=0:
        timerDisplayTxt.set("{:02d}:{:02d}".format(timeRemaining//60, timeRemaining%60)) #update the timer display text
        root.update() #updates the timer display
        if isTimerRunning:
            timeRemaining -= 1
        root.after(1000) #using after() function to wait 1 second before updating

       #after timer ends, mode is switched and the timer is reset
   switchMode()
   setTimer()

countdownTimer()


root.mainloop()
