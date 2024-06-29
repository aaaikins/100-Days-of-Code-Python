import turtle as t
import random as rd
import colorgram


def extraxt_images(filename, number_of_colors):
    rgb_colors = []
    colors = colorgram.extract(filename, number_of_colors)

    # Convert to tuple in rgb
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        new_color = (r, g, b)
        rgb_colors.append(new_color)

    return rgb_colors


# Convert colors from tuples to Hex
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


# Hirst Painting
def paint_hirst(number_of_dots, colors):

    colors = [rgb_to_hex(color) for color in colors]

    screen = t.Screen()
    # screen.screensize(640 * dots_per_line/4 , 400 * dots_per_line/4)

    dude = t.Turtle()
    dude.speed('fastest')
    dude.hideturtle()
    dude.penup()
    dude.setheading(225)
    dude.forward(325)
    dude.setheading(0)

    for dot_count in range(1, number_of_dots+1):
        dude.dot(20, rd.choice(colors))
        dude.penup()
        dude.forward(50)
        dude.pendown()

        if dot_count % 10 == 0:
            dude.penup()
            dude.setheading(90)
            dude.forward(50)
            dude.setheading(180)
            dude.forward(500)
            dude.setheading(0)

    screen.exitonclick()


colors = extraxt_images('image.jpg', 30)
paint_hirst(1000, colors)





