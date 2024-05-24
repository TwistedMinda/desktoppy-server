import os
from files_manip import create_file, delete_file, modify_file

def dispatch_actions(actions, base_path):
  print(actions)
  for action in actions:
    action_type = action.get('action')
    file_path = os.path.join(base_path, action.get('filePath', ''))
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if action_type == 'create':
      create_file(file_path, action.get('content', ''))
    elif action_type == 'delete':
      delete_file(file_path)
    elif action_type == 'modify':
      modify_file(file_path, action.get('content', ''))
    else:
      print(f"Unknown action type: {action_type}")
