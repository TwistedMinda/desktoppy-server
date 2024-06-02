import uuid
from typing import List, Dict, Optional
from parsing import *
from image_model import *

def get_json_response(prompt: str):
  res = parse_json(get_response(prompt, 'desktoppy_model'))
  if res.get('error'):
    return get_json_response(prompt)
  return res

class Request:
  def __init__(self, prompt: str, image_names: List[str] = []):
    self.id = str(uuid.uuid4())
    self.prompt = prompt
    self.image_names = image_names
    self.images_descriptions: Optional[List[str]] = []
    self.generated_images: Optional[List[str]] = []
    self.status = "pending"
    
    self.response: Optional[str] = None

  def load_images_descriptions(self, image_paths: List[str]):
    if len(image_paths) == 0:
      return
    self.status = "analyzing images"
    self.images_descriptions = [image_to_text(image_path) for image_path in image_paths]

  def execute(self, history: str = ""):
    self.status = "executing"
    try:
      res = get_json_response((
        f"{format_images_descriptions(self.images_descriptions)}"
        f"{format_history(history)}"
        f"New user prompt: {self.prompt}\n"
        f"Your turn to help him!"
      ))
      self.response = res.get('response')
      prompts = res.get('generate_prompts', [])
      if len(prompts) > 0:
        self.status = "generating images"
      for item in prompts:
        img_prompt = item.get('prompt', '')
        img_slug = item.get('slug', '')
        create_image(img_prompt, './images/' + img_slug)
        self.generated_images.append(img_slug)
      self.status = "completed"
    except Exception as e:
      print("Execution error:", e)
      self.status = "failed"

  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "prompt": self.prompt,
      "image_names": self.image_names,
      "image_descriptions": self.images_descriptions,
      "status": self.status,
      "response": self.response,
      "generated_images": self.generated_images
    }