from model import *
from files import *
from typing import List
import json

def format_images_descriptions(image_descriptions: List[str] = []):
  descriptions = "\n".join(image_descriptions)
  return (
    f"[IMPORTED IMAGES DESCRIPTIONS]\n{descriptions}\n[END OF DESCRIPTIONS]\n"
  ) if len(descriptions) > 0 else ""

def format_history(history: str):
  return (
    f"[CONVERSATION ALREADY VISIBLE TO THE USER]\n{history}\n[END OF CONVERSATION CONTEXT]\n"
  ) if len(history) > 0 else ""

def parse_json(value: str):
  try:
    return json.loads(value.strip())
  except json.JSONDecodeError as e:
    print(f"JSON Error: {e}", value)
  return { "error": "Invalid JSON" }