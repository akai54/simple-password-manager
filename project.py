
from random import randint

# EX1
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


enc_byte([3, 7], ord("f"))


def dec_byte(key, ctxt):
    premiere_partie = ctxt % 16
    deuxieme_partie = ctxt // 16
    resultat1 = dec(key, premiere_partie)
    resultat2 = dec(key, deuxieme_partie)
    final = (resultat1 << 4) | (resultat2)
    return final


dec_byte([3, 7], 221)


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
    write_file(filename + ".dec2", text)


from Cryptodome.Util.number import getPrime, inverse
import hashlib

def gen_rsa_keypair(bits, nom):
    pq_size = bits // 2
    p = getPrime(pq_size)
    q = getPrime(pq_size)

    assert p != q
    n = p * q  # module de chiffrement
    phi_de_n = (p - 1) * (q - 1)
    e = 65537  # exposant de chiffrement.
    assert e < phi_de_n and phi_de_n % e != 0

    d = inverse(e, phi_de_n)  # exposant de dechiffrement.
    print(
        f"Generation de clef pour {nom}.\nPQ_size = {pq_size}.\nP a été générée.\nQ a été générée.\nP est différent de Q.\nN a été générée.\nPhi de N a été générée.\nE = 65537.\nE respecte bien les conditions necessaires.\nD a été générée.\nReturn clef.\n"
    )
    return ((e, n), (d, n))

def rsa(msg, key):
    if 1:
        expo_mod = pow(msg, key[0], key[1])
        return expo_mod


def rsa_dec(msg, key):
    msg_dech = pow(msg, key[0], key[1])
    msg_str = msg_dech.to_bytes((msg_dech.bit_length() + 7) // 8, "big").decode("utf-8")
    print(msg_str)


def rsa_enc(msg, key):
    msg_int = int.from_bytes(msg.encode("utf-8"), "big")
    return rsa(msg_int, key)


def h(msg):
    msg_encoded = msg.encode()
    hash = int.from_bytes(hashlib.sha256(msg_encoded).digest(), "big")
    return hash


def rsa_sign(msg, key):
    hash = h(msg)
    signature = pow(hash, key[1][0], key[1][1])
    return (msg, signature)


def rsa_verify(sign, key):
    v = pow(sign[1], key[0][0], key[0][1])
    if v == h(sign[0]):
        print("Message authentique.\n")
    else:
        print("Message NON authentique.\n")


if __name__ == "__main__":
    clef_alice = gen_rsa_keypair(2048, "alice")
    clef_bob = gen_rsa_keypair(4096, "bob")
    rsa_dec(rsa_enc("Alice: Salut bob!", clef_alice[1]), clef_alice[0])
    rsa_dec(rsa_enc("Bob: Hey Alice!", clef_bob[1]), clef_bob[0])
    rsa_verify(rsa_sign("aurevoir", clef_alice), clef_alice)
    rand_num = randint(0, 255)
    enc_file_cbc([9, 0], "", rand_num)
    dec_file_cbc([9, 0], "", rand_num)
