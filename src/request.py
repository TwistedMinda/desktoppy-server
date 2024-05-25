import uuid
from typing import List, Dict, Optional
from parsing import *
from dispatcher import *
import pprint

class Request:
  def __init__(self, prompt: str, directory: str, image_paths: List[str]):
    self.id = str(uuid.uuid4())
    self.prompt = prompt
    self.directory = directory
    self.image_paths = image_paths
    self.status = "pending"
    self.actions: Optional[List[Dict]] = []
    self.response: Optional[str] = None

  def parse(self, history: str = ""):
    self.status = "parsing"
    self.actions = parse_actions(self.prompt, self.directory, history)

  def execute(self, history: str = ""):
    self.status = "executing"
    try:
      pprint.pprint(self.actions, width=40, depth=3, indent=2, compact=False)
      if (len(self.actions) == 0):
        self.response = get_response((
          f"{format_history(history)}"
          f"New user prompt: {self.prompt}\n"
          f"Your turn to help him!"
        ))
      else:
        for action in self.actions:
          action_type = action.get('action').strip()
          file_path = os.path.join(self.directory, action.get('filePath', ''))
          query = action.get('query')
          if action_type == 'delete':
            delete_file(file_path)
            # Don't need more interactions with AI
            continue

          content = extract_content(action_type, query, file_path)
          if action_type == 'copy':
            copy_file(file_path, content)
          elif action_type == 'move' or action_type == 'rename':
            move_file(file_path, content)
          elif action_type == 'read':
            if self.response is None:
              self.response = content
            else:
              self.response += f"\n{content}"
          elif action_type == 'create':
            create_file(file_path, content)
          elif action_type == 'modify':
            modify_file(file_path, content)
          else:
            print(f"Unknown action type: {action_type}")
        if self.response is None:
          self.response = f"Actions executed ({len(self.actions)})"
      self.status = "completed"
    except Exception as e:
      print("Execution error", e)
      self.status = "failed"

    # Handle images
    # for image_path in self.image_paths:
      # stream_image_to_text(image_path)

  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "prompt": self.prompt,
      "directory": self.directory,
      "image_paths": self.image_paths,
      "status": self.status,
      "actions": self.actions,
      "response": self.response
    }