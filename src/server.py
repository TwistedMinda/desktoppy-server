from flask import Flask, request, jsonify
from user_parser import *
from requests_queue import *
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
base_dir = os.getenv("BASE_TEST_DIR")

app = Flask(__name__)
CORS(app)

def run(directory, prompt, image_paths):
  # Process the prompt
  (actions, user_response) = parse_actions(prompt, directory)
  execute_actions(prompt, actions, directory)
  print('>', user_response)

  # Handle images
  for image_path in image_paths:
    stream_image_to_text(image_path)

@app.route('/run-script', methods=['POST'])
def run_script():
  data = request.get_json()
  folder = base_dir # data.get('folder')
  user_input = (
    f"Modify file phy2.py to change the prompt inside the tokenizer by string 'wow incredible it works'\n"
    f"Create file test/lol.py and write a python script that prints a word that makes us laugh\n"
    f"Read and summarize the yolo file for me"
  )
  prompt = data.get('prompt')
  filePaths = data.get('filePaths')
  try:
    run(folder, prompt, filePaths)
    return jsonify(str("ok")), 200
  except Exception as e:
    print(e)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
  app.run(debug=True)