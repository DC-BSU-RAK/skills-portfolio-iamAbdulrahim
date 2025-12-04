import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import pygame

# ---------------- SOUND SETUP ----------------
pygame.mixer.init()

# Load sounds
try:
    click_sound = pygame.mixer.Sound("click.mp3")
except:
    click_sound = None

try:
    laugh_sound = pygame.mixer.Sound("laugh.mp3")
except:
    laugh_sound = None

def play_click():
    if click_sound:
        click_sound.play()

def play_laugh():
    if laugh_sound:
        laugh_sound.play()

# ---------------- ANIMATIONS ----------------
def fade_in(widget, text, i=0):
    if i <= len(text):
        widget.config(text=text[:i])
        widget.after(20, lambda: fade_in(widget, text, i+1))

def glow_card():
    colors = ["#4a90e2", "#70a9f9", "#a6c6ff", "#ffffff"]
    def cycle(i=0):
        card.config(highlightbackground=colors[i], highlightcolor=colors[i])
        root.after(120, lambda: cycle((i + 1) % len(colors)))
    cycle()

def spawn_particle():
    emoji = random.choice(["😂", "🤣", "✨", "💫", "🌟"])
    x = random.randint(50, 550)
    y = 420
    lbl = tk.Label(root, text=emoji, font=("Segoe UI Emoji", 20), bg=root["bg"])
    lbl.place(x=x, y=y)
    def move(up=0):
        if up < 50:
            lbl.place(x=x, y=y - up)
            root.after(30, lambda: move(up + 2))
        else:
            lbl.destroy()
    move()
    root.after(500, spawn_particle)

# ---------------- JOKE FUNCTIONS ----------------
def load_jokes():
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "randomJokes.txt")
    if not os.path.exists(file_name):
        messagebox.showerror("Error", f"File not found: {file_name}")
        root.quit()
        return []

    jokes = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("?", 1)
            if len(parts) == 2:
                jokes.append((parts[0] + "?", parts[1].strip()))
    return jokes

def tell_joke():
    global current_joke
    play_click()
    if not jokes:
        fade_in(setup_label, "No jokes found!")
        return
    current_joke = random.choice(jokes)
    fade_in(setup_label, current_joke[0])
    punchline_label.config(text="")
    show_punchline_btn.config(state=tk.NORMAL)

def show_punchline():
    play_click()
    fade_in(punchline_label, current_joke[1])
    play_laugh()
    show_punchline_btn.config(state=tk.DISABLED)

def next_joke():
    play_click()
    tell_joke()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Alexa - Tell Me a Joke")
root.geometry("600x500")
root.resizable(False, False)

# Background image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_NAME = "background.jpg"  # <-- put your background image here
BG_PATH = os.path.join(BASE_DIR, BG_NAME)

try:
    bg_image = Image.open(BG_PATH)
    bg_image = bg_image.resize((600, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # keep reference!
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

except Exception as e:
    print("BACKGROUND ERROR:", e)
    messagebox.showerror("Error", f"Background image not found!\n{e}")
    root.config(bg="#d9e6fa")

# ---------------- CARD ----------------
card = tk.Frame(root, bg="white", padx=20, pady=20,
                bd=4, relief="ridge", highlightthickness=4)
card.place(relx=0.5, rely=0.52, anchor="center")

glow_card()

tk.Label(card, text="😂 Alexa, Tell Me a Joke 😂",
         font=("Segoe UI", 20, "bold"), bg="white").pack(pady=10)

setup_label = tk.Label(card, text="", wraplength=500,
                       font=("Segoe UI", 14), bg="white", justify="center")
setup_label.pack(pady=10)

punchline_label = tk.Label(card, text="", wraplength=500,
                           font=("Segoe UI", 14, "italic"),
                           fg="green", bg="white",
                           justify="center")
punchline_label.pack(pady=5)

# ---------------- BUTTONS ----------------
def styled_btn(text, cmd):
    return tk.Button(card, text=text, command=cmd,
                     font=("Segoe UI", 12, "bold"),
                     bg="#4a90e2", fg="white",
                     activebackground="#6aa8f7",
                     padx=20, pady=5, bd=3)

styled_btn("Alexa Tell Me a Joke", tell_joke).pack(pady=5)

show_punchline_btn = styled_btn("Show Punchline", show_punchline)
show_punchline_btn.pack(pady=5)
show_punchline_btn.config(state=tk.DISABLED)

styled_btn("Next Joke", next_joke).pack(pady=5)
styled_btn("Quit", root.quit).pack(pady=10)

# Load jokes
jokes = load_jokes()
current_joke = None

# Start emoji particles
spawn_particle()

root.mainloop()
