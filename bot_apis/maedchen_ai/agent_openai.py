#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 11:23:55 2023

@author: eee
"""
import os
import json

import requests

from utils.datetime_tools import get_today_date

class ChatGPTAgent:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_host = os.getenv("OPENAI_API_BASE")
        self.knowledge_cutoff = os.getenv("KNOWLEDGE_CUTOFF") # 2021-09
        
        self.chat_url = f'{self.api_host}/v1/chat/completions'
        self.headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json',
        }
        self.init_prompt = "Hello! Good to see you there!"
        
        self.token_thresh = 8192
        self.messages = []
        
    def chat(self, message, model):
        self.messages.append({"role": "user", "content": message})
        try:
            data = {
                "model": model,
                "stream": False,
                "messages": self.messages,
                "temperature": 0.2,
                "max_tokens": 2000,
            }
            d = json.dumps(data)
            response = requests.post(self.chat_url, headers=self.headers, data=d, timeout=300)
            content = response.json()["choices"][0]["message"]["content"]
            total_tokens = response.json()["usage"]["total_tokens"]
            if total_tokens >= self.token_thresh:
                self.messages = self.messages[1:]
            self.messages.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            return f"ERROR: {e}"

    def start(self, model):
        system_prompt = f"""You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.
            Knowledge cutoff: {self.knowledge_cutoff}
            Current date: {get_today_date()}"""
        self.messages = [{"role": "system", "content": system_prompt}]
        return self.chat(self.init_prompt, model)


if __name__ == "__main__":
    c = ChatGPTAgent()
    c.chat("hello there")
    print(c.chat("can you show me how to write a recursive function in python?"))
