from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    #Clears password field
    password_input.delete(0,END)
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)
    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- UTIL FUNCTIONS ------------------------------- #
def check_entries(website, email, password):
    return len(website) == 0 or len(email) == 0 or len(password)==0

def read_data_from_json(file_name):
    #Reads data from json file if exists or creates it
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            #Checking if .json file is empty
    except (json.JSONDecodeError, FileNotFoundError) as e:
        with open("passwords.json", "w") as file:
            #writing "{}" to detect the file content as .json
            file.write("{}")
            data = None

    return data
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_to_json():
    #Getting all inputs from gui
    website = website_input.get().capitalize()
    email= username_input.get().strip().lower()
    password = password_input.get().strip()
    
    new_data= {
        website : {
            "email" : email,
            "password" : password
        }
    }

    if check_entries(website, email, password):
        messagebox.showinfo(title = "Invalid Entries", message = "Please don't leave any fields empty!")
        return

    #Confirmation message before saving
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}\n" +
                                                f"Password: {password}\nIs it okay to save?")
    #Appending new info to txt file 
    if is_ok:
        data = read_data_from_json("passwords.json")
        
        with open(file ="passwords.json", mode ="w") as file:
            if data != None:
                #Updates the current dictionary with the new keys and values
                data.update(new_data)
                json.dump(data, file, indent=4)
            else:
                #Only used when .json file is empty
                json.dump(new_data, file, indent=4)

        #Clear Entry
        website_input.delete(0,END)
        password_input.delete(0,END)

#  ---------------------------- GET WEBSITE INFO ------------------------------- #
def search_website_info():
    #Getting website name from user entry
    website = website_input.get().capitalize()

    #Reading data from passwords.json file
    data = read_data_from_json("passwords.json")

    #Checking if website exists in database
    if data == None or data.get(website) == None:
        messagebox.showinfo(title="There's an Error", message="The website is not found, sorry.")
    else:
        #Getting data from current website
        website_info = data[website]
        email = website_info["email"] 
        password = website_info["password"]
        messagebox.showinfo(title=website, message= f"Website credentials\n"
                                                    f"Email: {email}\n"
                                                    f"Password: {password}\n"
                                                    "Password has been copied to clipboard")
        #copying website password to clipboard
        pyperclip.copy(password)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20 , pady=20)
window.grid_columnconfigure(1, weight=1)

canvas = Canvas(width = 200, height = 200)
logo_img = PhotoImage(file = "logo.png")
canvas.create_image(100,100 , image = logo_img)
canvas.grid(column = 1, row = 0)

#labels
website_label = Label(text = "Website:", width=25)
website_label.grid(column= 0, row = 1,)
username_label = Label(text = "Email/Username:", width=25)
username_label.grid(column=0, row=2,)
password_label = Label(text = "Password:", width=25)
password_label.grid(column=0, row=3,)

#Inputs
website_input = Entry(width=36)
website_input.grid(column=1, row=1)
website_input.focus()
username_input = Entry(width=36)
username_input.grid(column=1, row=2)
username_input.insert(END, 'example@test.com')
password_input = Entry(width=36)
password_input.grid(column=1, row=3)

search_btn = Button(text = "Search", width = 25, command = search_website_info)
search_btn.grid(column=2, row=1)
gen_pass_btn = Button(text = "Generate Password",width=25, command = generate_password)
gen_pass_btn.grid(column=2, row=3)
add_btn = Button(text = "Add", width=30, command=save_to_json)
add_btn.grid(column=1, row=4)

window.mainloop()