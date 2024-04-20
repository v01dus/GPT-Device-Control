from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import requests
import sys
sys.path.append('devices')
import devices

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

def control_kitchen_lights(state: str):
    if state == 'on':
       
        return "Kitchen lights turned on."
    
    elif state == 'off':
       
        return "Kitchen lights turned off."
    
    else:
        return "Invalid state. Please specify 'on' or 'off'."


def dishwasher_normal(state: str):

    if state == 'on':
        return "Normal wash setting turned on."
    elif state == 'off':
        return "Normal wash setting turned off."
    else:
        return "Invalid state. Please specify 'on' or 'off'."


def dishwasher_quick(state: str):

    if state == 'on':
        return "Quick wash setting turned on."
    elif state == 'off':
        return "Quick wash setting turned off."
    else:
        return "Invalid state. Please specify 'on' or 'off'."


def dishwasher_delicate(state: str):
   
    if state == 'on':
        return "Delicate wash setting turned on."
    elif state == 'off':
        return "Delicate wash setting turned off."
    else:
        return "Invalid state. Please specify 'on' or 'off'."

def control_bedroom_light(state: str):
  
    if state == 'on':
        return "Bedroom light turned on."
    elif state == 'off':
        return "Bedroom light turned off."
    else:
        return "Invalid state. Please specify 'on' or 'off'."

def control_coffee_grinder(state: str):
  
    if state == 'on':
        return "Coffee grinder turned on."
    elif state == 'off':
        return "Coffee grinder turned off."
    else:
        return "Invalid state. Please specify 'on' or 'off'."


def control_coffee_press(state: str):
   
    if state == 'on':
        return "Coffee press turned on."
    elif state == 'off':
        return "Coffee press turned off."
    else:
        return "Invalid state. Please specify 'on' or 'off'."

def reject_request():
    
    return "Sorry, I couldn't understand your request or there's no suitable function available to fulfill it."




tools = [
    {
        "type": "function",
        "function": {
            "name": "control_kitchen_lights",
            "description": "Switch only the kitchen lights.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the kitchen light switch.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_coffee_grinder",
            "description": "Control the coffee grinder of the Coffee Machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the coffee grinder.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_coffee_press",
            "description": "Control the coffee press of the Coffee Machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the coffee press.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dishwasher_delicate",
            "description": "Control the delicate wash setting of the Dishwasher for plates, bowls, and utensils.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the delicate wash setting.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dishwasher_normal",
            "description": "Control the normal wash setting of the Dishwasher for plates, bowls, and utensils.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the normal wash setting.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dishwasher_quick",
            "description": "Control the quick wash setting of the Dishwasher for plates, bowls, and utensils.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the quick wash setting.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_bedroom_light",
            "description": "Control only the bedroom Light.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "State of the bedroom light.",
                        "enum": ["on", "off"]
                    }
                },
                "required": ["state"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reject_request",
            "description": "Reject the user request if it's too ambiguous or there's no suitable function available.",
            "parameters": {}
        }
    }
]




SYSTEM_PROMPT = """You are an intelligent AI that controls smart home devices. Given a command or request from the user,
call one of your functions to complete the request. If the request cannot be completed by your available functions, call the reject_request function.
If the request is ambiguous or unclear, reject the request."""



def ask_function_calling(query):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "control_kitchen_lights": control_kitchen_lights,
            "control_coffee_grinder": control_coffee_grinder,
            "control_coffee_press": control_coffee_press,
            "dishwasher_delicate": dishwasher_delicate,
            "dishwasher_normal": dishwasher_normal,
            "dishwasher_quick": dishwasher_quick,
            "control_bedroom_light": control_bedroom_light,
            "reject_request": reject_request
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        return response  # Return the response after executing the function




user_query = "wash my clothes delicately"
print(ask_function_calling(user_query))