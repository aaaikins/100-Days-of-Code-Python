import tkinter as tk
import pandas as pd
import random as rd


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Load data
try:
    # Try to load the list of words to learn from words_to_learn.csv
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    # If not found, load the original list of French words
    original_data = pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # If words_to_learn.csv is found, use its data
    to_learn = data.to_dict(orient="records")


def next_card():
    """
    Display the next card from the list of words to learn.
    """
    global current_card, reveal_timer
    # Cancel the previous reveal timer if it exists
    window.after_cancel(reveal_timer)

    # Choose a random word from the list to learn
    current_card = rd.choice(to_learn)
    # Update the card to show the French word
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    # Set a timer to reveal the English translation after 5 seconds
    reveal_timer = window.after(5000, func=reveal_card)


def reveal_card():
    """
    Reveal the English translation of the current card.
    """
    # Update the card to show the English word
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    """
    Remove the known word from the list and update the CSV file.
    """
    # Remove the current card from the list of words to learn
    to_learn.remove(current_card)
    # Save the updated list to the CSV file
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    # Show the next card
    next_card()


def start_learning():
    """
    Start the flashcard learning process.
    """
    # Remove the start button
    start_button.grid_forget()
    # Show the first card
    next_card()


# Create the main window
window = tk.Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Set the initial reveal timer
reveal_timer = window.after(5000, func=reveal_card)

# Create a canvas to display the flashcard
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# Load images for the front and back of the card
card_front_img = tk.PhotoImage(file="./images/card_front.png")
card_back_img = tk.PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

# Add text to the card
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Load images for the buttons
cross_image = tk.PhotoImage(file="./images/wrong.png")
wrong_button = tk.Button(image=cross_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

check_image = tk.PhotoImage(file="./images/right.png")
right_button = tk.Button(image=check_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

# Create a start button
start_button = tk.Button(text="Start", font=("Ariel", 24, "bold"), command=start_learning)
start_button.grid(row=2, column=0, columnspan=2, pady=20)


# Run the main event loop
window.mainloop()
