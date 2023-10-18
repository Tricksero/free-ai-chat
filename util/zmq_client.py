#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

# TODO: maybe add faker tests
import zmq
import json
import unittest
from unittest import TestCase

TEST_QUESTION = "Show me a hello world program in python."
ID = "12"

def send_question(id: str, question: str=""):
    context = zmq.Context()

    #  Socket to talk to server
    print("Connect...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    print("Connected")

    question = question
    question_dict = {
        "question_text": question,
        "question_id": id
    }
    question_dict = json.dumps(question_dict)
    question_dict = question_dict.encode("utf-8")
    print("send: ", question)
    socket.send(question_dict)

    message = socket.recv()
    message = message.decode("utf-8")
    message_dict = json.loads(message)
    text = message_dict["question_text"]
    finished = message_dict["finished"]
    resulting_text = "".join(text)
    print("Received reply %s [ %s ]" % (question_dict, resulting_text, finished))
    return resulting_text, finished

class TCPClientTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_send_question(self):
        send_question(TEST_QUESTION, ID)

if __name__ == "__main__":
    unittest.main()
    pass