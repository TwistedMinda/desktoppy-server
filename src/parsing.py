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

def add_parser_instructions(prompt: str, directory: str, history: str = "", image_descriptions: List[str] = []):
  filenames = get_all_filenames(directory)
  detailed_prompt = (
    f"{format_images_descriptions(image_descriptions)}"
    f"{format_history(history)}"
    f"You are an exceptional and forgiving parser. Your are here to detect any action that has to be taken on files, if user is not talking about files just respond a empty array. \n"
    f"You will not over-use the 'read' action and only use it if you know what file it is referring to and it makes sense. \n"
    f"You will ignore everything related to images (don't try to 'read' images) as this is the job of another agent, but you can still use to understand context. \n"
    f"YOUR RESPONSE MUST BE FULLY VALID JSON. DO NOT RESPOND ANYTHING ELSE. Double-check its validity meticulously. Do not include any code blocks. Your response should be like a real API. \n"
    f"IMPORTANT: Simply return an empty array if no action is found, it's perfectly fine.\n"
    f"ONLY IF ACTIONS WHERE FOUND (no empty action allowed in the array), return array of objects, each with:'\n"
    f"- action: MUST BE one of ['read', 'create', 'delete', 'modify', 'copy', 'rename'] otherwise it is NOT an action \n"
    f"- filePath: The path of the file to be read, created, modified or deleted, moved or copied. \n"
    f"- query: The action that will be forwarded to another AI Agent so it must be as detailed as possible\n"
    f"Other rules: \n"
    f"- User folder base path is {directory}. \n"
    f"- Don't always try to read a file when user is asking a question, only do if you are sure the user refers to a specific file"
    f"- Accessible files for reference: {','.join(filenames)}. \n"
    f"User request: {prompt}"
)
  # print("_______Instructions________")
  # print(detailed_prompt)
  # print("_______________")
  return detailed_prompt

def parse_actions(prompt: str, directory: str, history: str = "", image_descriptions: List[str] = []):
  try:
    instructions = add_parser_instructions(prompt, directory, history, image_descriptions)
    json_response = get_response(instructions)
    return parse_json(json_response)
  except Exception as e:
    print(f"Parsing Error: {e}")
  return []

def parse_json(value: str):
  try:
    return json.loads(value.strip())
  except json.JSONDecodeError as e:
    print(f"JSON Error: {e}", value)
  return None