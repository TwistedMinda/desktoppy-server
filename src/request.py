import uuid
from typing import List, Dict, Optional
from parsing import *
from dispatcher import *
import pprint

class Request:
  def __init__(self, prompt: str, directory: str, image_names: List[str]):
    self.id = str(uuid.uuid4())
    self.prompt = prompt
    self.directory = directory
    self.image_names = image_names
    self.images_descriptions: Optional[List[str]] = []
    self.status = "pending"
    
    self.response: Optional[str] = None

  def parse(self, history: str = ""):
    self.status = "parsing"

  def load_images_descriptions(self, image_paths: List[str]):
    if len(image_paths) == 0:
      return
    self.status = "analyzing images"
    self.images_descriptions = [image_to_text(image_path) for image_path in image_paths]

  def execute(self, history: str = ""):
    self.status = "executing"
    try:
      self.response = get_response((
        f"{format_images_descriptions(self.images_descriptions)}"
        f"{format_history(history)}"
        f"New user prompt: {self.prompt}\n"
        f"Your turn to help him!"
      ))
      self.status = "completed"
    except Exception as e:
      print("Execution error:", e)
      self.status = "failed"

  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "prompt": self.prompt,
      "directory": self.directory,
      "image_names": self.image_names,
      "image_descriptions": self.images_descriptions,
      "status": self.status,
      "response": self.response
    }