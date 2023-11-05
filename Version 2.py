## Version 2

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import random
from gtts import gTTS
import os
import pygame
import tempfile
import time

def set_app_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel")
    style.configure("TButton")
    style.configure("TEntry", background="white", foreground="black")
    style.configure("TScrolledtext", foreground="black")
    app.configure(bg="#2c3e50")

def load_word_list(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]

word_list = load_word_list("words.txt")

main_contest_word_count = 70

main_contest_words = random.sample(word_list, main_contest_word_count)

current_word_idx = 0
main_contest_score = 0
pronounced = False
wrong_words = []

pygame.mixer.init()

def play_word(current_word):
    tts = gTTS(text=current_word, lang='en')
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    temp_file.close()
    tts.save(temp_file.name)
    pygame.mixer.music.load(temp_file.name)
    pygame.mixer.music.play()
    time.sleep(2)
    try:
        os.remove(temp_file.name)
    except PermissionError:
        pass

def check_word(user_input):
    if current_word_idx < main_contest_word_count:
        if user_input.strip().lower() == main_contest_words[current_word_idx].lower():
            return True
        else:
            wrong_words.append(main_contest_words[current_word_idx])
    return False

def next_word(event=None):
    global current_word_idx, main_contest_score, pronounced

    user_input = entry.get()

    if check_word(user_input):
        main_contest_score += 1
        wrong_words.clear()
    else:
        pronounced = False
        update_display()
        return

    current_word_idx += 1
    update_display()

def pronounce_word(event=None):
    global pronounced
    if not pronounced:
        play_word(main_contest_words[current_word_idx])

def update_display():
    if current_word_idx < main_contest_word_count:
        if wrong_words:
            feedback = f"Word {current_word_idx + 1}: Incorrect. Correct answer: '{main_contest_words[current_word_idx]}'"
            incorrect_words_text.insert(tk.END, feedback + "\n")
            entry.delete(0, tk.END)
        else:
            entry.delete(0, tk.END)
            incorrect_words_text.delete(1.0, tk.END)
        progress_label.config(text=f"Word {current_word_idx + 1}/{main_contest_word_count}")
    else:
        display_final_score()

def display_final_score():
    final_score_label.config(text=f"Main Contest Score: {main_contest_score}/{main_contest_word_count}")
    entry.config(state=tk.DISABLED)
    next_button.config(state=tk.DISABLED)

app = tk.Tk()
app.title("Spelling UIL Practice Test")
app.geometry("800x600")

set_app_style()

word_label = ttk.Label(app, text="Spelling Contest")
word_label.pack(pady=20)

progress_label = ttk.Label(app, text=f"Word 1/{main_contest_word_count}")
progress_label.pack(pady=10)

entry = ttk.Entry(app)
entry.pack(pady=10)

next_button = ttk.Button(app, text="Next Word", command=next_word)
next_button.pack(pady=10)

entry.bind('<Return>', next_word)
entry.bind('<Shift-Return>', pronounce_word)

final_score_label = ttk.Label(app, text="")
final_score_label.pack(pady=20)

incorrect_words_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
incorrect_words_text.pack(pady=10)

update_display()

play_word(main_contest_words[current_word_idx])

app.mainloop()
