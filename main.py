from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

FONT_NAME = 'ariel'


# ---------------------------- FINDING THE USERNAME/PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            data.update()
        if website in data:
            messagebox.showinfo(title=website, message=f'Username: {data[website]["username"]} '
                                                       f'\n\nPassword: {data[website]["password"]}')
        else:
            messagebox.showerror(title='Error', message=f"'{website}' was not found. Try again.")
            website_entry.delete(0, END)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")


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
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title='Password', message='The password has been copied to the clipboard.')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'username': username,
            'password': password,
        }
    }
    with open('data.json', 'r') as file:
        website_list = json.load(file)

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title='Oops!', message="Please do not leave any fields empty!")

    elif website in website_list:
        duplicate_answer = messagebox.askyesno(title='Duplicate', message='This website is already on file. Would you '
                                                                          'like to replace the old information?')

        if duplicate_answer:
            # Same as below. (Have not trimmed  down the code yet)
            try:
                with open('data.json', 'r') as file:
                    # Reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            except json.decoder.JSONDecodeError:
                with open("data.json", "w") as file:
                    file.write("{}")
                    file.close()
                    messagebox.showerror(title='Slight Error', message='Enter the information again.')
            else:
                # Updating old data with new data
                data.update(new_data)

                with open('data.json', 'w') as file:
                    # Saving updated data
                    json.dump(data, file, indent=4)

            finally:
                website_entry.delete(0, END)
                username_entry.delete(0, END)
                username_entry.insert(0, 'ajlocke@live.com')
                password_entry.delete(0, END)
    else:
        # Same as above. (Have not trimmed down the code yet)
        try:
            with open('data.json', 'r') as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as file:
                file.write("{}")
                file.close()
                messagebox.showerror(title='Slight Error', message='Enter the information again.')
        else:
            # Updating old data with new data
            data.update(new_data)

            with open('data.json', 'w') as file:
                # Saving updated data
                json.dump(data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            username_entry.delete(0, END)
            username_entry.insert(0, 'ajlocke@live.com')
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text='Website:', font=FONT_NAME)
website_label.grid(row=1, column=0)
username_label = Label(text='Email/Username:', font=FONT_NAME)
username_label.grid(row=2, column=0)
password_label = Label(text='Password:', font=FONT_NAME)
password_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, sticky='ew')
website_entry.focus()
username_entry = Entry(width=35)
username_entry.grid(row=2, column=1, columnspan=2, sticky='ew')
username_entry.insert(0, 'ajlocke@live.com')
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky='ew')

# Buttons
generate_password_button = Button(text='Generate Password', font=FONT_NAME, command=generate_password)
generate_password_button.grid(row=3, column=2)
search_button = Button(text='Search', font=FONT_NAME, command=find_password)
search_button.grid(row=1, column=2, sticky='ew')
add_button = Button(text='Add', font=FONT_NAME, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky='ew')

window.mainloop()
