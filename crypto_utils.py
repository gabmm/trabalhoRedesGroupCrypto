# crypto_utils.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets


def generate_random_key():
    return secrets.token_bytes(32)  # 256 bits (32 bytes)

def generate_random_iv():
    return secrets.token_bytes(16)  # 128 bits (16 bytes)

def encrypt(message, key, IV):
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padded_message = pad(message, AES.block_size)
    encrypted_message = encryptor.encrypt(padded_message)
    return encrypted_message


def decrypt(cipher, key, IV):
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    decrypted_message = unpad(decrypted_padded_message, AES.block_size)
    return decrypted_message
