import gpt4all_chat
import os


models_list = gpt4all_chat.local_models()
problems = []
for model in models_list:
    print(f"model: {models_list.index(model)}/{len(models_list)}")
    # if model in ["ggml-all-MiniLM-L6-v2-f16.bin", "starcoderbase-3b-ggml.bin", "llama-2-7b-chat.ggmlv3.q4_0.bin","nous-hermes-13b.ggmlv3.q4_0.bin"]:
    #     continue
    try:
        chat = gpt4all_chat.Chat(model)
        response = chat.new_message("What is the different between GPU and CPU for AI training?")
        print(f"The model: {model}\n answer: {response}")
    except Exception as e:
        print(e)
        problems.append(model)
print("fertig")


print(problems)
print(len(problems))