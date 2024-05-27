import json
from tkinter import *
from tkinter import messagebox as box
import pandas
from random import randint, choice, shuffle
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate():
    letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
              't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbol = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '*', '_', '+', '?']
    math = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    rand_letter = [choice(letter) for _ in range(randint(8, 10))]
    rand_symbol = [choice(symbol) for _ in range(randint(2, 4))]
    rand_math = [choice(math) for _ in range(randint(2, 4))]

    password_list = rand_letter + rand_math + rand_symbol
    shuffle(password_list)

    password = ''.join(password_list)
    pass_e.insert(0, f"{password}")
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    user = w_add.get()
    email_e = email_en.get()
    pas_en = pass_e.get()
    new_data = {user: {
        "email": email_e,
        "Password": pas_en,
    }
    }

    data = pandas.read_csv("pass2.csv")
    all_data = data.password.to_list()

    if pas_en in all_data:
        i_want = box.askyesno(title=pas_en,
                              message=f"Your password '{pas_en}' is easy to guess.\nDo you want to continue?")
        if i_want:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                with open("data.json", "w") as data_file:
                    data.update(new_data)
                    json.dump(data, data_file, indent=4)

            finally:
                w_add.delete(0, END)
                email_en.delete(0, END)
                pass_e.delete(0, END)
                box.showinfo(
                    title="Hurry", message="your password saved into data file")

    if len(user) == 0 or len(email_e) == 0 or len(pas_en) == 0:
        box.showinfo(
            title="Oops", message="Please don't leave any field empty")

    if 0 < len(user) < 4:
        box.showerror(
            title=user, message=f"Website address '{user}'  is too short")

    if 0 < len(email_e) <= 3:
        box.showerror(
            title=email_e, message=f"User name '{email_e}' must be at least three character")

    if 0 < len(pas_en) <= 3:
        box.showerror(
            title=pas_en, message=f"Password '{pas_en}' is too short")

    # for asking at the end

    if len(user) >= 4 and len(pas_en) > 3 and len(email_e) >= 4 and pas_en not in all_data:
        is_you_want = box.askokcancel(
            title=user, message=f"Your given data is \n{email_e} \n {pas_en} is it ok??")

        if is_you_want:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                with open("data.json", "w") as data_file:
                    data.update(new_data)
                    json.dump(data, data_file, indent=4)

            finally:
                w_add.delete(0, END)
                email_en.delete(0, END)
                pass_e.delete(0, END)
                box.showinfo(
                    title="Hurry", message="your password saved into data file")


# ---------------------------- PASSWORD SEARCH ------------------------------- #
def password_search():
    website = w_add.get()
    try:
        with open("data.json") as data:
            saved = json.load(data)
    except FileNotFoundError:
        box.showinfo(
            title="Oops", message='There is no data saved in my memory')
    else:
        if website in saved:
            email_get = saved[website]["email"]
            pass_get = saved[website]["Password"]
            box.showinfo(
                title=website, message=f"email: {email_get}\npassword: {pass_get}")
        else:
            box.showinfo(
                title="Error", message=f"There is no data about '{website}' saved in my memory")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

canvas = Canvas(width=200, height=200)
pic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pic)
canvas.grid(column=1, row=0)

web = Label(text="Website: ", font=("arial", 13))
web.grid(column=0, row=1)

w_add = Entry(width=33)
w_add.grid(column=1, row=1)
w_add.focus()

search = Button(text="Search", width=15, command=password_search)
search.grid(column=2, row=1)

email = Label(text="Email/Username: ", font=("arial", 13))
email.grid(column=0, row=2)

email_en = Entry(width=53)
email_en.grid(column=1, row=2, columnspan=3)

pas = Label(text="Password: ", font=("arial", 13))
pas.grid(column=0, row=3)

pass_e = Entry(width=33)
pass_e.grid(column=1, row=3)

generate = Button(text="Generate Password", width=15, command=generate)
generate.grid(column=2, row=3)

add = Button(text="Add", width=35, command=save)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
