import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def write_file(file, cont):
    f = open(file, "wb")
    f.write(bytes(cont))
    f.close()


# key generation
# key = Fernet.generate_key()
mysalt = b"\x84\x8d\xc4\xfd\xe0\x176\xb2\xbf\x9f<v<e\xf9\xe6"


kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256,
    length=32,
    salt=mysalt,
    iterations=100000,
    backend=default_backend(),
)

final_key = None
derived = False


def set_final(key):
    global final_key
    final_key = key


def get_final():
    return final_key


def enc_fernet(key, filename):
    with open(filename, "rb") as f:
        original = f.read()
    global derived
    if derived is False:
        password = key.encode()
        test = kdf.derive(password)
        key_2 = base64.urlsafe_b64encode(test)
        set_final(key_2)
        fernet = Fernet(key_2)
        encrypted = fernet.encrypt(original)
        with open(filename, "wb") as encrypted_file:
            encrypted_file.write(encrypted)
        derived = True
    else:
        fernet = Fernet(get_final())
        encrypted = fernet.encrypt(original)
        with open(filename, "wb") as encrypted_file:
            encrypted_file.write(encrypted)


def dec_fernet(key, filename):
    global derived
    if derived is False:
        password = key.encode()
        key_2 = base64.urlsafe_b64encode(kdf.derive(password))
        set_final(key_2)
        fernet = Fernet(key_2)
        with open(filename, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        with open(filename, "wb") as decrypted_file:
            decrypted_file.write(decrypted)
        derived = True
    else:
        fernet = Fernet(get_final())
        with open(filename, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        with open(filename, "wb") as decrypted_file:
            decrypted_file.write(decrypted)
