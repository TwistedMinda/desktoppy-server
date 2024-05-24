from model import *
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

def add_file_action_instructions(action, prompt, directory, file_path):
  file_content = read_file(file_path)
  detailed_prompt = (
    f"You have been entrusted with a specialized task. Your first task is to extract the specific context about the file at {file_path} from the initial user request and provided content. \n"
    f"Your second task is to update the content for the action {action} of the file at {file_path} based on this extracted context, this is your most important task, do NOT provide any response about other files. \n"
    f"Respond ONLY with the file content to be saved."
    f"Do not confirm when you're done. DO NOT say anything, no commentary, no explanations, no code-blocks, do not use ``` or any similar syntax. You only give the file content\n"
    f"If the content is code, BE SURE to not include unrequested unit testing. \n"
    f"Focus exclusively on the specified file and disregard any other files or user requests. \n"
    f"Current file content: {file_content} \n"
    f"Initial user request: {prompt}"
)
  print(f"_______________ [{file_path}]")
  print(f"> Instructions File:\n", detailed_prompt)
  print("_______________\n\n")
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

def extract_content(prompt, directory, action, file_path):
  instructions = add_file_action_instructions(action, prompt, directory, file_path)
  return get_response(instructions)

def dispatch_actions(prompt, actions, directory):
  print(actions)
  for action in actions:
    action_type = action.get('action')
    file_path = os.path.join(directory, action.get('filePath', ''))
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if action_type == 'create':
      content = extract_content(prompt, directory, action_type, file_path)
      create_file(file_path, content)
    elif action_type == 'modify':
      content = extract_content(prompt, directory, action_type, file_path)
      modify_file(file_path, content)
    elif action_type == 'delete':
      delete_file(file_path)
    else:
      print(f"Unknown action type: {action_type}")
