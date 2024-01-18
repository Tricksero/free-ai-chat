from gpt4all_chat import Chat as gpt4all_chat
from ollama_api import Chat as ollama_chat



class ChatWrapper:
    def __init__(self,model_name, api_kind):
        self.api_kind = api_kind
        if api_kind == "ollama":
            self._wrapped_instance = ollama_chat(model_name)
        else:
            self._wrapped_instance = gpt4all_chat(model_name)



    def new_message(self, msg,img: list = []):
        if self.api_kind == "ollama":
            return self._wrapped_instance.new_message(msg,img)

        return self._wrapped_instance.new_message(msg)


    def new_message_stream(self, msg,img: list = []):
        # print("1")
        # print(msg, self._wrapped_instance.chat_session)
        if self.api_kind == "ollama":
            return self._wrapped_instance.new_message_stream(msg,img)

        return self._wrapped_instance.new_message_stream(msg)


    def change_msg(self, new_msg: str, index: int):

        return self._wrapped_instance.change_msg(new_msg, index)

    def save_session(self) -> list:

        return self._wrapped_instance.save_session()

    def load_session(self, chat_session: list):
        self._wrapped_instance.load_session(chat_session)


    def change_model(self, new_model_name):
        self._wrapped_instance.change_model(new_model_name)
