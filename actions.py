import os
from files_manip import *
from lama import *

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
