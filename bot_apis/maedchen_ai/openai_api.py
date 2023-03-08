

import os
import openai

proxy = 'http://127.0.0.1:8889'
for k in ["HTTP_PROXY", "HTTPS_PROXY"]:
    os.environ[k] = proxy
    os.environ[k.lower()] = proxy

class ChatApp:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = [
            {"role": "system", "content": "You are a charming and heart-warning chat bot."},
        ]

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]

if __name__ == "__main__":
    c = ChatApp()
    c.chat("hello there")
    print(c.chat("can you show me how to write a recursive function in python?"))
