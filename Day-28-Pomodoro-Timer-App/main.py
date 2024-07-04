import math
import tkinter as tk
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
is_paused = False
remaining_time = 0


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, is_paused, remaining_time, timer
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    check_mark_label.config(text="")
    start_button.config(state=tk.NORMAL)  # Re-enable the start button
    reps = 0
    is_paused = False
    remaining_time = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, is_paused, remaining_time
    if is_paused:
        count_down(remaining_time)
        is_paused = False
    else:
        reps += 1
        start_button.config(state=tk.DISABLED)

        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 8 == 0:
            count_down(long_break_sec)
            timer_label.config(text="Long Break", fg=RED, bg=YELLOW)
            window.title("Time for a break!")
        elif reps % 2 == 0:
            count_down(short_break_sec)
            timer_label.config(text="Short Break", fg=PINK, bg=YELLOW)
            window.title("Time for a break!")
        else:
            count_down(work_sec)
            timer_label.config(text="Work", fg=GREEN, bg=YELLOW)
            window.title("Time to focus!")


# ---------------------------- UPDATE CHECK MARKS ------------------------------- #
def update_check_marks():
    check_marks = ""
    work_sessions = math.floor(reps / 2)
    for _ in range(work_sessions):
        check_marks += "✔"
    check_mark_label.config(text=check_marks)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, remaining_time
    remaining_time = count

    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'

    canvas.itemconfig(timer_text, text= f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)

    else:

        start_timer()
        update_check_marks()


# ---------------------------- PAUSE MECHANISM ------------------------------- #
def pause_timer():
    global is_paused, timer
    if not is_paused and timer:
        window.after_cancel(timer)
        is_paused = True
        start_button.config(state=tk.NORMAL)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
timer_label.grid(row=0, column=1)


canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)


start_button = tk.Button(text="Start", command=start_timer, bg=YELLOW, highlightthickness= 0)
start_button.grid(row=2, column=0)

pause_button = tk.Button(text="Pause", command=pause_timer, bg=YELLOW, highlightthickness=0)
pause_button.grid(row=4, column=1)

reset_button = tk.Button(text="Reset", command=reset_timer, bg=YELLOW, highlightthickness=0)
reset_button.grid(row=2, column=2)

check_mark_label = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))
check_mark_label.grid(row=3, column=1)

window.mainloop()
