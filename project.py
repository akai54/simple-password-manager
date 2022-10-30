import os
import sqlite3
import copy
import pyperclip
import secrets
from enc import *
from tabulate import tabulate

my_pwd = None


def end_fun(db_name):
    global my_pwd
    enc_fernet(my_pwd, db_name)
    os.system("cls" if os.name == "nt" else "clear")
    pyperclip.copy("")
    exit()


def enter_pwd():
    master_pwd = input("Please enter your Master Password: ")
    return master_pwd


def to_do(db_name, master=""):
    try:
        print(
            "Please press:\n"
            "1.Modify an entry.\n"
            "2.Delete an entry.\n"
            "3.Add an entry.\n"
            "4.Show all entries.\n"
            "5.Exit.\n"
        )
        choix = input("choice: ")
        if choix == "1":
            query_n = input("Please type the entry number: ")
            print("1.Modify site name.\n" "2.Modify username.\n" "3.Modify password.\n")
            to_change = input("choice: ")
            if to_change == "1":
                new_site = input("Enter new site name: ")
                query = """UPDATE passwords SET site_name = ? WHERE rowid = ?"""
                data = (new_site, query_n)
                modify_entry(db_name, query, data)
            elif to_change == "2":
                new_user = input("Enter new user name: ")
                query = """UPDATE passwords SET username = ? WHERE rowid = ?"""
                data = (new_user, query_n)
                modify_entry(db_name, query, data)
            elif to_change == "3":
                new_pwd = input("Enter new password: ")
                query = """UPDATE passwords SET pwd = ? WHERE rowid = ?"""
                data = (new_pwd, query_n)
                modify_entry(db_name, query, data)
            else:
                choix = 1
                to_do(db_name)

        elif choix == "2":
            to_delete = input("Please type the number of the entry to delete:")
            print("\n")
            delete_entry(db_name, to_delete)
        elif choix == "3":
            site = input("Site name:")
            usr = input("Username:")
            print("To generate a random password please type simply 'r'.")
            pwd = input("Password:")
            if pwd == "r":
                password_length = 20
                pwd = secrets.token_urlsafe(password_length)
                print(f"The generated password is: {pwd}")
            add_entry(db_name, site, usr, pwd)
        elif choix == "4":
            show_db(db_name)
        elif choix == "5":
            print(my_pwd)
            end_fun(db_name)
        else:
            print("Please choose only between the available choices.\n")
            to_do(db_name)
    except Exception as e:
        end_fun(db_name)


def modify_entry(db_name, query, entry):
    try:
        # Connect to database.
        conn = sqlite3.connect(db_name)

        # Create a cursor.
        cursor = conn.cursor()

        # Update Records.
        cursor.execute(query, entry)

        # Commit our command.
        conn.commit()
        # Close our connection.
        conn.close()

        to_do(db_name)
    except Exception as e:
        end_fun(db_name)


def delete_entry(db_name, rowid):
    try:
        # Connect to database.
        conn = sqlite3.connect(db_name)

        # Create a cursor.
        cursor = conn.cursor()

        # Delete Records.
        cursor.execute("DELETE FROM passwords WHERE rowid = ?", rowid)

        # Commit our command.
        conn.commit()
        # Close our connection.
        conn.close()

        to_do(db_name)
    except Exception as e:
        end_fun(db_name)


def show_db(db_name):
    try:
        # Connect to database.
        conn = sqlite3.connect(db_name)

        # Create a cursor.
        cursor = conn.cursor()

        # Query the db.
        cursor.execute("SELECT rowid, * FROM passwords")

        # Commit our command.
        conn.commit()

        # Print the whole db.
        print(tabulate(cursor.fetchall()))

        # Close our connection.
        conn.close()

        to_do(db_name)
    except Exception as e:
        end_fun(db_name)


def add_entry(db_name, site, usr, pwd):
    try:
        # Connect to database.
        conn = sqlite3.connect(db_name)

        # Create a cursor.
        cursor = conn.cursor()

        # Insert one Record into Table.
        cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (site, usr, pwd))

        # Commit our command.
        conn.commit()
        # Close our connection.
        conn.close()

        to_do(db_name)
    except Exception as e:
        end_fun(db_name)


def load_database():
    print("please choose the database.\n")
    list_databases = []
    for file in os.listdir():
        if file.endswith(".db"):
            list_databases.append(file)

    if len(list_databases) == 0:
        print("There are no available databases in the current directory.\n")
        exit()
    for i, val in enumerate(list_databases):
        print(i, val)
    chosen_file = int(input("\nEnter the database file number.\n"))
    print(f"You have chosen {list_databases[chosen_file]}\n")
    global my_pwd
    my_pwd = enter_pwd()
    try:
        dec_fernet(my_pwd, list_databases[chosen_file])
        to_do(list_databases[chosen_file])
    except Exception as e:
        print("Wrong password.")


def new_database():
    name = input("Please enter the name of this new database.\n")
    name = name + ".db"

    global my_pwd
    my_pwd = enter_pwd()

    # Connect to database.
    conn = sqlite3.connect(name)

    # Create a cursor.
    cursor = conn.cursor()

    # Create a Table.
    cursor.execute(
        """CREATE TABLE passwords (
                site_name text,
                username text,
                pwd text
                )"""
    )

    # Commit our command.
    conn.commit()
    # Close our connection.
    conn.close()
    print(f"A new database named {name} has been created in this directory.\n")
    to_do(name)


def choice():
    print(
        "Simple Password manager.\n"
        "Press n to create a new database.\n"
        "Press l to load an existing database.\n"
        "Press q to exit.\n"
    )
    choice = input()
    if choice == "n":
        new_database()
    elif choice == "l":
        load_database()
    elif choice == "q":
        os.system("cls" if os.name == "nt" else "clear")
        exit()
    else:
        print("Please choose only between the available choices.\n")


if __name__ == "__main__":
    choice()
