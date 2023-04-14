from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for letter in range(randint(8, 10))]
    password_list += [choice(symbols) for symbol in range(randint(2, 4))]
    password_list += [choice(numbers) for number in range(randint(2, 4))]
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {"email": username,
                  "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="warning", message="website or password cannot be empty")
    else:
        try:
            with open("passlist.json", "r") as passlist:
                #open passlist json file
                data = json.load(passlist)
        except FileNotFoundError:
            with open("passlist.json", "w") as passlist:
                json.dump(new_data, passlist, indent=4)
        else:
            #updating data in file
            data.update(new_data)
            with open("passlist.json", "w") as passlist:
                json.dump(data, passlist, indent=4)
                website_entry.delete(0, END)
                password_entry.delete(0, END)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    with open("passlist.json", "r") as passlist:
        # open passlist json file
        data = json.load(passlist)
        if website in data.keys():
            retrieved_username = data[website]["email"]
            retrieved_password = data[website]["password"]
            messagebox.showinfo(title=f"{website} data", message=f"Username/Email:    {retrieved_username}\n Password:    {retrieved_password}")






# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=200, height=200, highlightthickness=0)
password_logo = PhotoImage(file="password_logo.png")
canvas.create_image(100, 100, image=password_logo)
canvas.grid(column=1, row=0)

#labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)


#entries
website_entry = Entry(width=27)
website_entry.focus()
website_entry.grid(column=1, row=1)
username_entry = Entry(width=45)
username_entry.insert(0, "username@email.com")
username_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=27)
password_entry.grid(column=1, row=3)


#buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_password_button = Button(width=38, text="Add", command=save_password)
add_password_button.grid(column=1, row=4, columnspan=2)
find_password_button = Button(width=14, text="Find", command=find_password)
find_password_button.grid(column=2, row=1)

window.mainloop()