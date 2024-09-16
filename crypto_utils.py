# crypto_utils.py

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
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


#  ----------------------------- Grupo E2EE assimetrica --------------------

class RSAEncryption:
    def __init__(self):
        self.users = {}

    def generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def add_user(self, user_id):
        private_key, public_key = self.generate_keys()
        self.users[user_id] = {
            'private_key': private_key,
            'public_key': public_key
        }

    def encrypt_message_for_all(self, message):
        encrypted_messages = {}
        for user, keys in self.users.items():
            public_key = keys['public_key']
            encrypted_message = public_key.encrypt(
                message.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_messages[user] = encrypted_message
        return encrypted_messages

    def decrypt_message(self, user_id, encrypted_message):
        private_key = self.users[user_id]['private_key']
        decrypted_message = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()


# rsa_encryption = RSAEncryption()

# # Adicionar usuários
# for i in range(5):
#     rsa_encryption.add_user(f'user{i+1}')

# # criptografar uma mensagem para todos os outros usuários
# message = "Olá, pessoal!"
# encrypted_messages = rsa_encryption.encrypt_message_for_all(message)

# # Cada usuário descriptografa a mensagem
# for user in rsa_encryption.users:
#     decrypted_message = rsa_encryption.decrypt_message(user, encrypted_messages[user])
#     print(f"Mensagem descriptografada pelo {user}: {decrypted_message}")
