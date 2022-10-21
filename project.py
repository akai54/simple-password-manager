import os
import sqlite3
import copy
from random import randint
from tabulate import tabulate

sbox = [
    180,
    9,
    32,
    0,
    69,
    223,
    248,
    151,
    35,
    209,
    60,
    254,
    11,
    170,
    185,
    178,
    8,
    153,
    14,
    157,
    103,
    122,
    176,
    201,
    142,
    61,
    77,
    25,
    109,
    62,
    54,
    66,
    168,
    137,
    193,
    224,
    27,
    206,
    20,
    233,
    235,
    51,
    117,
    231,
    52,
    128,
    252,
    96,
    119,
    79,
    220,
    55,
    245,
    101,
    183,
    99,
    171,
    5,
    41,
    13,
    236,
    28,
    95,
    59,
    172,
    125,
    57,
    2,
    83,
    102,
    179,
    120,
    232,
    155,
    123,
    58,
    129,
    108,
    225,
    18,
    241,
    71,
    243,
    204,
    48,
    208,
    106,
    104,
    187,
    78,
    26,
    199,
    121,
    255,
    132,
    94,
    43,
    196,
    197,
    50,
    140,
    194,
    186,
    84,
    63,
    234,
    23,
    118,
    82,
    160,
    1,
    21,
    92,
    114,
    15,
    226,
    152,
    188,
    80,
    250,
    45,
    207,
    205,
    200,
    113,
    217,
    216,
    81,
    68,
    86,
    91,
    149,
    163,
    139,
    70,
    97,
    145,
    88,
    195,
    253,
    87,
    49,
    39,
    150,
    110,
    249,
    173,
    244,
    37,
    85,
    73,
    22,
    53,
    17,
    6,
    177,
    141,
    165,
    44,
    3,
    246,
    36,
    159,
    158,
    89,
    229,
    16,
    100,
    65,
    218,
    56,
    136,
    184,
    169,
    143,
    251,
    4,
    47,
    181,
    219,
    210,
    138,
    127,
    40,
    198,
    12,
    164,
    107,
    105,
    228,
    90,
    174,
    175,
    98,
    115,
    214,
    215,
    202,
    30,
    33,
    76,
    42,
    156,
    147,
    64,
    162,
    154,
    130,
    237,
    167,
    72,
    134,
    112,
    93,
    222,
    67,
    230,
    75,
    192,
    124,
    31,
    116,
    131,
    34,
    111,
    74,
    46,
    7,
    190,
    24,
    182,
    133,
    126,
    148,
    19,
    161,
    211,
    135,
    238,
    239,
    212,
    203,
    247,
    242,
    166,
    144,
    221,
    227,
    189,
    38,
    213,
    29,
    240,
    10,
    146,
    191,
]


def round(key, msg):
    return msg ^ key


def enc(key, msg):
    for e in key:
        tmp = round(e, msg)
        res = round(e, tmp)
    return res


# xobs = [sbox.index(n) for n in range(0, 256)]


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


my_pwd = []


def set_my_pwd(pwd):
    my_pwd[:] = list(pwd)


def get_master_pwd():
    return my_pwd


def end_fun(master_pwd, db_name):
    testo = get_master_pwd()
    print(testo, master_pwd, db_name)
    enc_file_cbc(master_pwd, db_name, 7)
    os.system("cls" if os.name == "nt" else "clear")
    exit()


def enter_pwd():
    master_pwd = input("Please enter your Master Password: ")
    tab = [ord(c) for c in master_pwd]
    return tab


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
            pwd = input("Password:")
            print("\n")
            add_entry(db_name, site, usr, pwd)
        elif choix == "4":
            show_db(db_name)
        elif choix == "5":
            print(get_master_pwd())
            end_fun(get_master_pwd(), db_name)
        else:
            print("Please choose only between the available choices.\n")
            to_do(db_name)
    except KeyboardInterrupt:
        end_fun(get_master_pwd(), db_name)
    except Exception as e:
        end_fun(get_master_pwd(), db_name)


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

    if len(list_databases) == 0:
        print("There are no available databses in the current directory.\n")
        exit()
    for i, val in enumerate(list_databases):
        print(i, val)
    chosen_file = int(input("\nEnter the database file number.\n"))
    print(f"You have chosen {list_databases[chosen_file]}\n")
    master = enter_pwd()
    set_my_pwd(master)
    dec_file_cbc(master, list_databases[chosen_file], 7)
    to_do(list_databases[chosen_file])


def new_database():
    name = input("Please enter the name of this new database.\n")
    name = name + ".db"

    master = enter_pwd()
    set_my_pwd(master)

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
    # add_entry("eli.db", "fb", "b", "1")
    # enc_file_cbc([2, 4], "eli.db", 7)
    # dec_file_cbc([0], "test.txt.enc2", 7)
    # print("Chiffrement du fichier test.txt effectué en cbc.\n")
    # print("Dechiffrement du fichier test.txt effectué.\n")
