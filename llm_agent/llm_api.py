import os.path
import asyncio
from google import genai
import json

class LLM_AGENT:
    def __init__(self, CONFIG_FILE=None):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())

        if not CONFIG_FILE:
            CONFIG_FILE = 'config.json'

        config = {}
        if not os.path.exists(CONFIG_FILE):
            raise Exception(f'CONFIG_FILE {CONFIG_FILE} does\'t exist')

        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        if config:
            self.client = genai.Client(api_key=config["API_KEY"])
        else:
            raise Exception(f'Fail to get LLM Client')

        self.all_tokens = 0
        self.current_tokens = 0
        print("llm_agent initialization success")

    def call_llm(self, question):
        try:
            response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question,
            )
            self.current_tokens = response.usage_metadata.total_token_count
            self.all_tokens += self.current_tokens
            return response.text
        except Exception as e:
            raise Exception(f'LLM call fail, error:{e}')

    def test_llm_agent(self, question=None):
        if not question:
            question = "What is your name?"
        answer = self.call_llm(question)

        print("Question: {}".format(question))
        print("LLM answer: {}".format(answer))

if __name__ == "__main__":
    CONFIG_FILE = 'config.json'
    llm_agent = LLM_AGENT(CONFIG_FILE)
    llm_agent.test_llm_agent()