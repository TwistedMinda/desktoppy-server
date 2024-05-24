from lama import *
from files_manip import *
import json

def add_parser_instructions(prompt, directory):
  filenames = get_all_filenames(directory)
  detailed_prompt = (
    f"You are an exceptional and forgiving parser. Your task is to extract the actions and files involved from the user request. \n"
    f"Respond only with a valid JSON. Double-check its validity meticulously. Do not include any code blocks. Your response should be like a real API. \n"
    f"1. 'response': Provide a clean response confirming that the requested actions have been applied. \n"
    f"2. 'actions': An array of objects, each with an 'action' key containing one of ['create', 'delete', 'modify'] and the associated 'filePath'. \n"
    f"Other rules: \n"
    f"- Cap your response to 200 characters. \n"
    f"- User folder base path is {directory}. \n"
    f"- Accessible files for reference: {','.join(filenames)}. \n"
    f"User request: {prompt} \n"
)
  print("_______________")
  print("> Instructions:\n", detailed_prompt)
  print("_______________")
  return detailed_prompt

def extract_prompt_actions(prompt, directory):
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
