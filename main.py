import customtkinter as ctk
from pygame import mixer
from random import choice

app = ctk.CTk()
app.title('CTk_Simon')
w = app.winfo_screenwidth()
h = app.winfo_screenheight()
app.geometry(f'{int(w/1.25)}x{int(h/1.25)}')

ctk.set_appearance_mode('dark')
mixer.init()

# Variables
button_array = ['button_tl',
                'button_tm',
                'button_tr',
                'button_ml',
                'button_mm',
                'button_mr',
                'button_bl',
                'button_bm',
                'button_br']
pattern = []
button_clicks = 0
score = 0
end_sound = mixer.Sound('Sounds/game_over.mp3')
beep_0 = mixer.Sound('Sounds/beep_01.mp3')
beep_1 = mixer.Sound('Sounds/beep_02.mp3')
beep_2 = mixer.Sound('Sounds/beep_03.mp3')
beep_3 = mixer.Sound('Sounds/beep_04.mp3')
beep_4 = mixer.Sound('Sounds/beep_05.mp3')
beep_5 = mixer.Sound('Sounds/beep_06.mp3')
beep_6 = mixer.Sound('Sounds/beep_07.mp3')
beep_7 = mixer.Sound('Sounds/beep_08.mp3')
beep_8 = mixer.Sound('Sounds/beep_09.mp3')

# App Widgets
top_label = ctk.CTkLabel(master=app, text='CTk Simon', text_color='white', font=('Arial', 40, 'bold'))
top_label.pack()
score_frame = ctk.CTkFrame(master=app, fg_color='transparent', height=25)
score_frame.pack()
game_frame = ctk.CTkFrame(master=app, fg_color='transparent', width=w/3, height=h/2)
game_frame.pack()
button_frame = ctk.CTkFrame(master=app, fg_color='transparent', width=w/3)
button_frame.pack(pady=10)

# Score Frame Widgets
game_label = ctk.CTkLabel(master=score_frame, text="Press Start to Play", text_color='lightsteelblue',
                          font=('Arial', 20, 'bold'))
game_label.pack(side='left', padx=40)
score_label = ctk.CTkLabel(master=score_frame, text=f'Score: {score}', text_color='lightcoral',
                           font=('Arial', 20, 'bold'))
score_label.pack(side='right', padx=40)

# Button Function
def button_click(button_pressed):
    global score
    global button_clicks
    button_index = button_array.index(button_pressed)
    beep = eval('beep_' + str(button_index))
    beep.set_volume(.25)
    mixer.Sound.play(beep)
    if (button_clicks + 1) != len(pattern):
        if button_pressed == pattern[button_clicks]:
            button_clicks += 1
        else:
            lose_condition(pattern[(button_clicks)])
    else:
        if button_pressed == pattern[button_clicks]:
            score += 1
            score_label.configure(text=f"Score: {score}")
            button_clicks = 0
            disable_buttons()
            game_frame.after(100, disable_hover())
            create_pattern()
            flash_buttons()
        else:
            lose_condition(pattern[-1])

# Buttons
button_tl = ctk.CTkButton(master=game_frame, fg_color='darkred', hover_color='#FF0000', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_tl': button_click(v))
button_tl.grid(row=0, column=0, padx=10, pady=10)
button_tm = ctk.CTkButton(master=game_frame, fg_color='#890596', hover_color='#F511F5', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_tm': button_click(v))
button_tm.grid(row=0, column=1, padx=10, pady=10)
button_tr = ctk.CTkButton(master=game_frame, fg_color='darkblue', hover_color='#0000FF', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_tr': button_click(v))
button_tr.grid(row=0, column=2,padx=10, pady=10)
button_ml = ctk.CTkButton(master=game_frame, fg_color='#C57635', hover_color='#FFAA00', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_ml': button_click(v))
button_ml.grid(row=1, column=0, padx=10, pady=10)
button_mm = ctk.CTkButton(master=game_frame, fg_color='#2392AF', hover_color='#00FFFF', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_mm': button_click(v))
button_mm.grid(row=1, column=1, padx=10, pady=10)
button_mr = ctk.CTkButton(master=game_frame, fg_color='#3F2305', hover_color='#785530', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_mr': button_click(v))
button_mr.grid(row=1, column=2,padx=10, pady=10)
button_bl = ctk.CTkButton(master=game_frame, fg_color='darkgreen', hover_color='#00FF00', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_bl': button_click(v))
button_bl.grid(row=2, column=0, padx=10, pady=10)
button_bm = ctk.CTkButton(master=game_frame, fg_color='#AF1171', hover_color='#FF6FA1', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_bm': button_click(v))
button_bm.grid(row=2, column=1, padx=10, pady=10)
button_br = ctk.CTkButton(master=game_frame, fg_color='#B0AB00', hover_color='#FFFF00', text=None, height=h/6,
                          border_width=2, border_color='gray', width=w/10, corner_radius=45,
                          command=lambda v='button_br': button_click(v))
button_br.grid(row=2, column=2, padx=10, pady=10)

# Disable Buttons on Program Start
def disable_buttons():
    for button in button_array:
        eval(button).configure(state='disabled')

# Game Functions
def create_pattern():
    r_button = choice(button_array)
    pattern.append(r_button)

def flash_buttons():
    for button in pattern:
        button_index = button_array.index(button)
        beep = eval('beep_' + str(button_index))
        beep.set_volume(.25)
        color = eval(button).cget('fg_color')
        flash_color = eval(button).cget('hover_color')
        eval(button).configure(fg_color=color)
        game_frame.after(250, game_frame.update())
        mixer.Sound.play(beep)
        eval(button).configure(fg_color=flash_color)
        game_frame.after(200, game_frame.update())
        eval(button).configure(fg_color=color)
        game_frame.after(200, game_frame.update())
    enable_buttons()
    enable_hover()

def start():
    global score
    game_label.configure(text='Follow the Pattern!')
    pattern.clear()
    score = score - score
    score_label.configure(text=f"Score: {score}")
    start_button.configure(state='disabled')
    create_pattern()
    flash_buttons()
    enable_buttons()

def lose_condition(button):
    mixer.Sound.play(end_sound)
    game_label.configure(text='GAME OVER')
    global button_clicks
    disable_buttons()
    color = eval(button).cget('fg_color')
    flash_color = eval(button).cget('hover_color')
    for num in range(5):
        eval(button).configure(fg_color=flash_color)
        game_frame.after(150, game_frame.update())
        eval(button).configure(fg_color=color)
        game_frame.after(150, game_frame.update())
    start_button.configure(state='normal')
    button_clicks = 0

def enable_buttons():
    for button in button_array:
        eval(button).configure(state='normal')

def disable_hover():
    for button in button_array:
        eval(button).configure(hover=False)

def enable_hover():
    for button in button_array:
        eval(button).configure(hover=True)

def quit():
    app.destroy()

# Bottom Buttons
start_button = ctk.CTkButton(master=button_frame, text='Start', fg_color='green', height=30, width=30,
                               corner_radius=30, hover_color='darkgreen', font=('Arial', 20), command=start)
start_button.pack(side='left', padx=25)
quit_button = ctk.CTkButton(master=button_frame, text='Quit', fg_color='red', height=30, width=30, corner_radius=30,
                            hover_color='darkred', font=('Arial', 20), command=quit)
quit_button.pack(side='right', padx=25)

# Start
disable_buttons()
app.mainloop()