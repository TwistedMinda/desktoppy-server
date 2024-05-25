import pprint
from model import *
from files import *

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