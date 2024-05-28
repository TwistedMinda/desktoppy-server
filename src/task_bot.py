import json
from model import *
from parsing import *
from dispatcher import *
from files import *
from typing import List, Dict

class TaskBot:

  conversation_history = ""
  user_directory = ""

  def __init__(self, directory: str):
    self.user_directory = directory

  def execute(self, actions: List[Dict]):
    for value in actions:
      action = value.get('action')
      file_path = value.get('filePath')
      query = value.get('query')
      if action == 'delete':
        delete_file(file_path)
        # Don't need more interactions with AI
        continue

      content = extract_content(action, query, file_path)
      if action == 'copy':
        copy_file(file_path, content)
      elif action == 'move' or action == 'rename':
        move_file(file_path, content)
      elif action == 'read':
        return content
      elif action == 'create':
        create_file(file_path, content)
      elif action == 'modify':
        modify_file(file_path, content)
      else:
        print(f"Unknown action type: {action}, You are about to get Fired. Are you repeating tasks? You have to re-assess where you are in the plan")

    return f"I have completed the task."