import turtle as t

duke = t.Turtle()
sketch_board = t.Screen()
sketch_board.listen()


def move_forward():
    duke.forward(10)


def move_backward():
    duke.backward(10)


def turn_left():
    new_heading = duke.heading() + 10
    duke.setheading(new_heading)


def turn_right():
    new_heading = duke.heading() - 10
    duke.setheading(new_heading)


def clear():
    duke.clear()
    duke.penup()
    duke.home()
    duke.pendown()


sketch_board.onkey(move_forward, 'd')
sketch_board.onkey(move_backward, 'a')
sketch_board.onkey(turn_left, 'w')
sketch_board.onkey(turn_right, 's')
sketch_board.onkey(clear, 'c')

sketch_board.exitonclick()