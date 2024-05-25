import pprint
from model import *
from files_manip import *

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

def extract_content(query, action, file_path):
  instructions = add_file_action_instructions(action, query, file_path)
  return get_response(instructions)

def execute_actions(prompt, actions, directory):
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
      continue
    elif action_type == 'copy':
      content = extract_content(query, action_type, file_path)
      copy_file(file_path, content)
      continue
    elif action_type == 'move' or action_type == 'rename':
      content = extract_content(query, action_type, file_path)
      move_file(file_path, content)
      continue
    
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
