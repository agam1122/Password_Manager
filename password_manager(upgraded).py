from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
alphabets = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '@', '#', '$', '%', '^', '*', '(', ')', '<', '>', '?']


def generate_password():
    password_input.delete(0, END)
    random_alphabets = random.choices(alphabets, k=5)  # idhar k ki jagah kush bhi likhoge to error dega

    random_numbers = random.choices(numbers, k=4)

    random_symbols = random.choices(symbols, k=4)

    password_list = random_alphabets + random_numbers + random_symbols

    random.shuffle(password_list)

    password_string = "".join(password_list)
    pyperclip.copy(password_string)
    password_input.insert(END, password_string)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_name_input.get()
    email_username = email_username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            'email': email_username,
            'password': password
        }
    }
    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Invalid Input", message="You left some field empty")

    else:
        correct_input = messagebox.askyesno(title="Confirmation",
                                            message=f"Website: {website}, Email/Username: {email_username}, Password: {password}")
        if correct_input:
            try:
                with open(file="passwords.json", mode='r') as file:
                    # for writing
                    # json.dump()
                    # for reading
                    # json.load()
                    # for update
                    # json.update()
                    data = json.load(file)
                    data.update(new_data)
                with open(file="passwords.json", mode='w') as file:
                    json.dump(data, file, indent=4)
            except FileNotFoundError:
                with open(file="passwords.json", mode='w') as file:
                    json.dump(new_data, file, indent=4)
            finally:
                website_name_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- SEARCH WEBSITE ------------------------------- #


def search_website():
    website = website_name_input.get()
    email_username = email_username_input.get()
    try:
        with open(file="passwords.json", mode='r') as file:
            data = json.load(file)
    except FileNotFoundError:
        with open(file="passwords.json", mode='w') as file:
            json.dump('', file, indent=4)
    if website in data:
        password = data[website]['password']
        messagebox.showinfo(message=f"Website: {website}\nE-mail: {email_username}\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showinfo(message=f"password for {website} not found!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(500, 400)
window.config(padx=20, pady=20)

# For lock symbol at the top
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
# adjust x and y coordinates according to your convenience
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)


# Specifies the text "Website: " written on the screen
website_text = Label(text="Website: ", font=("Courier", 14, "italic"))
website_text.grid(row=1, column=0)

# Specifies place where website's name should be entered
website_name_input = Entry(width=22)
website_name_input.grid(row=1, column=1)
website_name_input.focus()

# Specifies search button
search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(row=1, column=2)

# Specifies the text "Email/Username: " written on the screen
email_username_text = Label(text="Email/Username: ", font=("Courier", 14, "italic"))
email_username_text.grid(row=2, column=0)

# Specifies place where website's email should be entered
email_username_input = Entry(width=40)
email_username_input.grid(row=2, column=1, columnspan=2)
email_username_input.insert(index=0, string="demo_email@gmail.com")

# Specifies the text "Password: " written on the screen
password_text = Label(text="Password: ", font=("Courier", 14, "italic"))
password_text.grid(row=3, column=0)

# Specifies place where website's password should be entered
password_input = Entry(width=22)
password_input.grid(row=3, column=1)

# Specifies Generate Password button
generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)

# Specifies Add button
Add_button = Button(text="Add", width=37, command=add_password)
Add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
