import requests
import json
import os
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


def list_local_models():
    url = "http://ollama:9000/api/"

    response = requests.get(url + "tags")
    response = json.loads(response.text)

    return response

def new_message(model, msg,img: list = []):
    url = "http://ollama:9000/api/"
    data= {
  "model": model,
  "messages": [
    # {
    #   "role": "user",
    #   "content": "why is the sky blue?"
    # },
    # {
    #   "role": "assistant",
    #   "content": "due to rayleigh scattering."
    # },
    {
        "role": "user",
        "content": msg,
    }
  ],
  "images": img, # in einer Liste als base64 encoded
}

#     import base64

# # Function to encode an image file to base64
# def encode_image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#     return encoded_string

# # Path to your image file
# image_path = "path/to/your/image.jpg"

# # Encode the image to base64
# image_base64 = encode_image_to_base64(image_path)

    response = requests.post(url + "chat", json=data, stream= True)
    a = ""
    for line in response.iter_lines():
        if "error" in json.loads(line.decode()):
            print(json.loads(line.decode()))
            break
        os.system("clear")
        a += json.loads(line.decode())["message"]["content"]
        print(a)
        # print(json.loads(line.decode())["message"]["content"],type(json.loads(line.decode())))
        print("")



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


class api_chat:
    def __init__(self, modelname) -> None:
        # strucktur übernehmen. Über legen wie ich das am ende zusammen gefügt bekomme.
        # speed vergleich.
        pass

# Frage wie funktioniert das mit interschiedlichen chats die paralell laufen?

# Antwort:
# curl http://localhost:11434/api/chat -d '{
#   "model": "llama2",
#   "messages": [
#     {
#       "role": "user",
#       "content": "why is the sky blue?"
#     },
#     {
#       "role": "assistant",
#       "content": "due to rayleigh scattering."
#     },
#     {
#       "role": "user",
#       "content": "how is that different than mie scattering?"
#     }
#   ]
# }'
