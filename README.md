# MyPass
Local Passwords Administrator using Python Tkinter module 

This is a simple project wich purpose was learning tkinter basics and how to work with .json files properly

It displays a simple gui, that shows 3 entry fields that must be filled by the user:
- Website
- Email/Username
- Password

Once these three inputs are filled the user is able to proceed and add this information to a local generated .json file by clickinn on the Add button located at the bottom of the screen.

Also users are able to search their credetianls from an especific website just by typing the website name. This will display an info window that shows both the email and password from the especified website if it exists inside the .json file, otherwise it will show an error message window indicating that the website couldn't be found.

Finally the user can choose between generating a secured random password or introducing their own.