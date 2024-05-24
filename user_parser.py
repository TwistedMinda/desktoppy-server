from model import *
from files_manip import *
import json
import pprint

def add_parser_instructions(prompt, directory):
  filenames = get_all_filenames(directory)
  detailed_prompt = (
    f"You are an exceptional and forgiving parser. Your task is to extract the actions, files involved, and a summary of the action from the user request. \n"
    f"Respond only with a valid JSON. Double-check its validity meticulously. Do not include any code blocks. Your response should be like a real API. \n"
    f"1. 'response': Provide a clean response confirming that the requested actions have been applied. \n"
    f"2. 'actions': An array of objects, each with:'\n"
    f"- filePath: The path of the file to be read, created, modified or deleted. \n"
    f"- query: The details of the action that should be done on the file, or in case of reading, what information to extract, conserve all important information! \n"
    f"Other rules: \n"
    f"- User folder base path is {directory}. \n"
    f"- Accessible files for reference: {','.join(filenames)}. \n"
    f"User request: {prompt}"
)
  # print("_______Instructions________")
  # print(detailed_prompt)
  # print("_______________")
  return detailed_prompt

def add_file_action_instructions(query, file_path):
  file_content = read_file(file_path)
  detailed_prompt = (
    f"You have been entrusted with a specialized task. Extract the specific context about the file at {file_path} from the initial user request and provided content. \n"
    f"Your primary task is to generate a JSON array of commands to achieve the user's request. Each command should be executable and directly related to the specified file. \n"
    f"Respond ONLY with the JSON array of commands that are ONLY python code (with their imports and return line if needed). Do not include any commentary, explanations, or code blocks. \n"
    f"Example format that must be respected: [\"print('hello')\", ...] be extremely careful with quotes and escaping\n"
    f"Initial user request: {query}\n"
    f"Current file content: {file_content}"
)
  # print(f"_______[Instructions {file_path}]________")
  # print(detailed_prompt)
  # print("_______________")
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

def extract_content(query, file_path):
  instructions = add_file_action_instructions(query, file_path)
  return get_response(instructions)

def dispatch_actions(prompt, actions, directory):
  pprint.pprint(actions, width=40, depth=3, indent=2, compact=False)
  for action in actions:
    file_path = os.path.join(directory, action.get('filePath', ''))
    query = action.get('query')
    commands = extract_content(query, file_path)
    print("Commands: ", commands)
    command_list = json.loads(commands)
    for command in command_list:
      print(command)
      exec(command)
    print("done")
