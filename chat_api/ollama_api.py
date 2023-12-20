import requests
import json

# model list https://ollama.ai/library


# curl http://ollama:9000/api/pull -d '{"name": "llama2"}'

def download_model(modelname):
    url = "http://ollama:9000/api/"
    data = {"name": modelname}

    response = requests.post(url + "pull", json=data, stream= True)
    for line in response.iter_lines():
        print(json.loads(line.decode()),type(json.loads(line.decode())))
        print("")

    # response = json.loads(response.text)
    # local_model_list = [ model["name"].split(":")[0] for model in response["models"]]
    # return modelname.split(":")[0] in local_model_list


def local_models():
    url = "http://ollama:9000/api/"

    response = requests.get(url + "tags")
    response = json.loads(response.text)

    return response


def create_init_promt(name, base_model, init_promt):
    url = "http://ollama:9000/api/"
    data = {
        "name": name,
        "modelfile": f"From {base_model}\nSYSTEM {init_promt}"
    }
    response = requests.post(url + "create", json=data)

    for line in response.iter_lines():

        print(json.loads(line.decode()))
        print("")



class Chat:
    def __init__(self, model_name: str = "llama2") -> None:
        self.model_name = model_name
        self.chat_session = []

    def new_message(self, msg,img: list = []):
        url = "http://ollama:9000/api/"
        self.chat_session.append(

                {
                    "role": "user",
                    "content": msg,
                }
            )
        data= {
            "model": self.model_name,
            "messages": self.chat_session,
    "images": img, # in einer Liste als base64 encoded
    }

        response = requests.post(url + "chat", json=data)
        return response.text

    def new_message_stream(self, msg,img: list = []):
        self.chat_session.append(

                {
                    "role": "user",
                    "content": msg,
                }
            )
        url = "http://ollama:9000/api/"
        data= {
            "model": self.model_name,
            "messages": self.chat_session,
    "images": img, # in einer Liste als base64 encoded
    }
        response = requests.post(url + "chat", json=data, stream= True)
        for line in response.iter_lines():
            if "error" in json.loads(line.decode()):
                yield json.loads(line.decode())
                break

            yield json.loads(line.decode())["message"]["content"]


    def change_msg(self, new_msg: str, index: int):
        old_chat = self.chat_session
        self.chat_session = old_chat[:index]
        return self.new_message_stream(new_msg)

    def save_session(self) -> list:
        # das müsste alles sein
        return self.chat_session

    def load_session(self, chat_session: list):
        self.chat_session = chat_session


    def change_model(self, new_model_name):
        self.model_name = new_model_name