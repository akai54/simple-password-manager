from sbox_list import sbox
from struct import pack, unpack

# sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]


def round(key, msg):
    return sbox[msg ^ key]


def enc(key, msg):
    tmp = round(key[0], msg)
    res = round(key[1], tmp)
    print(key, msg, tmp, res)
    return res


xobs = [sbox.index(n) for n in range(0, 256)]


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


def write_file_enc(file, cont):
    packed = pack("i" * len(cont), *cont)
    print(cont, packed)
    f = open(file, "wb")
    f.write(packed)
    f.close()


def write_file(file, cont):
    f = open(file, "wb")
    f.write(bytes(cont))
    f.close()


def enc_file_cbc(key, filename, rand_num):
    file = open(filename, "rb")
    byte = file.read()
    file.close()
    text = []
    for octet in byte:
        text.append(enc_byte(key, rand_num ^ octet))
        rand_num = enc_byte(key, rand_num ^ octet)
        print(chr(octet), octet, text)
    write_file_enc(filename + "enc", text)


def dec_file_cbc(key, filename, rand_num):
    # Reading file.
    file = open(filename, "rb")
    byte = file.read()
    file.close()

    # byte size
    byte_len = len(byte)
    int_byte_len = int(byte_len / 4)

    unpacked = unpack("i" * int_byte_len, byte)
    text_chiffrer = list(unpacked)
    res = []

    for octet in text_chiffrer:
        res.append(dec_byte(key, octet) ^ rand_num)
        rand_num = octet

    print(f"\nbyte: {byte}")
    print(f"\nbyte_len: {byte_len}")
    print(f"\nunpacked: {unpacked}")
    print(f"\ntext_chiffrer: {text_chiffrer}")
    print(f"\nres: {res}")

    write_file(filename + "dec", res)
