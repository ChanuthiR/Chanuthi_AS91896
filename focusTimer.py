#importing ctk for GUI
import customtkinter as tk


#import string tkinter variable and image library
from tkinter import StringVar
from PIL import Image
from customtkinter import CTkImage

#importing messagebox library
from tkinter import messagebox

#importing audio library
from pygame import mixer

#Import library for partial function for checkboxes
from functools import partial

#initalize mode
current_mode = "Focus"

#initlizing timer amounts for each mode in seconds
FOCUS_TIME = 5
SHORT_BREAK_TIME =3
LONG_BREAK_TIME = 10

#initalizing the session counter
sessions = 0

#initalize boolean variable of whether timer is running or paused
is_timer_running = False
# initializing time remaining variable
time_remaining = 0

#initilizing after id variable
after_id = None
# creating a list of tasks
tasks = []

MUSIC = "jazz.mp3"

# music switch variable
is_music_playing = None

class MusicSelectWindow(tk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("200x170")
        #ensure window cannot be resized
        self.resizable(False, False)
        self.title("Music Select")
        self.configure(fg_color="#160F37")

        # grid configuration
        self.grid_columnconfigure(0, weight=1)

        #ensure window stays on top of other windows
        self.wm_attributes("-topmost", 1)

        self.music_selected = tk.StringVar(value="jazz.mp3")

        self.music_label = tk.CTkLabel(self, fg_color="#160F37", text="Music Selection:", text_color="#FFFFFF",
                                      font=tk.CTkFont(family="Consolas", size=14))
        self.music_label.grid(column=0, row=0, sticky="e", padx=20)

        self.jazz_option = tk.CTkRadioButton(self, bg_color="#160F37", text_color="white", text="Jazz",variable=self.music_selected,
                                             value="jazz.mp3", fg_color="#5DB69F", command=self.update_music)
        self.lofi_option = tk.CTkRadioButton(self, bg_color="#160F37", text_color="white", text="Lofi", variable=self.music_selected,
                                            value="lofi.mp3", fg_color="#5DB69F", command=self.update_music)
        self.rain_option = tk.CTkRadioButton(self, bg_color="#160F37", text_color="white", text="Rain", variable=self.music_selected,
                                            value="rain.mp3", fg_color="#5DB69F", command=self.update_music)
        self.classical_option = tk.CTkRadioButton(self, bg_color="#160F37", text_color="white", text="Classical", variable=self.music_selected,
                                            value="classical.mp3", fg_color="#5DB69F", command=self.update_music)
        self.retro_option = tk.CTkRadioButton(self, bg_color="#160F37", text_color="white", text="Retro", variable=self.music_selected,
                                            value="retro.mp3", fg_color="#5DB69F", command=self.update_music)

        self.jazz_option.grid(column=0, row=1)
        self.lofi_option.grid(column=0, row=2)
        self.rain_option.grid(column=0, row=3)
        self.classical_option.grid(column=0, row=4)
        self.retro_option.grid(column=0, row=5)

    def update_music(self):
        global MUSIC, is_music_playing
        MUSIC = self.music_selected.get()
        is_music_playing.set(value="off")
        TimerApp.music_control(root)
        mixer.music.load(MUSIC)
        mixer.music.set_volume(0.2)


#creates task list frame that can scroll
class TaskList(tk.CTkScrollableFrame):
    def __init__(self, master, values):
        #configuration of task list frame with a single column and dark purple background
        super().__init__(master)
        self.configure(fg_color="#160F37")
        self.grid_columnconfigure((0), weight=1)

        #using the task list as an argument for the update function
        self.values = values
        self.update(self.values)


    #function to update checkbox and remove button display when selected and unselected
    def update_checkbox(self, task_no):
        if self.task_vars[task_no].get():
            # play chime when task is marked as done
            mixer.Channel(0).play(mixer.Sound("scribble.mp3"))
            self.task_checkboxes[task_no].configure(bg_color="#2A2244",text_color="#595E61", font=tk.CTkFont(family="Consolas", size=24, overstrike=True))
            self.remove_buttons[task_no].configure(fg_color="#2A2244",bg_color="#2A2244", hover_color="#2A2244")
        else:
            self.task_checkboxes[task_no].configure(bg_color="#744B77", text_color="#FFFFFF",
                                                  font=tk.CTkFont(family="Consolas", size=24, overstrike=False))
            self.remove_buttons[task_no].configure(fg_color="#744B77",bg_color="#744B77",hover_color="#744B77")

    #function to update the remove button depending on whether it is hovered over or not
    def update_remove_button(self, is_hovering, button_no, partial):
        if is_hovering:
            self.remove_buttons[button_no].configure(image=CTkImage(light_image=Image.open("removeTaskHover.png"), size=(20, 20)))
        else:
            self.remove_buttons[button_no].configure(image=CTkImage(light_image=Image.open("removetaskButton.png"), size=(20, 20)))

    def remove_task(self, task_no):
        #remove task from the task list
        tasks.pop(task_no)

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
        self.task_vars =[]

        #create list to hold the checkboxes and respective remove buttons
        self.task_checkboxes = []
        self.remove_buttons = []

        # iterating through the list of tasks to make a task tab for each
        for i, task in enumerate(values):
             # creating a task with a boolean variable to hold checkbox value
            self.task_done = tk.BooleanVar()
            self.task_vars.append(self.task_done)

            self.task = tk.CTkCheckBox(self, height=39, width=320,
                                           hover_color="#515658", bg_color="#744B77", text_color="#FFFFFF",
                                           border_color="#595E61", border_width=12,
                                           fg_color="#5DB69F", font=tk.CTkFont(family="Consolas", size=24),
                                           text=task, checkmark_color="#5DB69F",
                                       variable=self.task_vars[i],
                                       command=partial(self.update_checkbox, i))
            #ensuring the text, no matter the length is visible at a glance
            self.task._text_label.configure(wraplength=290)

            #update geometry manager
            self.task.update()

            #creating remove task button
            #getting the height of the task checkbox and matching it as the height of the remove button
            self.remove_task_button = tk.CTkButton(self, fg_color="#744B77", text="", bg_color="#744B77",height=self.task.winfo_reqheight(), width=10,
                                       image=CTkImage(light_image=Image.open("removeTaskButton.png"), size=(20,20)), hover_color="#744B77",
                                                 command=partial(TaskList.remove_task, self, i))

            # add the created remove button to the remove button array
            self.remove_buttons.append((self.remove_task_button))

            #bindings to have events when the button is hovered over and not hovered over
            self.remove_buttons[i].bind("<Enter>", partial(self.update_remove_button, True, i))
            self.remove_buttons[i].bind("<Leave>",  partial(self.update_remove_button, False, i))

            self.remove_buttons[i].grid(column=0,row=i,sticky="e")


            # place task in the grid, with each task placed one row below the previous task
            self.task.grid(column=0, row=i, pady=10, padx=20)

            #adding created checkbox to the array
            self.task_checkboxes.append(self.task)

        #ensuring task vars is visible to outer functions
        return self.task_vars



#creates task list window
class TaskWindow(tk.CTkToplevel):
    global tasks, is_music_playing
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

        #creating the task label in the top right corner
        self.task_label = tk.CTkLabel(self, fg_color="#160F37", text="Tasks", text_color="#FFFFFF", font= tk.CTkFont(family="Consolas", size= 24))
        self.task_label.grid(column=0,row=0,sticky="e", padx=20)

        #creating task variable
        self.tasks = tasks

        #placing the task list frame
        self.task_list_frame = TaskList(self, values=self.tasks)
        self.task_list_frame.grid(row=1, column=0, padx=10, sticky="nsew")

        #creating task input box
        self.task_input = tk.CTkEntry(self, width=291, height=39, fg_color="#D9D9D9",font=tk.CTkFont(family="Consolas", size= 20),
                                     placeholder_text="add new task", placeholder_text_color="#030000")
        self.task_input.grid(column=0,row=2, padx=10, pady=10)

        #updating add task button depending on if the user is hovering or not
        def update_add_button(is_hovering):
            if is_hovering:
                self.add_task_button.configure(image=CTkImage(light_image=Image.open("addTaskHover.png"), size=(40, 40)))
            else:
                self.add_task_button.configure(image=CTkImage(light_image=Image.open("addTaskButton.png"), size=(40, 40)))


        #function to add a task
        def addTask(event=0):
            #initalize the valid input variable to false
            self.valid_input = False

            #check if input contains an alphanumeric character
            for char in self.task_input.get():
                if char.isalnum():
                    self.valid_input = True

            #displaying relevant error messages based on validation checks
            if self.task_input.get()=="":
                messagebox.askretrycancel("Invalid Input","Input cannot be empty")
            elif self.valid_input==False:
                messagebox.askretrycancel("Invalid Input","Input should contain alphabet characters")
            else:
                #if tasks are valid add it to the list
                tasks.append(self.task_input.get())
                #update the task list frame
                TaskList.update(self.task_list_frame, values=self.tasks)
                #remove input from entry box
            self.task_input.delete(0,len(self.task_input.get()))

        #creating add task button
        self.add_task_button = tk.CTkButton(self,fg_color="#160F37", text="", bg_color="#160F37",height=25, width=25,
                                       image=CTkImage(light_image=Image.open("addTaskButton.png"), size=(40,40)),
                                          hover_color="#160F37", command=addTask)
        #adding binding for events for when the button is hovered over or not
        self.add_task_button.bind("<Enter>", lambda hover: update_add_button(True))
        self.add_task_button.bind("<Leave>", lambda hover: update_add_button(False))

        self.add_task_button.grid(column=0, row=2, padx=10, pady=10, sticky="e")



#creates timer app window
class TimerApp(tk.CTk):
    def __init__(self):
        super().__init__()
        global MUSIC, is_music_playing

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

        #protocol to ensure clear shutdown
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.timer_display_txt = StringVar(self, value="00:00")  # timer display text initialized as a Tkinter variable

        # creating Timer Display label
        self.timer_display = tk.CTkLabel(self, textvariable=self.timer_display_txt, text_color="#5DB69F",
                                        font=tk.CTkFont(family="Consolas", size=200), fg_color="#160F37")
        self.timer_display.grid(row=1, column=0, columnspan=3, sticky="ew")

        #set up player, volume, and load the music
        mixer.init()
        mixer.music.load(MUSIC)
        mixer.music.set_volume(0.3)

        is_music_playing = tk.StringVar(value="off")

        #creating indicators within a list
        self.indicators = []

        #ensures there is no task list visible when program starts
        self.task_window = None

        #function to control the timer and update the start button GUI
        def timer_control():
            global is_timer_running
            is_timer_running = not is_timer_running
            if is_timer_running == True:
                self.start_btn.configure(text="Pause")
                countdown_timer()
            else:
                self.start_btn.configure(text="Start")
                countdown_timer()

        #function to set session indicators
        def set_indicator():
            global sessions, current_mode
            for indicator in self.indicators:
                if sessions==4: #making session indicators invisible when sessions are complete
                    indicator.configure(fg_color="#160F37")
                    self.indicator_label.configure(text_color="#160F37")
                    self.indicator_label.configure(text="{}/4".format(sessions))
                elif sessions == 0: #resetting indicators after long break is completed
                    self.indicator_label.configure(text="{}/4".format(sessions))
                    indicator.configure(fg_color="#595E61")
                    self.indicator_label.configure(text_color="#5DB69F")
                else: #if session counter doesn't equal 4 or 0
                    for session in range(1,sessions+1): #counts sessions from 1-4
                        indicator = self.indicators[session-1] #changes color of indicators
                        # based on number of completed sessions
                        indicator.configure(fg_color= "#5DB69F")
                        self.indicator_label.configure(text="{}/4".format(sessions))
            #update indicator label
            self.indicator_label.update()

        #function to open task window
        def open_tasks(self):
            if self.task_window is None or not self.task_window.winfo_exists(): #checks if the task list window already exists or not
                self.task_window = TaskWindow()  # create window
            else:
                self.task_window.focus()  # if window exists focus it

        #function to open music window
        def open_music(event=0):
            if self.music_window is None or not self.music_window.winfo_exists():  # checks if the music list window already exists or not
                self.music_window = MusicSelectWindow()  # create window
            else:
                self.music_window.focus()  # if window exists focus it

        #function to update task button based on whether the button is in a hovering state or not
        def update_task_button(is_hovering):
            if is_hovering:
                self.task_button.configure(image=CTkImage(light_image=Image.open("taskListHover.png"), size=(40,40)))
            else:
                self.task_button.configure(image = CTkImage(light_image=Image.open("taskListButton.png"), size=(40, 40)))


        def explain(event=0):
            messagebox.showinfo("how to use",
                                "This timer uses the pomodoro method of following a focus session with a short break, "
                                "and if you complete four focus sessions, you earn a long break. "
                                "This indicator can be used to track your progress.")
        #creating four indicators using a for loop
        # and changing the x position for each so it shifts to the right for each indicator
        self.indicator_label = tk.CTkLabel(self, text="0/4",fg_color= "#160F37",width=15,
                                       height=15, bg_color="#160F37", font=tk.CTkFont(family="Consolas", size=20)
                                          , text_color="#5DB69F",cursor='hand2')

        #add event binding to showcase messagebox when indicator label clicked
        self.indicator_label.bind("<Button>", explain)


        #updating add task button depending on if the user is hovering or not
        def update_indicator_label(is_hovering):
            if is_hovering:
                self.indicator_label.configure(text_color="#8DCBBB")
            else:
                self.indicator_label.configure(text_color="#5DB69F")

        #adding hover effect to indicator label
        self.indicator_label.bind("<Enter>", lambda hover: update_indicator_label(True))
        self.indicator_label.bind("<Leave>", lambda hover: update_indicator_label(False))


        self.indicator_label.grid(row=0, column=0, sticky="w", pady=(10,24), padx=28)

        for x in range(1,5):
            self.indicator=tk.CTkLabel(self, text="",fg_color= "#595E61", corner_radius=15,width=15,
                                       height=15, bg_color="#160F37")
            self.indicator.grid(row=0,column=0,sticky="nw", pady=20, padx=(40+(30*x)))
            self.indicators.append(self.indicator)

        # creating the start button with a hover effect and linking its functionality
        self.start_btn = tk.CTkButton(self, text="Start", fg_color="#322952", bg_color="#160F37", text_color="#FFFFFF",
                                     font=tk.CTkFont(family="Consolas", size=20), command=timer_control,
                                     border_spacing=10,
                                     corner_radius=20, width=172, height=42, hover_color="#392E5E")
        self.start_btn.place(x=320, y=300)

        # creating focus button
        self.focus_btn = tk.CTkButton(self, text="Focus", fg_color="#2A2244", bg_color="#160F37", text_color="#B776BB",
                                     command=lambda: set_mode("Focus"), font=tk.CTkFont(family="Consolas", size=20),
                                     border_spacing=10, corner_radius=20, width=172, height=42, hover_color="#392E5E")
        self.focus_btn.place(x=120, y=390)

        # creating short break button
        self.short_break_btn = tk.CTkButton(self, text="Short Break", fg_color="#2A2244", bg_color="#160F37",
                                          text_color="#B776BB", command=lambda: set_mode("Short Break"),
                                          font=tk.CTkFont(family="Consolas", size=20), border_spacing=10,
                                          corner_radius=20,
                                          width=172, height=42, hover_color="#392E5E")
        self.short_break_btn.place(x=320, y=390)

        # creating long break button
        self.long_break_btn = tk.CTkButton(self, text="Long Break", fg_color="#2A2244", bg_color="#160F37",
                                         text_color="#B776BB", command=lambda: set_mode("Long Break"),
                                         font=tk.CTkFont(family="Consolas", size=20), border_spacing=10,
                                         corner_radius=20,
                                         width=172, height=42, hover_color="#392E5E")
        self.long_break_btn.place(x=520, y=390)

        #creating music switch and adding the music icon
        self.music_switch = tk.CTkSwitch(self, text="Music",
                                        variable=is_music_playing, onvalue="on", offvalue="off", bg_color="#160F37",
                                        button_color="#79747E", fg_color="#E6E0E9",
                                        switch_width=75, text_color="#160F37", switch_height=35,
                                        progress_color="#6750A4", command=self.music_control, button_hover_color="#49454F")

        self.music_icon = tk.CTkLabel(self,text_color="#160F37",image=CTkImage(light_image=Image.open("musicNote.png"),
                                                    size=(15,15)), width=2, height=5, fg_color="#E6E0E9",text="")

        # add event binding to open music window when music icon clicked
        self.music_icon.bind("<Button>", open_music)


        #updating add task button depending on if the user is hovering or not
        def update_music_icon(is_hovering):
            if is_hovering:
                self.music_icon.configure(image=CTkImage(light_image=Image.open("musicNoteHover.png"),size=(15,15)))
            else:
                self.music_icon.configure(image=CTkImage(light_image=Image.open("musicNote.png"),size=(15,15)))

        #adding hover effect to indicator label
        self.music_icon.bind("<Enter>", lambda hover: update_music_icon(True))
        self.music_icon.bind("<Leave>", lambda hover: update_music_icon(False))

        self.music_icon.place(x=650,y=24)
        self.music_switch.grid(row=0, column=2, pady=10, padx=(0,30))

        #creating task button and linking hover updates
        self.task_button = tk.CTkButton(self,fg_color="#160F37", text="Tasks", bg_color="#160F37",height=25, width=25,
                                       image=CTkImage(light_image=Image.open("taskListButton.png"), size=(40,40)), hover_color="#160F37",
                                       command=lambda: open_tasks(self))
        self.task_button.grid(row=0,column=2, sticky="ne", pady=10)

        self.task_button.bind("<Enter>", lambda hover: update_task_button(True))
        self.task_button.bind("<Leave>",lambda hover: update_task_button(False))

        self.music_window = None


        # function for user to set the mode manually based on input from the buttons
        def set_mode(new_mode):
            global current_mode, is_timer_running
            current_mode = new_mode

            #set the timer boolean to false
            is_timer_running = False
            #upate start button GUIT when mode switches
            self.start_btn.configure(text="Start")

            #set the timer amount
            set_timer()


        # logic to select timer amount to match the mode, and changes the display colours of the mode buttons to showcase active mode
        def set_timer():
            global current_mode, time_remaining
            if current_mode == "Focus":
                self.focus_btn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")
                self.short_break_btn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.long_break_btn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                time_remaining = FOCUS_TIME
            elif current_mode == "Short Break":
                time_remaining = SHORT_BREAK_TIME
                self.focus_btn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.short_break_btn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")
                self.long_break_btn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
            elif current_mode == "Long Break":
                time_remaining = LONG_BREAK_TIME
                self.focus_btn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.short_break_btn.configure(fg_color="#2A2244", text_color="#B776BB", hover_color="#392E5E")
                self.long_break_btn.configure(fg_color="#744B77", text_color="#FFFFFF", hover_color="#905994")
            self.timer_display_txt.set(
                "{:02d}:{:02d}".format(time_remaining // 60, time_remaining % 60))  # update the timer display text

        # logic to switch mode based on the previous mode and the number of sessions completed
        def switch_mode():
            global sessions, current_mode, is_timer_running
            #play chime after a session ends
            mixer.Channel(0).play(mixer.Sound("chime.mp3"))
            #set the timer to not run
            is_timer_running = False
            self.start_btn.configure(text="Start")
            if current_mode == "Focus":
                sessions += 1 #increment session counter
                if sessions == 4: # once four sessions are complete, long break starts
                    current_mode = "Long Break"
                    set_timer() #set timer for switched mode
                elif sessions < 4: #if focus session completed, and four sessions have not yet completed
                    current_mode = "Short Break"
            elif current_mode == "Long Break": #resetting counter at end of long break
                sessions = 0
                current_mode = "Focus"
            else:
                current_mode = "Focus" #if it is a break mode, switch to focus mode

        set_timer()

        # countdown function created
        def countdown_timer():
            global time_remaining, is_timer_running, after_id
            #updates timer label based on countdown
            if is_timer_running==False:
                return
            elif time_remaining != 0:
                self.timer_display_txt.set(
                    "{:02d}:{:02d}".format(time_remaining // 60, time_remaining % 60))  # update the timer display text
                self.update()  # updates the timer display
                time_remaining -= 1
                after_id = self.after(1000, countdown_timer)
            else:
                self.after_cancel(after_id)
                # after timer ends, mode is switched and the timer is reset
                switch_mode()
                set_indicator()
                set_timer()

        #run countdown timer
        countdown_timer()

        #function  to change the button colour after music switch is on
        #plays the music when switch is on and stops music when switch is not on
    def music_control(self):
            global is_music_playing
            if is_music_playing.get() == "on":
                mixer.music.play(-1)
                self.music_switch.configure(button_color="white", button_hover_color="#EADDFF")
                self.music_icon.configure(fg_color="white")
            else:
                mixer.music.pause()
                self.music_switch.configure(button_color="#79747E", button_hover_color="#49454F")
                self.music_icon.configure(fg_color="#E6E0E9")


#calling the TimerApp
if __name__ == '__main__':
    root = TimerApp()
    root.mainloop()


