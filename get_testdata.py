import chat_api.gpt4all_chat as gpt4all_chat


def print_out():
    """test the GPT4ALL class
    """

    gpt_object = gpt4all_chat.GPT4ALL("llama-2-7b-chat.ggmlv3.q4_0.bin")

    message = "The tests does not run on the right class."

    print("object", gpt_object)

    # test generate a message

    answer = gpt_object.generate('write a "Hello world" program in python')

    message = "The return of the network have the wrong datatype."

    print("answer", answer)


#answer 
 #Hinweis: This is just an example, you should not use this code as-is. It will not work as it stands. You need to replace the `print` statement with something that makes sense for your specific project.

#Here's an example of how you could write a "Hello world" program in Python:
#```
#print("Hello, World!")
#```
#This code will print the string `"Hello, World!"` when it is run. You can modify this code to suit your needs by changing the `print` statement with something else that makes sense for your project. For example, you could use a different message or add some logic to the program.

#Here's an example of how you could modify the code to print a personalized greeting:
#```
#name = "John"
#print("Hello, {}!".format(name))
#```
#This code will print `"Hello, John!"` when it is run,

    session = gpt_object.save_session()

    message = "saving the session returned the wrong datatype."

    print("session", session)

    print("dict", session[0])

#session [{'role': 'system', 'content': ''}]
#dict {'role': 'system', 'content': ''}

def print_chat_stream():
    chat = gpt4all_chat.Chat()
    while True:
        question = input("What do you want to ask? ")
        msg_stream = chat.new_message_stream(question)
        stream_array = []
        for word in msg_stream:
            stream_array.append(word)
            
        print("result_array", stream_array)
        print("new_message_stream", "\n")
        print("".join(stream_array))

        answer = chat.new_message(question)

        message = "The return of the network have the wrong datatype."

        print("new_message", answer)
    pass


 #Unterscheidung between Python 2 and Python 3.

#In Python 2, the following code will print "Hello World!":
#```
#print("Hello World!")
#```
#But in Python 3, it will raise a `NameError`:
#```
#print("Hello World!") # This will raise a NameError in Python 3
#```
#The reason for this difference is that in Python 2, the `print` statement was not a function, but an operator. In Python 3, it has been changed to a function, which raises a `NameError` when passed a string without quotes.

#To print a string in Python 3, you need to use quotes:
#```
#print("Hello World!") # This will work in Python 3
#```

if __name__ == "__main__":
    print_chat_stream()