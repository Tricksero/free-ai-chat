"""tests for the gpt4all chat api
"""
from pathlib import Path
import subprocess
import unittest
import gpt4all_test


class CliTest(unittest.TestCase):
    """tests for the GPT4ALL chat api

    Args:
        unittest (TestCase): unittest base class.
    """


    def test_class_gpt4all(self):
        """test the GPT4ALL class
        """

        gpt_object = gpt4all_test.GPT4ALL("llama-2-7b-chat.ggmlv3.q4_0.bin")

        message = "The tests does not run on the right class."

        self.assertIsInstance(gpt_object, gpt4all_test.GPT4ALL, message)

        # test generate a message

        answer = gpt_object.generate('write a "Hello world" program in python')

        message = "The return of the network have the wrong datatype."

        self.assertIsInstance(answer, str, message)


        # test save and load session

        # test save session

        session = gpt_object.save_session()

        message = "saving the session returned the wrong datatype."

        self.assertIsInstance(session, list, message)

        self.assertIsInstance(session[0], dict, message)

        # test load session

        gpt_object.load_session(session)






    def test_class_chat(self):
        """test the GPT4ALL class
        """

        chat_object = gpt4all_test.Chat("llama-2-7b-chat.ggmlv3.q4_0.bin")

        message = "The tests does not run on the right class."

        self.assertIsInstance(chat_object, gpt4all_test.Chat, message)

        # test generate a message

        answer = chat_object.new_message('write a "Hello world" program in python')

        message = "The return of the network have the wrong datatype."

        self.assertIsInstance(answer, str, message)

        answer = chat_object.new_message_stream('write a "Hello world" program in python')

        message = "The return of the network have the wrong datatype."

        self.assertEqual(str(type(answer)), "<class 'generator'>", message)

        # test save session

        session = chat_object.save_session()

        message = "saving the session returned the wrong datatype."

        self.assertIsInstance(session, list, message)

        self.assertIsInstance(session[0], dict, message)

        # test load session

        chat_object.load_session(session)

        # test change massage

        chat_object.change_msg('define cybersecurity', 0)

        new_session = chat_object.save_session()

        self.assertNotEqual(session, new_session, "changing session failed")

        # test change model

        chat_object.change_model("nous-hermes-13b.ggmlv3.q4_0.bin")

        new_session = chat_object.save_session()

        self.assertNotEqual(session, new_session, "changing model and keep session failed")

        answer = chat_object.new_message('write a "Hello world" program in python')

        message = "The return of the network have the wrong datatype after swapping model"

        self.assertIsInstance(answer, str, message)



    def test_miscellaneous_api_functions(self):
        """test all functions in the api.
        """

        check_download_working = gpt4all_test.download_model("ggml-model-gpt4all-falcon-q4_0.bin")

        message = "Given model download was expected."

        self.assertEqual(check_download_working, "ggml-model-gpt4all-falcon-q4_0.bin" + " is downloaded to " + gpt4all_test.get_save_path(), message)

        check_download_all_ready = gpt4all_test.download_model("ggml-model-gpt4all-falcon-q4_0.bin")

        message = "Given model is as all ready downloaded was expected."

        self.assertEqual(check_download_all_ready, "model all ready exist", message)

        # restlichen funktionen noch überprüfen



def run_pylint_and_mypy():
    """
    Run pylint and mypy tests
    """
    base_dir = Path(__file__).resolve().parent
    print(base_dir)
    subprocess.run(['pylint', base_dir], check=False)

    subprocess.run(['mypy', base_dir],  check=False)


# self.assertRaises(ValueError, function_that_raises) expect error
if __name__ == '__main__':
    unittest.main()
    run_pylint_and_mypy()
