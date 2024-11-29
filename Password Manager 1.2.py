# This is a python script for storing and recalling usernames and passwords
# associated to specific URL's
# Created by Matt Thompson
# Created on 04/12/2023
# Completed on 06/12/2023
# Version 1.2 (added password protection to the storage file)

import getpass
import hashlib

owner = input("Hi there! Might I begin with your name? ")

print("Welcome to your your password manager, {}.".format(owner))
print("How may I help you today?")

#Creating a slight delay to feel more oganic.
import time
time.sleep(0.6)

#Define function to load or create storage file if not found in specified directory.
Login_Details = "Login Details.txt"

def load_login(password):
    try:
        with open(Login_Details, "r") as file:
            content = file.read()
            decrypted_content = decrypt(content, password)
            lines = decrypted_content.strip().split("\n")
            return {url: {"username": username, "password": password} for url, username, password in (line.split(",") for line in lines)}
    except FileNotFoundError:
        return {}

#Function to save login information to the storage file.
def save_login(login, password):
    with open(Login_Details, "w") as file:
        login_str = "\n".join(f"{url},{data['username']},{data['password']}" for url, data in login.items())
        encrypted_content = encrypt(login_str, password)
        file.write(encrypted_content)

#Encrypt the stored password information.
def encrypt(content, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    encrypted_content = ""

    for i, char in enumerate(content):
        encrypted_char = chr(ord(char) + int(hashed_password[i % len(hashed_password)], 16))
        encrypted_content += encrypted_char

    return encrypted_content

#Decrypt the stored password information.
def decrypt(content, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    decrypted_content = ""

    for i, char in enumerate(content):
        decrypted_char = chr(ord(char) - int(hashed_password[i % len(hashed_password)], 16))
        decrypted_content += decrypted_char

    return decrypted_content

#Define a function to recall the password.
def get_password():
    return getpass.getpass("Enter your password: ")

#Defining function for writing the login details to the storage file.
def add_login():
    url = input("What site is this login for? ")
    username = input("What is the username? ")
    password = input("What is the password? ")

    login = load_login(get_password())
    login[url] = {"username": username, "password": password}
    save_login(login, get_password())
    print("Login successfully added.")

#Defining function to recall stored login information.
def get_login():
    url = input("Which URL would you like to display? ")
    login = load_login(get_password())

    if url in login:
        print(f"Username: {login[url]['username']}")
        print(f"Password: {login[url]['password']}")
    else:
        print("No details found for that particular site.")

#Creating the main menu.
def main():
    while True:
        print("""
        1. Add Login
        2. Show Login
        3. Exit
        """)
        option = input("Which would you like to do? ")

        if option == "1":
            add_login()
        elif option == "2":
            get_login()
        elif option == "3":
            print("Thank you for using DigiCore's password manager, closing now.")
            break
        else:
            print("Invalid option, please review the choices and try again.")

#Running the password manager.
if __name__ == "__main__":
    main()
