## Version two. Test mode.

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
    with open(filename, "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
        return [line.strip() for line in file]

word_list = load_word_list("words.txt")

main_contest_word_count = 70

main_contest_words = random.sample(word_list, main_contest_word_count)

current_word_idx = 0
user_answers = {}
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

def next_word(event=None):
    global current_word_idx, main_contest_score, pronounced
    if current_word_idx < main_contest_word_count:
        user_input = entry.get()
        user_answers[main_contest_words[current_word_idx]] = user_input
        if user_input == main_contest_words[current_word_idx]:
            main_contest_score += 1
        else:
            wrong_words.append((main_contest_words[current_word_idx], user_input))
        current_word_idx += 1
        pronounced = False
        update_display()

def pronounce_word(event=None):
    global pronounced
    if not pronounced:
        play_word(main_contest_words[current_word_idx])

def update_display():
    if current_word_idx < main_contest_word_count:
        progress_label.config(text=f"Word {current_word_idx + 1}/{main_contest_word_count}")
        entry.delete(0, tk.END)
    else:
        display_final_score()

def display_final_score():
    final_score_label.config(text=f"Main Contest Score: {main_contest_score}/{main_contest_word_count}")
    entry.config(state=tk.DISABLED)
    next_button.config(state=tk.DISABLED)
    display_wrong_words()

def display_wrong_words():
    if wrong_words:
        wrong_words_label.config(text="Incorrect Words:")
        for idx, (word, user_input) in enumerate(wrong_words):
            feedback = f"Word {idx + 1}: You entered '{user_input}', correct answer: '{word}'"
            incorrect_words_text.insert(tk.END, feedback + "\n")

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

wrong_words_label = ttk.Label(app, text="")
wrong_words_label.pack(pady=10)

incorrect_words_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
incorrect_words_text.pack(pady=10)

update_display()

play_word(main_contest_words[current_word_idx])

app.mainloop()
