from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import requests
import sys
sys.path.append('devices')

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))


function_descriptions = [
    {
    "name": "control_kitchen_lights",
    "description": "Control only the kitchen lights.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on kitchen light switch.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,

{
    "name": "control_coffee_grinder",
    "description": "Control the coffee grinder of the Coffee Machine.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on the coffee grinder.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,
{
    "name": "control_coffee_press",
    "description": "Control the coffee press of the Coffee Machine.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on the coffee press.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,
{
    "name": "control_wash_delicate",
    "description": "Control the delicate wash setting of the Dishwasher.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on the delicate wash setting.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,
{
    "name": "control_wash_normal",
    "description": "Control the normal wash setting of the Dishwasher.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on the normal wash setting.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,
{
    "name": "control_wash_quick",
    "description": "Control the quick wash setting of the Dishwasher.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on the quick wash setting.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,
{
    "name": "control_bedroom_light",
    "description": "Control the bedroom Light.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform on the bedroom light.",
                "enum": ["on", "off"]
            }
        },
        "required": ["action"]
    }
}
,
{
    "name": "reject_request",
    "description": "Reject the user request if it's too ambiguous or there's no suitable function available.",
    "parameters": {},
    "returns": {
        "type": "string",
        "description": "Message indicating that the request is rejected."
    }
}




]



SYSTEM_PROMPT = """You are an intelligent AI that controls smart home devices. Given a command or request from the user,
call one of your functions to complete the request. If the request cannot be completed by your available functions, call the reject_request function.
If the request is ambiguous or unclear, reject the request."""



def ask_function_calling(query):
    messages = [{"role": "user", "content": query}]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    print(completion)




user_query = " "
ask_function_calling(user_query)