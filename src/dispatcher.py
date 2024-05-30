from model import *
from files import *
from parsing import *

def add_file_action_instructions(action: str, query: str, file_path: str, history: str = "", image_descriptions: List[str] = []):
  old_conversation = format_history(history)
  img_desc = format_images_descriptions(image_descriptions)
  if action == 'create':
    return (
      f"{img_desc}"
      f"{old_conversation}"
      f"You were ordered to create a new file at {file_path} to fulfill user request. \n"
      f"Respond ONLY with the file content to be saved. \n"
      f"Do not confirm when you're done. DO NOT say anything, no commentary, no explanations, no code-blocks, do not use ``` or any similar syntax. You only give the file content\n"
      f"User request: {query}"
    )
  elif action == 'read':
    file_content = read_file(file_path)
    return (
      f"{img_desc}"
      f"{old_conversation}"
      f"You were ordered to read the file at {file_path} and respond the to the query using the context content. \n"
      f"DO NOT RESPOND WITH THE FILE CONTENT. \n"
      f"Current file content: {file_content} \n"
      f"User request: {query}"
    )
  elif action == 'modify':
   file_content = read_file(file_path)
   return (
      f"{img_desc}"
      f"{old_conversation}"
      f"You were ordered to modify the file at {file_path} to fulfill user request. \n"
      f"Do not confirm when you're done. DO NOT say anything, no commentary, no explanations, no code-blocks, do not use ``` or any similar syntax. You only give the file content\n"
      f"Current file content: {file_content} \n"
      f"User request: {query}"
      f"Modification is crucial, user wants you to reflect on what the file needs to changed to, if possible, reuse as much as possible from the initial content."
    )
  elif action == 'move' or action == 'rename':
    return (
      f"{img_desc}"
      f"{old_conversation}"
      f"You were ordered to move the file at {file_path} to fulfill user request. \n"
      f"You must ONLY respond with the destination file AS SIMPLE STRING. \n"
      f"User request: {query}"
    )
  elif action == 'copy':
    return (
      f"{img_desc}"
      f"{old_conversation}"
      f"You were ordered to copy the file at {file_path} to fulfill user request. \n"
      f"You must ONLY respond with the destination file AS SIMPLE STRING. \n"
      f"User request: {query}"
    )
  file_content = read_file(file_path)
  return (
    f"{img_desc}"
    f"{old_conversation}"
    f"Give your best help to the user. \n"
    f"Current file content: {file_content} \n"
    f"User request: {query}"
  )

def extract_content(action: str, query: str, file_path: str, history: str = "", image_descriptions: List[str] = []):
  instructions = add_file_action_instructions(action, query, file_path, history, image_descriptions)
  print("> Manipulating files")
  response = get_response(instructions)
  print("> Done manipulating files")
  return response
