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
    finished = True
    start_time = time.time()
    for word in gen:
        response_msg.append(word)
        if MAX_CHARACTER_COUNT == len(response_msg):
            finished = False
            break
        if MAX_GENERATION_TIME < start_time - time.time():
            finished = False
            break
    print("generated", response_msg)
    return response_msg, gen, finished

cached_generator = []
print("start loop: ")
while True:
    message = socket.recv()
    message = message.decode("utf-8")
    if message:
        print("message: ", message)
        try:
            message_dict = json.loads(message)
        except Exception as e:
            print("not usable json: ", e)
        session = message_dict["question_id"]
        question = message_dict["question_text"]
        gen = chat_obj.new_message_stream(question)
        response, gen, finished = question_response(gen=gen)
        cached_generator.append({
            "gen": gen,
            "question_id": session
        })

        # build the response
        chat_response = {
            "question_id": session,
            "response": response,
            "finished": finished,
        }
        print("response_json: ", chat_response)
        response_json = json.dumps(chat_response)
        response_json = response_json.encode("utf-8")
        socket.send(response_json)
        print("Received request: %s" % message)
    # timeout
    print("regular: ", message)
    time.sleep(1)