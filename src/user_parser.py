from model import *
from files_manip import *
import json

def add_parser_instructions(prompt, directory):
  filenames = get_all_filenames(directory)
  detailed_prompt = (
    f"You are an exceptional and forgiving parser. Your task is to extract the actions, files involved, and a summary of the action from the user request. \n"
    f"Respond only with a valid JSON. Double-check its validity meticulously. Do not include any code blocks. Your response should be like a real API. \n"
    f"1. 'response': Provide a clean response confirming that the requested actions have been applied. \n"
    f"2. 'actions': An array of objects, each with:'\n"
    f"- query: The details of the action that should be done on the file, or in case of reading what information to extract, conserve all important information! Should always be at least 20 characters\n"
    f"- filePath: The path of the file to be read, created, modified or deleted. \n"
    f"- action: one of ['read','create', 'delete', 'modify', 'copy', 'rename'] \n"
    f"Other rules: \n"
    f"- User folder base path is {directory}. \n"
    f"- Accessible files for reference: {','.join(filenames)}. \n"
    f"IMPORTANT: Last but not least, if no action on file is detected, respond just as normal, just return empty array\n"
    f"User request: {prompt}"
)
  # print("_______Instructions________")
  # print(detailed_prompt)
  # print("_______________")
  return detailed_prompt

def parse_actions(prompt, directory):
  instructions = add_parser_instructions(prompt, directory)
  json_response = get_response(instructions)
  try:
    response_data = json.loads(json_response)
    actions = response_data.get('actions', [])
    user_response = response_data.get('response', '')
  except json.JSONDecodeError as e:
    print(f"Error parsing JSON response: {e}", json_response)
    actions = []
    user_response = "Error with the exchange"
  return (actions, user_response)
