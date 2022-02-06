BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random

curr_card = {}
to_learn = {}

try:
    # reading from the file
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("swedish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # get all the words/translation rows out as a list of dictionaries
    # each dictionary contains a key swedish and the value is the word and key english and the value the word
    to_learn = data.to_dict(orient="records")
    # creating a new dictionary that represents the current card




# ---------------------------- FLASHCARD MECHANISM -------------------- #
# a function to get the next card in the game, we choose a random word from the swedish_words dictionary
def next_card():
    global curr_card, flip_timer
    # each time we at a new card we cancel the timer, because each card triggers a new timer
    window.after_cancel(flip_timer)
    # a random choice of a swedish word which is saved into current card dictionary
    # it helps us each time to get to the current card
    curr_card = random.choice(to_learn)
    # we show the swedish word
    canvas.itemconfig(leanguage_text, text="Swedish", fill="black")
    canvas.itemconfig(word_text, text=curr_card["swedish"], fill="black")
    # updating the background back to the front image, because next card should always be the front
    canvas.itemconfig(card_background, image=card_front_img)
    # each time we are at a new card we should flip it after 3 seconds
    flip_timer = window.after(3000, func=flip_card)

# a function to flip the card and show the english translation for the word
def flip_card():
    # changing the title to english
    canvas.itemconfig(leanguage_text, text="English", fill="white")
    # changing the word to english(translation from swedish)
    canvas.itemconfig(word_text, text=curr_card["english"], fill="white")
    # changing the background color
    canvas.itemconfig(card_background, image=card_back_img)

# this function updates the list of swedish words we need to learn
# it removes the word the user knows from the list by removing current card
def is_known():
    to_learn.remove(curr_card)
    # creating a new list which contains the words left for me to learn
    # in this way the original list of swedish words remain whole
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    # calling for next card
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
# creating a window
window = Tk()
# creating a title for the window
window.title("Flash Card")
window.config(padx = 50, pady = 50, bg=BACKGROUND_COLOR)
# after 3 seconds we flip the card
flip_timer = window.after(3000, func=flip_card)

# creating a canvas
canvas = Canvas(width=800, height=526)

# adding an image to the canvas
card_front_img = PhotoImage(file="card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_back_img = PhotoImage(file="card_back.png")

# adding a text to our canvas
leanguage_text = canvas.create_text(400, 150, text="Swedish", fill="black", font= ("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font= ("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness= 0)
# the image appears on our screen
canvas.grid(column=0, row=0, columnspan=2)


# creating a right button
vi_image = PhotoImage(file="right.png")
vi_button = Button(image=vi_image, highlightthickness= 0, command=is_known)
# placing the label
vi_button.grid(row=1, column=0)


# creating a wrong button
x_image = PhotoImage(file="wrong.png")
x_button = Button(image=x_image, highlightthickness= 0, command= next_card)
# placing the label
x_button.grid(row=1, column =1)

# generating the card
next_card()




window.mainloop()