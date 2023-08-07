from collections.abc import Callable, Iterable, Mapping
import socket
import threading
from multiprocessing import Process
from typing import Any
from read_config import Config 
from crypto_tamplate import cummunication_crypto
import crypto_tamplate
import user_database_conn as userdata

# das key handling ändern. Nicht jedesmal neu erstellen!

class conversation(Process):
    
    def __init__(
        self,
        conn: socket,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] = {},
        *,
        daemon: bool | None = None
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.conn = conn
        self.crypto_connection = cummunication_crypto()
    
    def run(self):
        self.handshake()
        self.login()
        choose_chat(self.conn, self.username, self.crypto_connection)

    def handshake(self):
        self.crypto_connection.export_public_key()
        pub_key_server_bytes = self.crypto_connection.pub_key_server_bytes
        send_data(self.conn, pub_key_server_bytes)
        symetric_key_encrypt = recive_data(self.conn, 5000)
        symetric_key = self.crypto_connection.decrypt_message_assymetric(symetric_key_encrypt)
        self.crypto_connection.symetric_key = symetric_key

    def register(self):
        username = recive_data(self.conn)
        username = self.crypto_connection.decrypt_message_symetric(username)
        if len(username) < 30 and not userdata.check_user_exist(username):
            # username is valide
            msg = self.crypto_connection.encrypt_message_symetric(b"valid")
            send_data(self.conn, msg)
            password = recive_data(self.conn)
            password = crypto_tamplate.hash_password(
                        self.crypto_connection.decrypt_message_symetric(
                            password))
            userdata.create_new_user(username, password)
            self.login()
        else:
            msg = self.crypto_connection.encrypt_message_symetric(b"not valid")
            send_data(self.conn, msg)
            self.register()

    def login(self):
        username = recive_data(self.conn)
        username = self.crypto_connection.decrypt_message_symetric(username)
        if len(username) > 30:
            msg = self.crypto_connection.encrypt_message_symetric(b"exit")
            send_data(self.conn, msg)
        elif not userdata.check_user_exist(username):
            msg = self.crypto_connection.encrypt_message_symetric(b"register")
            send_data(self.conn, msg)
            self.register()
        elif userdata.check_user_exist(username):
            msg = self.crypto_connection.encrypt_message_symetric(b"continue")
            #später zufällig keins der anderen
            send_data(self.conn, msg)
            password = recive_data(self.conn)
            password_hash = crypto_tamplate.hash_password(
                self.crypto_connection.decrypt_message_symetric(password))
            if userdata.get_hashed_password(username) == password_hash:
                print("succes login") # Glückwunsch du bist eingelogt
                self.username = username
                msg = self.crypto_connection.encrypt_message_symetric(
                                                        b"succes login")
                send_data(self.conn, msg)
                
                
            else:
                self.conn.close()
                self.close()
                self.__del__()

 

def recive_data(conn: socket, recive_limit: int | None = None) -> bytes:
    if recive_limit is None:
        recive_limit = config_server["recive_limit"]
    return conn.recv(recive_limit)

def send_data(conn: socket, msg: bytes):
    if isinstance(msg, str):
        msg = msg.encode()
    conn.sendall(msg)


def choose_chat(conn: socket, username: str, crypto: cummunication_crypto):
    chats = str(userdata.get_chats_from_user(username)).strip("[]")
    print(chats)
    pass

global config_server

config_server = Config().get_server_configs()

# erstmal eine einfache unverschlpsselte version ohne login und datenbank? Will ich nicht. Dann lieber damit anfangen

# recive_limit

# private_key

# public_key

# hostname = socket.gethostname() 
# IPAddr = socket.gethostbyname(hostname) 
# print("Your Computer Name is:"+hostname)s: socket, crypto: cummunication_crypto)

HOST = "172.17.0.2" #if config_server["ip"] == "None" else config_server["ip"]  # Standard loopback interface address (localhost)
PORT = 8000 #if config_server["port"] == "None" else int(config_server["port"]) # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    # als variable umformulieren?
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        print("start_process")
        conversation(conn).start()
        # with conn:
        #     print(f"Connected by {addr}")
        #     while True:
        #         data = conn.recv(1024)
        #         if not data:
        #             break
        #         conn.sendall(data)
            