
import os

from openai import OpenAI

class deepseekChat:
    def __init__(self, model="deepseek-chat", system_prompt=""):
        api_key = os.getenv("DEEPSEEK_APIKEY")
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.model = model
        self.system_prompt = system_prompt
        self.max_history = 30
        
        self.reset_messages()
    
    
    def chat(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        if len(self.messages) > self.max_history:
            if len(self.system_prompt) > 0:
                self.messages = [{"role": "system", "content": self.system_prompt}] + self.messages[-self.max_history+1:]
            else:
                self.messages = self.messages[-self.max_history:]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                # temperature=0.2, #?
                stream=False
            )

            answer = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": answer})
            return answer
        
        except Exception as e:
            return f"ERROR: {e}"

    
    def reset_messages(self):
        self.messages = []
        if len(self.system_prompt) > 0:
            self.messages.append({"role": "system", "content": self.system_prompt})

    
if __name__ == "__main__":
    chat_agent = deepseekChat()
    print(chat_agent.chat("Hello!"))
