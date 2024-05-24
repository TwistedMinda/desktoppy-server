import argparse
from model import *
from user_parser import *

def run(prompt, directory):
  # We retrieve actions and dispatch them
  (actions, user_response) = extract_prompt_actions(prompt, directory)
  dispatch_actions(prompt, actions, directory)
  print('>', user_response)

def entry(directory, prompt, image_paths):
  # Process the prompt
  user_input = (
    f"Modify file phy2.py to change the prompt inside the tokenizer by string 'wow incredible it works'\n"
    f"Create file test/lol.py and write a python script that prints a word that makes us laugh\n"
    f"Read and summarize the yolo file for me"
  )
  # args.prompt
  run(prompt, directory)

  # Handle images
  for image_path in image_paths:
    stream_image_to_text(image_path)
  