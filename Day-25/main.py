import turtle as t

import pandas
import pandas as pd

df = pd.read_csv("50_states.csv")
states = df.state.to_list()

screen = t.Screen()

screen.title("U.S. States Game")

image = "blank_states_img.gif"

screen.addshape(image)
t.shape(image)

answer_state = screen.textinput(title="Guess the State", prompt="What's another state's name?").title()

guessed_states = []
while len(guessed_states) < len(states):

    if answer_state == "Exit":
        missing_states = []
        for state in states:
            if state not in guessed_states:
                missing_states.append(state)
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

    if answer_state in states:
        turtle = t.Turtle()
        turtle.hideturtle()
        turtle.penup()
        state_data = df[df.state == answer_state]
        turtle.goto(int(state_data.x), int(state_data.y))
        turtle.write(answer_state)
        guessed_states.append(answer_state)
    answer_state = screen.textinput(title=f"{len(guessed_states)}/{len(df)} States Correct", prompt="What's another state's name?").title()



screen.mainloop()