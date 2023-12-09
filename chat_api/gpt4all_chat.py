"""
GPT4ALL chat API.
"""
import os
import requests # type: ignore
import gpt4all # type: ignore
from gpt4all import GPT4All as GPT4AllBaseClass # type: ignore

# ollama: curl http://ollama:9000

# gab ein gpt4all update da nach schauen, dass das dann wieder läuft?

# das hier testen
#ausprobieren, ob auch andere models von hugging face hier schon einlesbar sind.

# https://github.com/facebookresearch/llama/issues/483

# https://towardsdatascience.com/fine-tune-your-own-llama-2-model-in-a-colab-notebook-df9823a04a32?gi=88780445931c

# https://www.youtube.com/watch?v=LslC2nKEEGU

class GPT4ALL(GPT4AllBaseClass):
    """
    Base class for the chat class. Is not builded for usage.
    """
    def __init__(self, model_name: str,
                 model_path: str | None = None,
                 model_type: str | None = None,
                 allow_download: bool = True,
                 n_threads: int | None = None):
        """
        init the class.

        model_name (str): is the model name which should be used.
        model_path (str | None): default (None)
        optional path where the model is saved or should be saved.

        model_type (str | None): default (None)
        optional information which type the model is.

        allow_download (bool): default (True)
        if false the model will not be downloaded if its missing

        n_threads (int | None): default (None)
        is the number of threads which the model can use

        return None
        """
        super().__init__(model_name, model_path, model_type, allow_download, n_threads)

    def save_session(self) -> list[dict]: #[str][str] generic class draus machen
        """
        Give the current chat session.

        return list[dict[str][str]]
        """
        return self.current_chat_session

    def load_session(self, chat_session: list[dict]): # [str][str]
        """
        Loads an chat session.

        chat_session (list[dict[str][str]]):
        needs an old chat session to continue the chat.
        """
        self.current_chat_session = chat_session



class Chat:
    def __init__(self, model_name: str = "llama-2-7b-chat.ggmlv3.q4_0.bin", token = 200) -> None:
        self.model_name = model_name
        self.model = GPT4ALL(model_name)
        self.token = token
        self.model.chat_session()

    def new_message(self, msg: str):
        return self.model.generate(msg)

    def new_message_stream(self, msg: str):
        return self.model.generate(msg, streaming=True) #dringend testen

    def change_msg(self, new_msg: str, index: int):
        old_chat = self.model.save_session()
        new_chat = old_chat[:index]
        self.model.load_session(new_chat)
        self.model.generate(new_msg)

    def save_session(self) -> list:
        # das müsste alles sein
        return self.model.save_session()

    def load_session(self, chat_session: list):
        self.model.load_session(chat_session)


    def change_model(self, new_model_name):
        chat = self.model.save_session()
        self.model_name = new_model_name
        self.model = GPT4ALL(new_model_name)
        self.model.load_session(chat)


def download_model(model: str, max_retrys=5):
    # print(get_save_path()+"/"+model)
    if os.path.exists(get_save_path()+"/"+model):
        return "model all ready exist"

    model_name = gpt4all.gpt4all.append_extension_if_missing(model)
    try:
        GPT4AllBaseClass.download_model(
                model_name, get_save_path())
    except requests.exceptions.ChunkedEncodingError:
        if 0 < max_retrys:
            download_model(model, max_retrys-1)
        else:
            return f"the model {model} was requested but unable to download"

    return model + " is downloaded to " + get_save_path()

def get_list_of_all_models() -> dict:
    return GPT4ALL.list_models() # zweiter return wert für details über locale

def download_all_models():
    model_names = [model["filename"] for model in get_list_of_all_models()]
    response = [download_model(model_name) for model_name in model_names]
    return response


def get_save_path():
    return gpt4all.gpt4all.DEFAULT_MODEL_DIRECTORY

def local_models():
    return [i for i in os.listdir(get_save_path()) if ".bin" in i]



if __name__ == "__main__":
    download_model("llama-2-7b-chat.ggmlv3.q4_0.bin")
