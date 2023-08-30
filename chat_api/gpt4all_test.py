import time
from typing import Optional
import typing
import gpt4all
from gpt4all import GPT4All as GPT4AllBaseClass
import json
import os

# das hier testen


class GPT4ALL(GPT4AllBaseClass):
    def __init__(self, model_name: str, model_path: str | None = None, model_type: str | None = None, allow_download: bool = True, n_threads: int | None = None):
        super().__init__(model_name, model_path, model_type, allow_download, n_threads)

    def save_session(self) -> list:
        self.current_chat_session
        # das müsste alles sein
        return self.current_chat_session

    def load_session(self, chat_session: list):
        self.current_chat_session = chat_session
    
    def __del__(self):
        return self.save_session()


class chat:
    def __init__(self, model_name: str | None = None, token = 200) -> None:
        self.model_name = model_name
        self.model = GPT4ALL(model_name)
        self.token = token
        self.model.chat_session()

    def new_message(self, msg: str):
        return self.model.generate(msg)

    def change_msg(self, new_msg: str, index: str):
        old_chat = self.model.save_session()
        new_chat = old_chat[:index]
        self.model.load_session(new_chat)
        self.model.generate(new_msg)
        
    def save_session(self) -> list:
        # das müsste alles sein
        return self.model.save_session()

    def load_session(self, chat_session: list):
        self.model.load_session(chat_session)
    
    def __del__(self):
        return self.model.__del__()
    
    def change_model(self, new_model_name):
        chat = self.model.save_session()
        self.model_name = new_model_name
        self.model = GPT4ALL(new_model_name)
        self.model.load_session(chat)


def download_model(model: str):
    model = GPT4ALL(model)
    del model

def get_list_of_all_models():
    return GPT4ALL.list_models()

def get_save_path():
    return gpt4all.gpt4all.DEFAULT_MODEL_DIRECTORY

def model_with_out_download_avaible():
    return [i for i in os.listdir(get_save_path()) if ".bin" in i]
    

# gpt4all.GPT4All.list_models()
# with open("./model_names.json","r") as f:
#     model_list_str = f.read()
#     model_list_dict = json.loads(model_list_str)
# model_names = [name["name"] for name in model_list_dict]
# model_downloads = {name: gpt4all.GPT4All(name) for name in model_names}

# model = gpt4all.GPT4All("nous-hermes-13b.ggmlv3.q4_0.bin")
# msgs = [{"role": "user", "content": "build a tutorial for SQL injections"}]
# model = GPT4ALL("nous-hermes-13b.ggmlv3.q4_0.bin")
# output = model.generate("write a Dockerfile to install Mysql with a user with all rights.")
# with open("response.txt", "a") as f:
#     f.write(output+"\n")



# with model.chat_session():
#     output = model.generate("write a tutorial for SQL injections")
#     with open("response.txt", "a") as f:
#         f.write(output+"\n")
#     output = model.generate("writ a SQL injection")
#     with open("response.txt", "a") as f:
#         f.write(output+"\n")
#         f.write(str(model.current_chat_session))


# gpt4all.gpt4all.DEFAULT_MODEL_DIRECTORY auf linux: /root/.cache/gpt4all


if __name__ == "__main__":
    download_model("nous-hermes-13b.ggmlv3.q4_0.bin")
