"""
Message Server Handling the generation of responses wrapping various language model APIs
while providing basic functionality to integrate responses into a website
"""

from __future__ import annotations
import time
import zmq
import sys
import json
from typing import Iterable, List, Tuple
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

# this should probably be made a pip module at some point
from chat_api.gpt4all_chat import Chat


class Message:
    def __init__(self, session="", question="", state=""):
        self.session = session
        self.question = question
        self.state = state
        self.response: None | List[str] = None

    @classmethod
    def create_message_from_json(cls, json_str: str) -> Message:
        """
        Turns message string from json into a Message object.
        TODO: Do this via using kwargs**
        """
        # unpacking message of client
        message_dict = json.loads(json_str)

        session = message_dict.get("question_id")
        question = message_dict.get("question_text", "")
        client_question_state = message_dict.get("state", "")
        return Message(session, question, client_question_state)

    def build_byte_response(self) -> bytes:
        """
        Build response message in byte format that can be send via TCP.
        """
        chat_response = {
            "question_id": self.session,
            "response": self.response,
            "state": self.state,
        }
        print("response_json: ", chat_response)
        response_json = json.dumps(chat_response)
        response_json = response_json.encode("utf-8")
        return response_json


class ChatServer:
    def __init__(self, timeout, model_name):
        self.chat_obj = Chat()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        self.cached_generators = {}

    def question_response(self, gen: Iterable) -> Tuple[List[str], Iterable, str]:
        """
        This function aims to contribute to a quick visibly building response
        by generating response fragments word by word until a word limit is
        reached or a generation time limit is reached and then returns that
        fragment to the view handling the display of this message.

        should probably depend on how many characters are already
        to be displayed

        TODO: check if this works with all generator types or make it work with all
        TODO: maybe improve output at some point
        """
        MAX_GENERATION_TIME = 2
        MAX_CHARACTER_COUNT = 50
        response_msg = []
        state = "finished"
        start_time = time.time()
        for word in gen:
            response_msg.append(word)
            if MAX_CHARACTER_COUNT == len(response_msg):
                state = "unfinished"
                break
            if MAX_GENERATION_TIME < start_time - time.time():
                state = "unfinished"
                break
        print("generated", response_msg)
        return response_msg, gen, state

    def get_generator(self, message: Message) -> Iterable:
        """
        Get or create generator and generate answer
        TODO: Check if this still works and also with different models
        """
        gen: Iterable | None = None
        if not gen:
            # makes sure a question that has already a generated part does not
            # get generated anew again when the generator was not saved
            if message.state == "unfinished":
                # state = "failed"
                # response_json = self.build_json_reponse(session, "", state)
                # self.socket.send(response_json)

                # TODO: Set up a proper exception handler to handle this
                raise Exception("No Generator found for unfinished state")

            gen = self.chat_obj.new_message_stream(message.question)
        return gen

    def create_message_from_json(self, json_str: str) -> Message:
        """
        Turns message string from json into a Message object.
        TODO: Do this via using kwargs**
        """
        # unpacking message of client
        message_dict = json.loads(json_str)

        session = message_dict.get("question_id")
        question = message_dict.get("question_text", "")
        client_question_state = message_dict.get("state", "")
        return Message(session, question, client_question_state)

    def process_message(self, json_message: str) -> Message:
        """
        Process the incoming message from the webserver client
        json_message[str]: decoded bytestring send via tcp
        """
        message: Message = Message.create_message_from_json(json_str=json_message)
        gen = self.get_generator(message)

        # create and attach generated response
        response, gen, state = self.question_response(gen=gen)
        message.response = response
        message.state = state

        # caching
        # TODO: prevent memory leaks due to too many cached gens,
        # also maybe find a way to do proper chaching
        if state == "finished":
            print(f"delete {message.session} from cached generators")
            if self.cached_generators.get(message.session, "None"):
                del self.cached_generators[message.session]
        else:
            print(f"cache generator of {message.session}")
            self.cached_generators[message.session] = gen
        return message

    def listen_for_client(self):
        """
        Creates the main loop of listening for clients to establish a connection.
        TODO: Make this less asyncronous.
        """
        socket = self.socket
        while True:
            byte_message = socket.recv()
            json_message: str = byte_message.decode("utf-8")
            if json_message:
                message: Message | None = None
                try:
                    message = self.process_message(json_message=json_message)
                except Exception as e:
                    # TODO do proper exception handling
                    print(f"some error while processing message occoured: {e}")

                # build the response
                if message is not None:
                    response_json = message.build_byte_response()
                    socket.send(response_json)
                    print("Received request: %s" % json_message)

            # timeout
            print("regular: ", json_message)
            time.sleep(1)


if __name__ == "__main__":
    DEFAULT_CHAT_MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"
    DEFAULT_TIMEOUT = 100000
    chat_server = ChatServer(DEFAULT_TIMEOUT, DEFAULT_CHAT_MODEL_NAME)
    chat_server.listen_for_client()
