from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import requests


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))



tools = [
    {
        "type": "function",
        "function": {
    "name": "control_device",
    "description": "Control a smart home device",
    "parameters": {
        "type": "object",
        "properties": {
            "device": {
                "type": "string",
                "description": "Device name",
                "enum": ["Kitchen Light",
                        "Bedroom Light",
                        "Refrigerator",
                        "Dishwasher",
                        "Vacuum Bot",
                        "Nature Hub",
                        "Storage Light",
                        "Electric Kettle",
                        "Air Purifier"]
            },
            "command": {
                "type": "object",
                "properties": {
                    "idx": {
                        "type": "string",
                        "description": "Command index",
                        "enum": ["L1", "L2", "L3"]
                    },
                    "type": {
                        "type": "string",
                        "description": "Command type",
                        "enum": ["0x81", "0x80"]
                    },
                    "val": {
                        "type": "integer",
                        "description": "Command value",
                        "enum": [0, 1]
                    }
                },
                "required": ["idx", "type", "val"]
            }
        },
        "required": ["device", "command"]
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
call one of your functions to complete the request. If the request cannot be completed by your available functions. Ask for clarification if a user request is ambiguous."""


def control_device(device, idx, type_, val):
    # Kitchen Light
    if device == "Kitchen Light":
        if idx in ["L1"]:
            if type_ == "0x81" and val == 1:
                return f"Turned on the {device} at {idx}"
            elif type_ == "0x80" and val == 0:
                return f"Turned off the {device} at {idx}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Bedroom Light
    elif device == "Bedroom Light":
        if idx in ["L1", "L2"]:
            if type_ == "0x81" and val == 1:
                return f"Turned on the {device} at {idx}"
            elif type_ == "0x80" and val == 0:
                return f"Turned off the {device} at {idx}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Refrigerator
    elif device == "Refrigerator":
        if idx in ["L1", "L2"]:
            if type_ == "0x81" and val == 1:
                return f"Started power saving mode for the {device} at {idx}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped power saving mode for the {device} at {idx}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Dishwasher
    elif device == "Dishwasher":
        if idx in ["L1", "L2", "L3"]:
            if type_ == "0x81" and val == 1:
                return f"Started wash cycle '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped wash cycle '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"

    elif device == "Vacuum Bot":
        # Example command for Vacuum Bot
        if idx in ["L1", "L2", "L3"]:
            if type_ == "0x81" and val == 1:
                return f"Started vacuum mode '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped vacuum mode '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    elif device == "Storage Light":
        if idx in ["L1"]:
            if type_ == "0x81" and val == 1:
                return f"Turned on the {device} at {idx}"
            elif type_ == "0x80" and val == 0:
                return f"Turned off the {device} at {idx}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    elif device == "Electric Kettle":
        if idx in ["L1", "L2"]:
            if type_ == "0x81" and val == 1:
                return f"Started boiling mode '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped boiling mode '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    elif device == "Air Purifier":
        if idx in ["L1", "L2", "L3"]:
            if type_ == "0x81" and val == 1:
                return f"Started purifier mode '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped purifier mode '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"
        
    

def reject_request():
    
    return "Sorry, I couldn't understand your request or there's no suitable function available to fulfill it."

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
            "control_device": control_device,
            "reject_request": reject_request
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            if function_to_call is None:
                # If function is not found, call reject_request
                reject_response = reject_request()
                messages.append(
                    {
                        "role": "tool",
                        "name": "reject_request",
                        "content": reject_response,
                    }
                )
                continue
            
            function_args = json.loads(tool_call.function.arguments)

            # Extract device, idx, type_, val from the command argument
            device = function_args.get("device")
            command = function_args.get("command", {})
            idx = command.get("idx")
            type_ = command.get("type")
            val = command.get("val")

            if function_name == "reject_request":
                # If calling reject_request, do not pass any arguments
                function_response = function_to_call()
            else:
                function_response = function_to_call(device, idx, type_, val)
                
           
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

    return response



user_query = "vacuum in mode 2, after you are done turn off the vacuum cleaner"
print(ask_function_calling(user_query))

