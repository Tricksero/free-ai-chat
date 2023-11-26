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

def send_question(question):
    context = zmq.Context()

    #  Socket to talk to server
    print("Connect...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.CONNECT_TIMEOUT, 5000)
    print("Connected")
    #socket.RCVTIMEO = 20000

    question_dict = {
        "question_text": question.question,
        "question_id": str(question.id),
        "state": question.state,
    }
    question_dict = json.dumps(question_dict)
    question_dict = question_dict.encode("utf-8")
    print("send: ", question.question)
    socket.send(question_dict)

    message = socket.recv()
    message = message.decode("utf-8")
    message_dict = json.loads(message)
    text = message_dict.get("response")
    state = message_dict.get("state")
    resulting_text = "".join(text)
    print(f"Received reply {question_dict} [ {resulting_text} ] {state}")
    return resulting_text, state

class TCPClientTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_send_question(self):
        send_question(TEST_QUESTION, ID)

if __name__ == "__main__":
    unittest.main()
    pass