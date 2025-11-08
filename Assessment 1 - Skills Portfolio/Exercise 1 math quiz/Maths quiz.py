# importing required modules
import tkinter as tk
from tkinter import ttk, messagebox
import random

# setting up colours for the UI
BG_COLOR = "#e9ecff"
BTN_COLOR = "#6C63FF"
BTN_TEXT = "white"
TITLE_COLOR = "#2C2C54"
TEXT_COLOR = "#333"
FRAME_COLOR = "#ffffff"

# function for showing a small loading animation before menu
def loading_bar(callback):
    clear_window()
    tk.Label(root, text="🔄 Loading...", font=("Arial", 18, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=100)
    progress = ttk.Progressbar(root, length=300, mode="determinate", maximum=100)
    progress.pack(pady=20)
    
    # slowly fill up the progress bar
    def fill_bar(value=0):
        if value <= 100:
            progress["value"] = value
            root.after(25, fill_bar, value + 2)
        else:
            callback()
    fill_bar()

# main menu for selecting difficulty level
def displayMenu():
    clear_window()
    tk.Label(root, text="🎯 Select Difficulty Level", font=("Arial", 18, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)
    levels = [("Easy (1-digit)", "easy"),
              ("Moderate (2-digit)", "moderate"),
              ("Advanced (4-digit)", "advanced")]
    # create a button for each level
    for text, level in levels:
        ttk.Button(root, text=text, style="Rounded.TButton",
                   command=lambda l=level: start_quiz(l)).pack(pady=10)

# function to generate random numbers based on selected difficulty
def randomInt(level):
    if level == "easy":
        return random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99)
    elif level == "advanced":
        return random.randint(1000, 9999)

# randomly decide whether question is addition or subtraction
def decideOperation():
    return random.choice(["+", "-"])

# function to show each maths question
def displayProblem():
    global num1, num2, operation, answer_entry, attempt, progress_bar
    clear_window()
    operation = decideOperation()
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    # make sure subtraction doesn’t go negative
    if operation == "-" and num1 < num2:
        num1, num2 = num2, num1
    attempt = 1

    tk.Label(root, text="🧮 Maths Quiz", font=("Arial", 20, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=10)
    tk.Label(root, text=f"Question {question_number}/10", font=("Arial", 14),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)

    # progress bar to show how many questions are done
    progress_bar = ttk.Progressbar(root, length=250, maximum=10, mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar["value"] = question_number - 1

    # show the questions
    tk.Label(root, text=f"{num1} {operation} {num2} =", font=("Arial", 26, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=10)

    # answer input box
    answer_entry = ttk.Entry(root, font=("Arial", 18), justify="center")
    answer_entry.pack(pady=10)
    answer_entry.focus()

    # button to check answer
    ttk.Button(root, text="Submit Answer", style="Rounded.TButton",
               command=check_answer).pack(pady=10)

# check if user’s answer is correct
def isCorrect(user_answer):
    return user_answer == (num1 + num2 if operation == "+" else num1 - num2)

# small visual effect for correct/wrong answers
def flash_color(color):
    root.config(bg=color)
    root.after(300, lambda: root.config(bg=BG_COLOR))

# function that checks user’s input and updates score
def check_answer():
    global score, question_number, attempt
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number.")
        return
    
    if isCorrect(user_answer):
        # first try gives 10 points, second try gives 5
        if attempt == 1:
            score += 10
            flash_color("#C8E6C9")
            messagebox.showinfo("Correct!", "✅ Correct! +10 points.")
        else:
            score += 5
            flash_color("#C8E6C9")
            messagebox.showinfo("Correct!", "✅ Correct (second try)! +5 points.")
        next_question()
    else:
        # wrong answer - allow retry once
        flash_color("#FFCDD2")
        if attempt == 1:
            attempt += 1
            messagebox.showinfo("Incorrect", "❌ Wrong! Try again.")
        else:
            messagebox.showinfo("Incorrect", "❌ Wrong again! Moving on.")
            next_question()


def next_question():
    global question_number
    question_number += 1
    if question_number > 10:
        displayResults()
    else:
        displayProblem()

# final screen showing score and rank
def displayResults():
    clear_window()
    if score >= 90:
        rank, emoji = "A+", "🏆"
    elif score >= 80:
        rank, emoji = "A", "👏"
    elif score >= 70:
        rank, emoji = "B", "👍"
    elif score >= 60:
        rank, emoji = "C", "🙂"
    else:
        rank, emoji = "Needs Improvement", "😅"

    tk.Label(root, text=f"{emoji} Quiz Complete!", font=("Arial", 22, "bold"),
             bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)
    tk.Label(root, text=f"Final Score: {score}/100", font=("Arial", 18),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
    tk.Label(root, text=f"Rank: {rank}", font=("Arial", 18),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    # buttons for replay or exit
    ttk.Button(root, text="Play Again", style="Rounded.TButton",
               command=lambda: loading_bar(displayMenu)).pack(pady=10)
    ttk.Button(root, text="Exit", style="Rounded.TButton",
               command=root.quit).pack(pady=5)

# starts the quiz and resets score
def start_quiz(level):
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 1
    displayProblem()


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# creating main window
root = tk.Tk()
root.title("🎲 Maths Quiz")
root.geometry("520x580")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')
root.config(bg=BG_COLOR)

# button and progress bar styling
style = ttk.Style()
style.theme_use("clam")
style.configure("Rounded.TButton",
                background=BTN_COLOR,
                foreground=BTN_TEXT,
                font=("Arial", 12, "bold"),
                borderwidth=0,
                focusthickness=3,
                focuscolor="none",
                padding=6)
style.map("Rounded.TButton", background=[("active", "#5146d9")])
style.configure("TProgressbar", troughcolor=BG_COLOR, background=BTN_COLOR)

# background design using canvas
canvas = tk.Canvas(root, width=520, height=580, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# create gradient-like background
for i in range(0, 580, 2):
    color = f"#{(233 - i//10):02x}{(236 - i//20):02x}{255:02x}"
    canvas.create_rectangle(0, i, 520, i+2, outline="", fill=color)

# small maths icons for decoration
icons = ["➕", "➖", "✖️", "➗", "√", "∑"]
for _ in range(30):
    x, y = random.randint(30, 480), random.randint(30, 540)
    canvas.create_text(x, y, text=random.choice(icons),
                       font=("Arial", 20, "bold"), fill="#d0d3ff", angle=random.randint(-25, 25))

# white box frame in the middle
canvas.create_rectangle(63, 143, 453, 523, outline="", fill="#cdd0ff")

frame = tk.Frame(root, bg=FRAME_COLOR, bd=0, highlightbackground="#b9bcff", highlightthickness=2)
canvas.create_window(260, 330, window=frame, width=380, height=370)

# main title and intro text
tk.Label(frame, text="🧮  Maths Quiz  🎯", font=("Arial", 26, "bold"),
         bg=FRAME_COLOR, fg=TITLE_COLOR).pack(pady=20)
tk.Label(frame, text="Sharpen your maths skills with fun problems!",
         font=("Arial", 12), bg=FRAME_COLOR, fg=TEXT_COLOR).pack(pady=5)
tk.Label(frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
         font=("Arial", 10), bg=FRAME_COLOR, fg="#aaa").pack(pady=10)

# start and exit buttons
ttk.Button(frame, text="Start Quiz", style="Rounded.TButton",
           command=lambda: loading_bar(displayMenu)).pack(pady=20)
ttk.Button(frame, text="Exit", style="Rounded.TButton",
           command=root.quit).pack(pady=5)

# run the main event loop
root.mainloop()
