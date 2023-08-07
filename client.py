import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
import time
from getpass import getpass

class cummunication_crypto:
    def __init__(self) -> None:
        self.symetric_key = None
        self.pub_key_server = None


    def import_public_key(self, public_key_bytes):
        self.pub_key_server = RSA.import_key(public_key_bytes)

    def encrypt_message_assymetric(self, message: str | bytes):
        if isinstance(message, str):
            message = message.encode('utf-8')
        if not isinstance(message, bytes):
            raise # später eine Fehlermeldung schreiben

        cipher_rsa = PKCS1_OAEP.new(self.pub_key_server)
        encrypted_message = cipher_rsa.encrypt(message)
        
        return encrypted_message
    
    def encrypt_message_symetric(self, message: str | bytes):
        if isinstance(message, str):
            message = message.encode()
        elif not isinstance(message, bytes):
            raise #fehlermeldung
        
        cipher_suite = Fernet(self.symetric_key)
        encrypted_message = cipher_suite.encrypt(message)
        return encrypted_message
    
    def decrypt_message(self, encrypted_message: bytes) -> str:
        if not isinstance(encrypted_message, bytes):
            raise #Fehlermeldung schreiben
        cipher_suite = Fernet(self.symetric_key)
        decrypted_message = cipher_suite.decrypt(encrypted_message)
        return decrypted_message.decode()



HOST = "172.17.0.2"  # The server's hostname or IP address
PORT = 8000  # The port used by the server

def get_massage(crypto: cummunication_crypto):
    data = s.recv(600)
    return crypto.decrypt_message(data)
    

def handshake(s: socket, crypto: cummunication_crypto):
    data = s.recv(5000)
    print(f"Received {data!r}")
    crypto.import_public_key(data)
    crypto.symetric_key = Fernet.generate_key()
    print(crypto.symetric_key)
    pub_key_user_encrypt = crypto.encrypt_message_assymetric(crypto.symetric_key)
    s.sendall(pub_key_user_encrypt)

def register(s: socket, crypto: cummunication_crypto):
    print("you are not registert on the server. Restart the Programm or type in your username to register.")
    username = input("username: ").encode()
    username = crypto.encrypt_message_symetric(username)
    s.sendall(username)
    answer = s.recv(600)
    answer = crypto.decrypt_message(answer)
    if not answer == "valid":
        register(s, crypto)
    
    password = crypto.encrypt_message_symetric(getpass().encode())
    s.sendall(password)
    login(s, crypto)
    
    
def auth_error(s: socket, crypto: cummunication_crypto):
    print("An authentication error is happend. Please Try again")
    raise


def login(s: socket, crypto: cummunication_crypto):
    username = input("username: ").encode()
    username = crypto.encrypt_message_symetric(username)
    s.sendall(username)
    answer = s.recv(600)
    answer = crypto.decrypt_message(answer)
    if answer != "error" and answer != "register":
        password = crypto.encrypt_message_symetric(getpass())
        s.sendall(password)
    elif answer == "register":
        register(s, crypto)
    elif answer == "error":
        print("please try again to connect to the Server or register.")
        print("to register type in a new username to try again please type in exit")
        register_answer = input()
        if register_answer == "exit":
            exit()
        else:
            pass
    else:
        password = crypto.encrypt_message_symetric(getpass().encode())
        s.sendall(password)
    
    answer = crypto.decrypt_message(s.recv(600))
    shoose_chat(s, crypto) if answer == "succes login" else \
        auth_error(s, crypto)
    

def shoose_chat(s: socket, crypto: cummunication_crypto):
    pass

crypto = cummunication_crypto()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    handshake(s, crypto)
    login(s, crypto)
    
    # while True:
    data = s.recv(600)
    answer = crypto.decrypt_message(data)
    print(answer)
    user_input = input().encode()
    user_input = crypto.encrypt_message_symetric(user_input)
    s.sendall(user_input)

