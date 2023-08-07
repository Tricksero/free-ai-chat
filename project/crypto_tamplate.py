from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
import hashlib


# aus dem server und datenbank zwei objekte machen

class cummunication_crypto:
    def __init__(self) -> None:
        self.pub_key_server = None
        self.priv_key_server = None
        self.symetric_key = None
        self.pub_key_server_bytes = None
        self.key_size = 4096 # in config auslagern

        self.generate_rsa_key_pair()
        self.export_public_key()

    def generate_rsa_key_pair(self):
        self.priv_key_server = RSA.generate(self.key_size)
        self.pub_key_server = self.priv_key_server.publickey()

    def export_public_key(self):
        self.pub_key_server_bytes = self.pub_key_server.export_key()

    def decrypt_message_symetric(self, encrypted_message: bytes):
        if not isinstance(encrypted_message, bytes):
            raise #Fehlermeldung schreiben
        
        cipher_suite = Fernet(self.symetric_key)
        decrypted_message = cipher_suite.decrypt(encrypted_message)
        return decrypted_message

    
    def encrypt_message_symetric(self, message):
        if isinstance(message, str):
            message = message.encode()
        elif not isinstance(message, bytes):
            raise #fehlermeldung
        
        cipher_suite = Fernet(self.symetric_key)
        encrypted_message = cipher_suite.encrypt(message)
        return encrypted_message
    
    def decrypt_message_assymetric(self, encrypted_message):
        if not isinstance(encrypted_message, bytes):
            raise #Fehlermeldung schreiben
        cipher_rsa = PKCS1_OAEP.new(self.priv_key_server)
        decrypted_message = cipher_rsa.decrypt(encrypted_message)
        
        return decrypted_message


def hash_password(plain_password: bytes):

    hash_object = hashlib.sha512()
    hash_object.update(plain_password)
    hex_digest = hash_object.hexdigest()
    return hex_digest

