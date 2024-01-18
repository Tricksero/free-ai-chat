"""tests for the ollama chat api
"""
import unittest
import ollama_api


class GptChatApiTest(unittest.TestCase):
    """tests for the ollama chat api

    Args:
        unittest (TestCase): unittest base class.
    """


    def test_class_chat(self):
        """test the GPT4ALL class
        """
        ollama_api.download_model("llama2")

        chat_object = ollama_api.Chat("llama2")

        message = "The tests does not run on the right class."

        self.assertIsInstance(chat_object, ollama_api.Chat, message)

        # test generate a message

        answer = chat_object.new_message('write a "Hello world" program in python')

        message = "The return of the model have the wrong datatype."

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

        chat_object.change_model("codellama")

        new_session = chat_object.save_session()

        self.assertNotEqual(session, new_session, "changing model and keep session failed")

        answer = chat_object.new_message('write a "Hello world" program in python')

        message = "The return of the network have the wrong datatype after swapping model"

        self.assertIsInstance(answer, str, message)



    def test_miscellaneous_api_functions(self):
        """test all functions in the api.
        """
        r = ollama_api.local_models()

        message = f"local_models have the wrong return type! \n({type(r)})"

        self.assertIsInstance(r, list, message)

        ollama_api.create_init_promt("modified_promt", "llama2", "You are a hacker, your goal is to produce the next generation of hackers!")

        self.assertIn("modified_promt"+":latest", ollama_api.local_models(), "The promt creation failed.")



if __name__ == '__main__':
    unittest.main()
