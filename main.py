# Study Mode

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import random
from gtts import gTTS
import os
import pygame
import tempfile
import time
import pyttsx3

def set_app_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel")
    style.configure("TButton")
    style.configure("TEntry", background="white", foreground="black")
    style.configure("TScrolledtext", foreground="black")
    app.configure(bg="#2c3e50")

def load_word_list(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]

word_list = load_word_list("words.txt")

main_contest_words = []  # Initialize main_contest_words as a global list

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust the speaking rate as needed

def select_words(start_index, end_index, num_words=70):
    if 1 <= start_index <= end_index <= len(word_list):
        selected_words = word_list[start_index - 1:end_index]
        random.shuffle(selected_words)
        return selected_words[:num_words]
    else:
        return []

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

# Initialize main contest variables
current_word_idx = 0
pronounced = False
wrong_words = []

pygame.mixer.init()

def check_word(user_input):
    if current_word_idx < len(main_contest_words):
        if user_input.strip().lower() == main_contest_words[current_word_idx].lower():
            return True
        else:
            wrong_words.append(main_contest_words[current_word_idx])
    return False

def next_word(event=None):
    global current_word_idx, pronounced

    user_input = entry.get()

    if check_word(user_input):
        wrong_words.clear()
    else:
        pronounced = False
        update_display()
        return

    current_word_idx += 1
    update_display()
    play_word(main_contest_words[current_word_idx])

def pronounce_word(event=None):
    global pronounced
    if not pronounced:
        play_word(main_contest_words[current_word_idx])

def alt_pronunciation(event=None):
    engine.setProperty("voice", "com.apple.speech.synthesis.voice.Agnes")
    engine.say(main_contest_words[current_word_idx])
    engine.runAndWait()
    pronounced = True

def update_display():
    if current_word_idx < len(main_contest_words):
        if wrong_words:
            feedback = f"Word {current_word_idx + 1}: Incorrect. Correct answer: '{main_contest_words[current_word_idx]}'"
            incorrect_words_text.insert(tk.END, feedback + "\n")
            entry.delete(0, tk.END)
        else:
            entry.delete(0, tk.END)
            incorrect_words_text.delete(1.0, tk.END)
        progress_label.config(text=f"Word {current_word_idx + 1}/{len(main_contest_words)}")
        score_label.config(text=f"Score: {current_word_idx}/{70}")
    else:
        entry.config(state=tk.DISABLED)
        next_button.config(state=tk.DISABLED)

def start_contest():
    start_index = int(start_entry.get())
    end_index = int(end_entry.get())
    global main_contest_words, current_word_idx, pronounced, wrong_words
    main_contest_words = select_words(start_index, end_index, num_words=70)
    if main_contest_words:
        entry.config(state=tk.NORMAL)
        next_button.config(state=tk.NORMAL)
        current_word_idx = 0
        pronounced = False
        wrong_words.clear()
        progress_label.config(text=f"Word 1/{len(main_contest_words)}")
        entry.delete(0, tk.END)
        incorrect_words_text.delete(1.0, tk.END)
        update_display()
        play_word(main_contest_words[current_word_idx])

app = tk.Tk()
app.title("Spelling UIL Practice Test")
app.geometry("800x600")

set_app_style()

word_label = ttk.Label(app, text="Spelling Contest")
word_label.pack(pady=20)

start_label = ttk.Label(app, text="Start Index:")
start_label.pack()
start_entry = ttk.Entry(app)
start_entry.pack()

end_label = ttk.Label(app, text="End Index:")
end_label.pack()
end_entry = ttk.Entry(app)
end_entry.pack()

start_button = ttk.Button(app, text="Start Contest", command=start_contest)
start_button.pack(pady=10)

progress_label = ttk.Label(app, text="")
progress_label.pack(pady=10)

entry = ttk.Entry(app)
entry.pack(pady=10)
entry.config(state=tk.DISABLED)

next_button = ttk.Button(app, text="Next Word", command=next_word)
next_button.pack(pady=10)
next_button.config(state=tk.DISABLED)

entry.bind('<Return>', next_word)
entry.bind('<Shift-Return>', pronounce_word)
entry.bind('<Alt-Return>', alt_pronunciation)

score_label = ttk.Label(app, text="Score: 0/70")
score_label.pack()

incorrect_words_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
incorrect_words_text.pack(pady=10)

update_display()

app.mainloop()
