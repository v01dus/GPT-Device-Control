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

def control_kitchen_lights(action: str):
    if action == 'on':
       
        return "Kitchen lights turned on."
    
    elif action == 'off':
       
        return "Kitchen lights turned off."
    
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_wash_normal(action: str):
    """
    Control the normal wash setting of the Dishwasher.

    Parameters:
        action (str): Action to perform on the normal wash setting. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the normal wash setting.
    """
    if action == 'on':
        return "Normal wash setting turned on."
    elif action == 'off':
        return "Normal wash setting turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_wash_quick(action: str):
    """
    Control the quick wash setting of the Dishwasher.

    Parameters:
        action (str): Action to perform on the quick wash setting. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the quick wash setting.
    """
    if action == 'on':
        return "Quick wash setting turned on."
    elif action == 'off':
        return "Quick wash setting turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_wash_delicate(action: str):
    """
    Control the delicate wash setting of the Dishwasher.

    Parameters:
        action (str): Action to perform on the delicate wash setting. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the delicate wash setting.
    """
    if action == 'on':
        return "Delicate wash setting turned on."
    elif action == 'off':
        return "Delicate wash setting turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."

def control_bedroom_light(action: str):
    """
    Control the Bedroom Light.

    Parameters:
        action (str): Action to perform on the bedroom light. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the bedroom light.
    """
    if action == 'on':
        return "Bedroom light turned on."
    elif action == 'off':
        return "Bedroom light turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."

def control_coffee_grinder(action: str):
    """
    Control the coffee grinder of the Coffee Machine.

    Parameters:
        action (str): Action to perform on the coffee grinder. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the coffee grinder.
    """
    if action == 'on':
        return "Coffee grinder turned on."
    elif action == 'off':
        return "Coffee grinder turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."


def control_coffee_press(action: str):
    """
    Control the coffee press of the Coffee Machine.

    Parameters:
        action (str): Action to perform on the coffee press. Valid values are 'on' or 'off'.

    Returns:
        str: Confirmation message indicating the action performed on the coffee press.
    """
    if action == 'on':
        return "Coffee press turned on."
    elif action == 'off':
        return "Coffee press turned off."
    else:
        return "Invalid action. Please specify 'on' or 'off'."

def reject_request():
    """
    Reject the user request if it's too ambiguous or there's no suitable function available.

    Returns:
        str: Message indicating that the request is rejected.
    """
    return "Sorry, I couldn't understand your request or there's no suitable function available to fulfill it."




tools = [
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "reject_request",
            "description": "Reject the user request if it's too ambiguous or there's no suitable function available.",
            "parameters": {},
            "returns": {
                "type": "string",
                "description": "Message indicating that the request is rejected."
            }
        }
    }
]




SYSTEM_PROMPT = """You are an intelligent AI that controls smart home devices. Given a command or request from the user,
call one of your functions to complete the request. If the request cannot be completed by your available functions, call the reject_request function.
If the request is ambiguous or unclear, reject the request."""



def ask_function_calling(query):
        messages = [{"role": "user", "content": query}]
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
    
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "control_kitchen_lights": control_kitchen_lights,
                "control_coffee_grinder": control_coffee_grinder,
                "control_coffee_press": control_coffee_press,
                "control_wash_delicate": control_wash_delicate,
                "control_wash_normal": control_wash_normal,
                "control_wash_quick": control_wash_quick,
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
                
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            return second_response
        

user_query = "make me coffee"
print(ask_function_calling(user_query))