import tkinter as tk
from tkinter import messagebox
import random as rd
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a random password and copy it to the clipboard."""
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
    window.update()

    gen_password_button.config(state=tk.DISABLED)

    pyperclip.copy(password)
    messagebox.showinfo(message="Password has been copied to clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Save the current password to a JSON file."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password}}

    if not website or not email or not password:
        messagebox.showwarning(title='Oops', message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                file_content = data_file.read()
                if file_content.strip():
                    data = json.loads(file_content)
                else:
                    data = {}
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError:
            data = {}

        data.update(new_data)
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        gen_password_button.config(state=tk.NORMAL)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    """Search for a saved password for the given website."""
    website = website_entry.get()
    try:
        with open("data.json", "r") as file:
            file_content = file.read()
            if not file_content.strip():
                raise json.JSONDecodeError("Empty file", file_content, 0)
            data = json.loads(file_content)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File Found")
    except json.JSONDecodeError:
        messagebox.showwarning(title="Error", message="Data file is empty or corrupted")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showwarning(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=250, height=250, highlightthickness=0)
tomato_img = tk.PhotoImage(file="logo.png")
canvas.create_image(125, 125, image=tomato_img)
# canvas.pack()
canvas.grid(row=0, column=1)


website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = tk.Entry(width=18)
website_entry.focus()
website_entry.grid(row=1, column=1)

search_button = tk.Button(text="Search", width=13, command=search)
search_button.grid(row=1, column=2)

email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = tk.Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@example.com")

password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = tk.Entry(width=18)
password_entry.grid(row=3, column=1)

gen_password_button = tk.Button(text="Generate Password", command=generate_password)
gen_password_button.grid(row=3, column=2)

add_button = tk.Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()