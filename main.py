"""
    Title: MyPass 
    Author: BrandonMagana
    Description: Local Password Administrator using Tkinter module
"""
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
"""
    Generates a random password from a set of characters and displays it at 
    the corresponding entry.
    Arguments:
        None
    Returns:
        None
"""
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

    #shuffles the random selected characters from each list
    shuffle(password_list)

    #Creates new password
    password = "".join(password_list)

    #Displays password in GUI corresponding field
    password_input.insert(0, password)

# ---------------------------- UTIL FUNCTIONS ------------------------------- #
"""
    Confirms that all entries have been filled
    Arguments:
        * website (str): string that represents the corresponding input for that provided 
                       in that field
        * email (str): string that represents the corresponding input for that provided 
                       in that field
        * password (str): string that represents the corresponding input for that provided 
                          in that field
    Returns:
        * boolean: True if all entries have been filled, otherwise False
    
"""
def check_entries(website, email, password):
    return len(website) == 0 or len(email) == 0 or len(password)==0

"""
    Reads data from json file if exists otherwise creates the file
    Arguments:
        * file_name (str): string that represents the path of the .json file
    Returns:
        * data (dict): if data exists otherwise None
""" 
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

"""
    Saves the inputs provided from GUI to .json file
    Arguments:
        * None
    Returns:
        * None
"""
def save_to_json():
    #Getting all inputs from gui
    website = website_input.get().capitalize()
    email= username_input.get().strip().lower()
    password = password_input.get().strip()
    

    #Checking if all inputs have been given properly
    if check_entries(website, email, password):
        messagebox.showinfo(title = "Invalid Entries", message = "Please don't leave any fields empty!")
        return

    #Confirmation message before saving the info
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}\n" +
                                                f"Password: {password}\nIs it okay to save?")
    #Saving info to .json file
    if is_ok:
        
        #Dictionary that contains the info to been saved
        new_data= {
            website : {
                "email" : email,
                "password" : password
            }
        }

        #Copying password to clipboard
        pyperclip.copy(password)

        #Reads .json file or creates a new one if doestn't exists
        data = read_data_from_json("passwords.json")
        
        #Writes to .json file
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
"""
    Search for website inside .json file, if exits displays a window with the credentials for the website
    otherwise, shows a window with an error message.
    Arguments:
        * None
    Returns:
        * None
"""
def search_website_info():
    #Getting website name from user entry
    website = website_input.get().capitalize()

    #Reading data from passwords.json file
    data = read_data_from_json("passwords.json")

    #Checking if website exists in database
    if data == None or data.get(website) == None:
        messagebox.showinfo(title="There's an Error", message=f"No details for {website} found.")
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

#Creating and configurating window
window = Tk()
window.title("Password Manager")
window.config(padx=20 , pady=20)
window.grid_columnconfigure(1, weight=1)

#Canvas
canvas = Canvas(width = 200, height = 200)
logo_img = PhotoImage(file = "logo.png")
canvas.create_image(100,100 , image = logo_img)
canvas.grid(column = 1, row = 0)

#Labels
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

#Buttons
search_btn = Button(text = "Search", width = 25, command = search_website_info)
search_btn.grid(column=2, row=1)
gen_pass_btn = Button(text = "Generate Password",width=25, command = generate_password)
gen_pass_btn.grid(column=2, row=3)
add_btn = Button(text = "Add", width=30, command=save_to_json)
add_btn.grid(column=1, row=4)

window.mainloop()