from model import *
from files import *
import json

def add_parser_instructions(prompt: str, directory: str, history: str = ""):
  filenames = get_all_filenames(directory)
  detailed_prompt = (
    f"[START OF OLD CONVERSATION FOR CONTEXT]\n"
    f"{history}\n" if len(history) > 0 else ""
    f"[END OF OLD CONVERSATION]\n"
    f"You are an exceptional and forgiving parser. Your are here to detect any action that has to be taken on files. \n"
    f"Respond only with a valid JSON. Double-check its validity meticulously. Do not include any code blocks. Your response should be like a real API. \n"
    f"Response must be array of objects, each with:'\n"
    f"- filePath: The path of the file to be read, created, modified or deleted, moved or copied. \n"
    f"- query: The action that will be forwarded to another AI Agent so it must be as detailed as possible\n"
    f"- action: one of ['read','create', 'delete', 'modify', 'copy', 'rename'] \n"
    f"Other rules: \n"
    f"- User folder base path is {directory}. \n"
    f"- Accessible files for reference: {','.join(filenames)}. \n"
    f"IMPORTANT: Simply return an empty array if no action is found, it's perfectly fine.\n"
    f"User request: {prompt}"
)
  # print("_______Instructions________")
  # print(detailed_prompt)
  # print("_______________")
  return detailed_prompt

def parse_actions(prompt: str, directory: str, history: str = ""):
  try:
    instructions = add_parser_instructions(prompt, directory)
    json_response = get_response(instructions)
    try:
      return json.loads(json_response)
    except json.JSONDecodeError as e:
      print(f"JSON Format: {e}", json_response)
  except Exception as e:
    print(f"Parsing Error: {e}")
  return []
