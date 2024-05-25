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
    f"- query: The details of the action that should be done on the file, or in case of reading what information to extract, conserve all important information! \n"
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

def add_file_action_instructions(action, query, file_path):
  file_content = read_file(file_path)

  if action == 'create':
    return (
      f"Your first task is to create a new file at {file_path} to fulfill user request. \n"
      f"Respond ONLY with the file content to be saved. \n"
      f"Do not confirm when you're done. DO NOT say anything, no commentary, no explanations, no code-blocks, do not use ``` or any similar syntax. You only give the file content\n"
    )
  elif action == 'read':
    return (
      f"Your first task is to read the file at {file_path} and extract the specific context. \n"
      f"Current file content: {file_content} \n"
      f"User request: {query}"
    )
  elif action == 'modify':
    return (
      f"Your first task is to modify the file at {file_path} to fulfill user request. \n"
      f"Do not confirm when you're done. DO NOT say anything, no commentary, no explanations, no code-blocks, do not use ``` or any similar syntax. You only give the file content\n"
      f"Current file content: {file_content} \n"
      f"User request: {query}"
    )
  elif action == 'move' or action == 'rename':
    return (
      f"Your first task is to move the file at {file_path} to fulfill user request. \n"
      f"You must ONLY respond with the destination file AS SIMPLE STRING. \n"
      f"User request: {query}"
    )
  elif action == 'copy':
    return (
      f"Your first task is to copy the file at {file_path} to fulfill user request. \n"
      f"You must ONLY respond with the destination file AS SIMPLE STRING. \n"
      f"User request: {query}"
    )
  return (
    f"Give your best help to the user. \n"
    f"Current file content: {file_content} \n"
    f"User request: {query}"
  )

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

def extract_content(query, action, file_path):
  instructions = add_file_action_instructions(action, query, file_path)
  return get_response(instructions)

def dispatch_actions(prompt, actions, directory):
  pprint.pprint(actions, width=40, depth=3, indent=2, compact=False)
  if (len(actions) == 0):
    stream_response(prompt)
    return
  for action in actions:
    action_type = action.get('action').strip()
    file_path = os.path.join(directory, action.get('filePath', ''))
    query = action.get('query')
    # Simple actions
    if action_type == 'delete':
      delete_file(file_path)
      return
    elif action_type == 'copy':
      content = extract_content(query, action_type, file_path)
      copy_file(file_path, content)
      return
    elif action_type == 'move' or action_type == 'rename':
      content = extract_content(query, action_type, file_path)
      move_file(file_path, content)
      return
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    content = extract_content(query, action_type, file_path)
    if action_type == 'read':
      print(">", content)
    elif action_type == 'create':
      create_file(file_path, content)
    elif action_type == 'modify':
      modify_file(file_path, content)
    else:
      print(f"Unknown action type: {action_type}")
