#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import os
import sys
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from chat_api.gpt4all_chat import GPT4ALL, Chat

DEFAULT_CHAT_MODEL_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"
DEFAULT_TIMEOUT = 100000  
chat_obj = Chat(DEFAULT_CHAT_MODEL_NAME)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def question_response(gen):
    """
    This function aims to contribute to a quick visibly building response by generating response fragments word by word
    until a word limit is reached or a generation time limit is reached and then returns that fragment
    to the view handling the display of this message. 
    """
    # should probably depend on how many characters are already to be displayed
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

def build_json_reponse(session, response, state):
    chat_response = {
        "question_id": session,
        "response": response,
        "state": state,
    }
    print("response_json: ", chat_response)
    response_json = json.dumps(chat_response)
    response_json = response_json.encode("utf-8")
    return response_json

cached_generator = {}
print("start loop: ")
while True:
    message = socket.recv()
    message = message.decode("utf-8")
    if message:
        print("message: ", message)
        # unpacking message of client
        try:
            message_dict = json.loads(message)
        except Exception as e:
            print("not usable json: ", e)
        session = message_dict.get("question_id")
        question = message_dict.get("question_text")
        client_question_state = message_dict.get("state")

        # get or create generator and generate answer
        gen = cached_generator.get(session)
        if not gen:
            # makes sure a question that has already a generated part does not get generated anew again when the generator was not saved
            if client_question_state == "unfinished":
                state = "failed"
                response_json = build_json_reponse(session, "", state)
                socket.send(response_json)
                continue
            gen = chat_obj.new_message_stream(question)
        response, gen, state = question_response(gen=gen)

        # caching 
        # TODO: prevent memory leaks due to too many cached gens, also maybe find a way to do
        # proper chaching
        if state == "finished":
            print(f"delete {session} from cached generators")
            gen = cached_generator.get(session)
            if gen:
                cached_generator[session]
        else: 
            print(f"cache generator of {session}")
            cached_generator[session] = gen

        # build the response
        response_json = build_json_reponse(session, response, state)
        socket.send(response_json)
        print("Received request: %s" % message)
    # timeout
    print("regular: ", message)
    time.sleep(1)