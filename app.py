import openai
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def ask_function_calling(query):
    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    print(response)

user_query = "Turn on the light"
ask_function_calling(user_query)