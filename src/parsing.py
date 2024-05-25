from model import *
from files import *
import json

def add_parser_instructions(prompt: str, directory: str, history: str = ""):
  filenames = get_all_filenames(directory)
  detailed_prompt = (
    f"Old conversation for context to help you understand last request better: {history}" if len(history) > 0 else ""
    f"You are an exceptional and forgiving parser. Your task is to extract the actions, files involved, and a summary of the action from the user request. \n"
    f"Respond only with a valid JSON. Double-check its validity meticulously. Do not include any code blocks. Your response should be like a real API. \n"
    f"Response must be array of objects, each with:'\n"
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

def parse_actions(prompt: str, directory: str, history: str = ""):
  try:
    instructions = add_parser_instructions(prompt, directory, history)
    json_response = get_response(instructions)
    actions = json.loads(json_response)
  except Exception as e:
    print(f"Parsing Error: {e}")
    actions = []
  return actions
