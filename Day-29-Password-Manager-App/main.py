import tkinter as tk
from tkinter import messagebox
import random as rd
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [rd.choice(letters) for char in range(rd.randint(8, 10))]
    password_list.extend(rd.choice(symbols) for char in range(rd.randint(2, 4)))
    password_list.extend(rd.choice(numbers) for char in range(rd.randint(2, 4)))

    rd.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

    gen_password_button.config(state=tk.DISABLED)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title='Oops', message="Please don't leave any fields empty!")
    else:
        is_okay = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                         f"\nPassword: {password} \nIs it ok to save?")
        if is_okay:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password} \n ")
                website_entry.delete(0, last=len(website_entry.get()))
                # email_entry.delete(first=0, last=len(email_entry.get()))
                password_entry.delete(first=0, last=len(password_entry.get()))


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
tomato_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 94, image=tomato_img)
# canvas.pack()
canvas.grid(row=0, column=1)


website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = tk.Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)

email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = tk.Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "aaache27@colby.edu")

password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = tk.Entry(width=18)
password_entry.grid(row=3, column=1)

gen_password_button = tk.Button(text="Generate Password", command=generate_password)
gen_password_button.grid(row=3, column=2)

add_button = tk.Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()