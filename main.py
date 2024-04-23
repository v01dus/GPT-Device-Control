from openai import OpenAI
import json
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

model = "gpt-3.5-turbo-0125"

function_descriptions = [
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
                         "Coffee Machine",
                        "Bedroom Light",
                        "Refrigerator",
                        "Dishwasher",
                        "Vacuum Bot",
                        "Storage Light",
                        "Electric Kettle",
                        "Air Purifier"]
            },
            "command": {
                "type": "object",
                "properties": {
                    "idx": {
                        "type": "string",
                        "description": "Represents the specific control within the device. Only accepts on and off actions. You can toggle the kitchen light with index L1. To toggle coffee machine's coffee grinder using index L1 and coffee press using index L2. You can toggle the dishwasher's normal cycle with index L1, the quick cycle with index L2, and the delicate cycle with index L3. To toggle the bedroom light, use index L1. For the refrigerator, you can toggle normal cooling with index L1 and power-saving mode with index L2. Toggle cleaning mode 1 of the vacuum bot with index L1, mode 2 with index L2, and mode 3 with index L3. Use index L1 to toggle the storage light. The electric kettle's boiling function can be toggled with index L1, and the keep warm mode with index L2. Toggle mode 1 of the air purifier with index L1, mode 2 with index L2, and mode 3 with index L3.",
                        "enum": ["L1", "L2", "L3"]
                    },
                    "type": {
                        "type": "string",
                        "description": "Denotes the command type, such as 0x81 for on commands and 0x80 for off",
                        "enum": ["0x81", "0x80"]
                    },
                    "val": {
                        "type": "integer",
                        "description": "Represents the state to which the device should be set. Set value 0 for off commands and 1 for on.",
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
                    call one of your functions to complete the request. Invoke the functions only when the request aligns with the device's capabilities and known commands. If the request can not be completed by your available functions, use the reject_request function.
                    If the request is ambiguous, absurd, or unclear, use the reject_request function. Only use functions, do not reply with text that is not a function call."""


def control_device(device, idx, type_, val):
    """
    Controls various devices based on the input parameters.

    Parameters:
        device (str): The device to control.
        idx (str): The index or mode of the device.
        type_ (str): The type of action to perform on the device.
        val (int): The value indicating whether to turn on or off (1 or 0).

    Returns:
        str: A message indicating the action taken on the device.

    Note:
        - The function supports controlling different devices with specific conditions for each.
        - Handles turning devices on/off, setting modes, and starting/stopping cycles.
    """
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
        if idx in ["L1"]:
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

    # Vacuum Bot
    elif device == "Vacuum Bot":
        if idx in ["L1", "L2", "L3"]:
            if type_ == "0x81" and val == 1:
                return f"Started vacuum mode '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped vacuum mode '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Storage Light
    elif device == "Storage Light":
        if idx in ["L1"]:
            if type_ == "0x81" and val == 1:
                return f"Turned on the {device} at {idx}"
            elif type_ == "0x80" and val == 0:
                return f"Turned off the {device} at {idx}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Electric Kettle
    elif device == "Electric Kettle":
        if idx in ["L1", "L2"]:
            if type_ == "0x81" and val == 1:
                return f"Started boiling mode '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped boiling mode '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Air Purifier
    elif device == "Air Purifier":
        if idx in ["L1", "L2", "L3"]:
            if type_ == "0x81" and val == 1:
                return f"Started purifier mode '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped purifier mode '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"
    
    # Coffee Machine
    elif device == "Coffee Machine":
        if idx in ["L1", "L2"]:
            if type_ == "0x81" and val == 1:
                return f"Started preparing coffee with '{idx}' on the {device}"
            elif type_ == "0x80" and val == 0:
                return f"Stopped preparing coffee with '{idx}' on the {device}"
        else:
            return f"Invalid index '{idx}' for {device}"

    
     
    

def reject_request():
    """
    Returns a message for requests that couldn't be fulfilled.

    Returns:
        str: A message indicating inability to understand the request or no suitable function available.
    """

    
    return "Sorry, I couldn't understand your request or there's no suitable function available to fulfill it."


def ask_function_calling(model, query):
        """
        Calls a function based on the user query and model predictions.

        Parameters:
            model: The language model used for predictions.
            query (str): The user query to generate function calls.

        Returns:
            str or None: The function to be called based on model predictions,
                        or None if no suitable function is found.

        Note:
            - Constructs system and user messages.
            - Uses the language model to generate completions.
            - Parses model output to find tool calls and corresponding functions.
            - Returns the function to be called or None if not found.
        """
        messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=function_descriptions,
        )
        
        if completion and completion.choices:
            choice = completion.choices[0]
            if choice.message and choice.message.tool_calls:
                tool_call = choice.message.tool_calls[0]
                if tool_call and tool_call.function:
                    return tool_call.function
        
        # If any step is None, return None
        return None

        
user_query = " "
print('Model output: ', ask_function_calling(model, user_query))

