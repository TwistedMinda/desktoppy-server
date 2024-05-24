import argparse
import json
from lama import get_response, stream_image_to_text
from actions import dispatch_actions

directory = "C:/Users/Julien/projects/ai/safe_zone/"

def add_instructions(prompt):
  detailed_prompt = (
    f"You are a parser, extract the actions and files involved."
    f" Only respond with a valid JSON (double-check that), no code block, just like a real API:"
    f" 1. 'response' a clean response for the user, and confirmation that his requested actions have been applied"
    f" 2. 'actions' array of objects with key 'action' being one of ['create', 'delete', 'modify'] and the associated 'filePath' and of course the new 'content'"
    f" Cap your response to 200 characters"
    f" User folder base path file is {directory}"
    f" User request: {prompt}"
  )
  return detailed_prompt


def main():
  # Parse arguments
  parser = argparse.ArgumentParser(description="Process a user request")
  parser.add_argument("prompt", type=str, help="The prompt to processed.")
  parser.add_argument("image_paths", type=str, nargs='*', help="The image paths to process.")
  args = parser.parse_args()

  # Process the prompt
  user_input = """
    Modify file phy2.py to change the prompt inside the tokenizer for 'fuck me it works'
    Create file test/lol.py and write a python script that says "lol"
  """ # args.prompt
  clean_prompt = add_instructions(user_input)
  json_response = get_response(clean_prompt)
  
  # Parse the JSON response
  try:
      response_data = json.loads(json_response)
      user_response = response_data.get('response', '')
      actions = response_data.get('actions', [])
      dispatch_actions(actions, directory)
      print(user_response)
  except json.JSONDecodeError as e:
      print(f"Error parsing JSON response: {e}", json_response)
  
  # Handle images
  for image_path in args.image_paths:
    stream_image_to_text(image_path)

if __name__ == "__main__":
  main()