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
                "description": "Device name"
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
                        


# device_commands = {
#         "Turn on the kitchen light": {
#             "device": "Kitchen Light",
#             "command": {
#                 "idx": "L1",
#                 "type": "0x81",
#                 "val": 1
#             }
#         },
#         "Turn off the kitchen light": {
#             "device": "Kitchen Light",
#             "command": {
#                 "idx": "L1",
#                 "type": "0x80",
#                 "val": 0
#             }
#         },
#         "Turn on the bedroom light": {
#             "device": "Bedroom Light",
#             "command": {
#                 "idx": "L1",
#                 "type": "0x81",
#                 "val": 1
#             }
#         },
#         "Turn off the bedroom light": {
#             "device": "Bedroom Light",
#             "command": {
#                 "idx": "L1",
#                 "type": "0x80",
#                 "val": 0
#             }
#         },
#         "Turn on power saving mode for the refrigerator": {
#             "device": "Refrigerator",
#             "command": {
#                 "idx": "L2",
#                 "type": "0x81",
#                 "val": 1
#             }
#         },
#         "Turn off power saving mode for the refrigerator": {
#             "device": "Refrigerator",
#             "command": {
#                 "idx": "L2",
#                 "type": "0x80",
#                 "val": 0
#             }
#         },
#         "Start quick wash on the dishwasher": {
#             "device": "Dishwasher",
#             "command": {
#                 "idx": "L2",
#                 "type": "0x81",
#                 "val": 1
#             }
#         },
#         "Stop quick wash on the dishwasher": {
#             "device": "Dishwasher",
#             "command": {
#                 "idx": "L2",
#                 "type": "0x80",
#                 "val": 0
#             }
#         }
#     }


SYSTEM_PROMPT = """You are an intelligent AI that controls smart home devices. Given a command or request from the user,
call one of your functions to complete the request. If the request cannot be completed by your available functions or the request is ambiguous or unclear, reject the request."""



def control_device(device, idx, type_, val):
    
    if device == "Kitchen Light" or device == "Bedroom Light":
        if type_ == "0x81" and val == 1:
            return f"Turned on the {device}"
        elif type_ == "0x80" and val == 0:
            return f"Turned off the {device}"
    elif device == "Refrigerator":
        if type_ == "0x81" and val == 1:
            return "Started power saving mode for the refrigerator"
        elif type_ == "0x80" and val == 0:
            return "Stopped power saving mode for the refrigerator"
    elif device == "Dishwasher":
        if type_ == "0x81" and val == 1:
            return "Started quick wash on the dishwasher"
        elif type_ == "0x80" and val == 0:
            return "Stopped quick wash on the dishwasher"
    
    return "Invalid device or command"

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
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            # Extract device, idx, type_, val from the command argument
            device = function_args["device"]
            command = function_args["command"]
            idx = command["idx"]
            type_ = command["type"]
            val = command["val"]

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

# Test the updated ask_function_calling function
user_query = "refrigerator on saving mode"
print(ask_function_calling(user_query))
