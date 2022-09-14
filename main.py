from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- Search Function ------------------------------ #


def search():
    website = website_entry.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            password = data[website]["password"]
            email = data[website]["username"]
    except FileNotFoundError:
        print("File not Found")
        messagebox.showwarning("Oops", "File is not created yet, try adding a website & password first.")
    except KeyError:
        print("key not found")
        messagebox.showwarning("Error", f"You do not currently have any saved data for {website}")
    else:
        messagebox.showinfo(website, f"{website}\nUsername: {email},\n Password: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_user_info():

    username = username_entry.get()
    password = password_entry.get()
    website = website_entry.get()
    new_data = {
         website: {
             "username": username,
             "password": password,
         }
    }

    if len(username) == 0 or len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields blank!")
    else:
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
                # Updating old data
                data.update(new_data)
        except FileNotFoundError:
            data = new_data
        finally:
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)

                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entry Boxes
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

username_entry = Entry(width=35)
username_entry.insert(0, "example@email.com")
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save_user_info)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=search)
search_button.grid(column=2, row=1)

# ---------------------------- CANVAS SETUP ------------------------ #
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# ----------------------------- MAIN LOOP ----------------------------- #
window.mainloop()
