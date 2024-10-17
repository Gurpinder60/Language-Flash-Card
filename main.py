from tkinter import *
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
df = {}
try:
    data = pd.read_csv("./data/words-to-learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    df = data.to_dict(orient="records")
else:
    df = data.to_dict(orient="records")

current_card = {}
flip_timer = None


def next_card():
    global current_card, flip_timer
    # Cancel the previous timer (if any) to avoid multiple flips happening
    if flip_timer:
        window.after_cancel(flip_timer)

    # Pick a new random card
    current_card = choice(df)

    # Update the card to show the French word
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    # Restart the timer for flipping the card after 3 seconds
    flip_timer = window.after(3000, flip_card)


def flip_card():
    # Update the card to show the English translation
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    global df
    df.remove(current_card)
    # Convert the list of dictionaries back to a DataFrame
    new_data = pd.DataFrame(df)

    # Save the updated data back to the 'words-to-learn.csv' file
    new_data.to_csv("./data/words-to-learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Setup the canvas for displaying the cards
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons for right and wrong
wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

# Start by showing the first card
next_card()

window.mainloop()
