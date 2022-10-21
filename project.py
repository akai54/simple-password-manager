import os
import sqlite3
from random import randint
from tabulate import tabulate

# sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]


def round(key, msg):
    return msg ^ key


def enc(key, msg):
    for e in key:
        tmp = round(e, msg)
        res = round(e, tmp)
    return res


# xobs = [sbox.index(n) for n in range(0, 16)]


def back_round(k, c):
    return c ^ k


def dec(key, ctxt):
    for e in key:
        tmp = back_round(e, ctxt)
        res = back_round(e, tmp)
    return res


def enc_byte(key, msg):
    premiere_partie = msg % 16
    deuxieme_partie = msg // 16
    resultat1 = enc(key, premiere_partie)
    resultat2 = enc(key, deuxieme_partie)
    final = (resultat1 << 4) | (resultat2)
    return final


def dec_byte(key, ctxt):
    premiere_partie = ctxt % 16
    deuxieme_partie = ctxt // 16
    resultat1 = dec(key, premiere_partie)
    resultat2 = dec(key, deuxieme_partie)
    final = (resultat1 << 4) | (resultat2)
    return final


def enc_ascii(key, msg):
    return enc_byte(key, ord(msg))


def dec_ascii(key, ctxt):
    resultat = dec_byte(key, ctxt)
    return chr(resultat)


def write_file(file, cont):
    f = open(file, "wb")
    f.write(bytes(cont))
    f.close()


def enc_file(key, file):
    text = []
    with open(file, "rb") as f:
        while byte := f.read(1):
            text.append(enc_byte(key, ord(byte)))
    write_file(file + ".enc", text)


def dec_file(key, file):
    text = []
    with open(file, "rb") as f:
        while byte := f.read(1):
            text.append(dec_byte(key, int.from_bytes(byte, "big")))
    write_file(file + ".dec", text)


def enc_file_cbc(key, filename, rand_num):
    file = open(filename, "rb")
    byte = file.read()
    file.close()
    text = []
    for octet in byte:
        text.append(enc_byte(key, rand_num ^ octet))
        rand_num = enc_byte(key, rand_num ^ octet)
    write_file(filename, text)


def dec_file_cbc(key, filename, rand_num):
    file = open(filename, "rb")
    byte = file.read()
    file.close()
    text = []
    for octet in byte:
        text.append(dec_byte(key, octet) ^ rand_num)
        rand_num = octet
    # for _ in text:
    # print(chr(_), end='')
    write_file(filename, text)


def end_fun(master_pwd, db_name):
    enc_file_cbc(master_pwd, db_name, 7)
    os.system("cls" if os.name == "nt" else "clear")
    exit()


def enter_pwd():
    master_pwd = input("Please enter your Master Password: ")
    tab = [ord(c) for c in master_pwd]
    return tab


def to_do(db_name, master=""):
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

    elif choix == "2":
        to_delete = input("Please type the number of the entry to delete:")
        print("\n")
        delete_entry(db_name, to_delete)
    elif choix == "3":
        site = input("Site name:")
        usr = input("Username:")
        pwd = input("Password:")
        print("\n")
        add_entry(db_name, site, usr, pwd)
    elif choix == "4":
        show_db(db_name)
    elif choix == "5":
        end_fun(master, db_name)
    else:
        print("Please choose only between the available choices.\n")
        to_do(db_name)


def modify_entry(db_name, query, entry):
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


def delete_entry(db_name, rowid):
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


def show_db(db_name):
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


def add_entry(db_name, site, usr, pwd):
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


def load_database():
    print("please choose the database.\n")
    list_databases = []
    for file in os.listdir():
        if file.endswith(".db"):
            list_databases.append(file)

    for i, val in enumerate(list_databases):
        print(i, ",", val)
    chosen_file = int(input("\nEnter the database file number.\n"))
    print(f"You have chosen {list_databases[chosen_file]}\n")
    master = enter_pwd()
    dec_file_cbc(master, list_databases[chosen_file], 7)
    to_do(list_databases[chosen_file] + ".dec2", master)


def new_database():
    name = input("Please enter the name of this new database.\n")
    name = name + ".db"

    master = enter_pwd()

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
    enc_file_cbc(master, name, 7)
    print(f"A new database named {name} has been created in this directory.\n")
    dec_file_cbc(master, name, 7)
    to_do(name, master)


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
    return choice


if __name__ == "__main__":
    choice()
    # add_entry("eli.db", "fb", "b", "1")
    # enc_file_cbc([2, 4], "eli.db", 7)
    # dec_file_cbc([0], "test.txt.enc2", 7)
    # print("Chiffrement du fichier test.txt effectué en cbc.\n")
    # print("Dechiffrement du fichier test.txt effectué.\n")
