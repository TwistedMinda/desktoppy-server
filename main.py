import argparse
from lama import stream_image_to_text
from actions import dispatch_actions
from user_parser import add_parser_instructions, extract_prompt_actions

directory = "C:/Users/Julien/projects/ai/safe_zone/"

def run(prompt):
  # We retrieve actions and dispatch them
  (actions, user_response) = extract_prompt_actions(prompt, directory)
  dispatch_actions(prompt, actions, directory)
  print('>', user_response)

def main():
  # Parse arguments
  parser = argparse.ArgumentParser(description="Process a user request")
  parser.add_argument("prompt", type=str, help="The prompt to processed.")
  parser.add_argument("image_paths", type=str, nargs='*', help="The image paths to process.")
  args = parser.parse_args()

  # Process the prompt
  user_input = (
    f"Modify file phy2.py to change the prompt inside the tokenizer by string 'wow incredible it works'\n"
    f"Create file test/lol.py and write a python script that prints a word that makes us laugh"
  )
  # args.prompt
  run(user_input)

  # Handle images
  for image_path in args.image_paths:
    stream_image_to_text(image_path)
  
if __name__ == "__main__":
  main()