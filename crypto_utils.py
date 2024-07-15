from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os


def generate_aes_key():
    # Gera uma chave AES aleatória de 16 bytes.
    return os.urandom(16)


def encrypt(message, key):
    encrypted = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))
    encrypted_text = encrypted.encrypt(pad(message.encode(), 16))
    return  encrypted_text


def decrypt(ciphertext, key):
    decrypted = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))
    decrypted_text = unpad(decrypted.decrypt(ciphertext), 16).decode()
    return decrypted_text
