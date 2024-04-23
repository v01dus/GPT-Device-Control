import jsonlines
import os
import csv
from openai import OpenAI
from dotenv import load_dotenv
import json
from sklearn.model_selection import train_test_split


model = "gpt-3.5-turbo-0125"

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))


function_descriptions = [
    {
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
    },
                         
    {
            "name": "reject_request",
            "description": "Reject the user request if it's too ambiguous or there's no suitable function available.",
            "parameters": {}
        }
    
]



def load_csv_finetuning(csv_file, output_path):
    """
    Reads a CSV file containing system, user, and function call data,
    then writes it to a JSONL file in a specific format.

    Parameters:
        csv_file (str): Path to the CSV file with system, user, and function call data.
        output_path (str): Path to the output JSONL file.

    Note:
        - Converts each row of CSV to a JSONL format with messages and function descriptions.
        - Supports "control_device" and "reject_request" functions based on CSV columns.
    """
    # Open the CSV file for reading
    with open(csv_file, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Open the JSONL file for writing
        with jsonlines.open(output_path, mode='w') as jsonl_file:
            for row in csv_reader:
                system = row[0]
                values = [{"role": "system", "content": system}]
                values.append({"role": "user", "content": row[1]})
                if row[2] == "reject_request":     
                    values.append({"role": "assistant", "function_call": {"name": row[2], "arguments": "{}"}})
                elif row[2] == "control_device":
                     values.append({"role": "assistant", "function_call": {"name": row[2], "arguments": f'{{"device":"{row[3]}","command":{{"idx":"{row[4]}","type":"{row[5]}","val":{row[6]}}}}}'}})

               
                json_data = {"messages":values, "functions": function_descriptions}
                jsonl_file.write(json_data)
                



def split_jsonl(input_file, split_ratio=0.8):
    """
    Splits a JSONL file into training and validation sets.

    Parameters:
        input_file (str): Path to the input JSONL file.
        split_ratio (float): Ratio of training to validation data (default: 0.8).

    Note:
        - Reads the JSONL file and splits the lines into training and validation sets.
        - Writes the split data to 'train.jsonl' and 'val.jsonl'.
    """   
    with open(input_file, 'r') as jsonl_file:
        lines = jsonl_file.readlines()


    train_lines, val_lines = train_test_split(lines, train_size=split_ratio, random_state=42)


    with open('train.jsonl', 'w') as train_file:
        train_file.writelines(train_lines)


    with open('val.jsonl', 'w') as val_file:
        val_file.writelines(val_lines)




if __name__ == '__main__':
    fine_tuning_data = "input.jsonl"
    load_csv_finetuning("dataset.csv", fine_tuning_data)
    split_jsonl('input.jsonl', split_ratio=0.8)
    
