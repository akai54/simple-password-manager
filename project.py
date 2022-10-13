from random import randint
import os

sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

def round(key, msg):
    return sbox[msg ^ key]

def enc(key, msg):
    tmp = round(key[0], msg)
    res = round(key[1], tmp)
    return res

xobs = [sbox.index(n) for n in range(0, 16)]

def back_round(k, c):
    return xobs[c] ^ k

def dec(key, ctxt):
    tmp = back_round(key[1], ctxt)
    res = back_round(key[0], tmp)
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
    write_file(filename + ".enc2", text)


def dec_file_cbc(key, filename, rand_num):
    file = open(filename, "rb")
    byte = file.read()
    file.close()
    text = []
    for octet in byte:
        text.append(dec_byte(key, octet) ^ rand_num)
        rand_num = octet
    # for _ in text:
        #print(chr(_), end='')
    write_file(filename + ".dec2", text)

def load_database():
    print("please choose the database.\n")
    dir_list = os.listdir()
    for x in os.listdir():
        if x.endswith(".enc2"):
            print(x)
    chosen_file = input("Enter the database file number.\n")

def new_database():
    name = input("Please enter the name of this new database.\n")
    print(f'A new database named {name} has been created in this directory.\n')

def choice():
    print("Simple Password manager.\n"
          "Press n to create a new database.\n"
          "Press l to load an existing database.\n"
          "Press q to exit.\n")
    choice = input()
    if choice == "n":
        pass 
    elif choice == "l":
        load_database()
    elif choice == "q":
        exit()
    else:
        print("Please choose only between the available choices.\n")
    return choice

if __name__ == "__main__":
    choice()
    rand_num = randint(0, 255)
    enc_file_cbc([9, 0], "test.txt", rand_num)
    print("Chiffrement du fichier test.txt effectué en cbc.\n")
    dec_file_cbc([9, 0], "test.txt.enc2", rand_num)
    print("Dechiffrement du fichier test.txt effectué.\n")
