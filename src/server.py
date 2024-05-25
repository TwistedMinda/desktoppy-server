from flask import Flask, request, jsonify
from parsing import *
from dispatcher import *
from flask_cors import CORS
from store import Store
from request import Request
from dotenv import load_dotenv
import os
import tempfile

# Load .env
load_dotenv()
base_dir = os.getenv("BASE_TEST_DIR")

app = Flask(__name__)
CORS(app)

store = Store()

@app.route('/run-script', methods=['POST'])
def run_script():
  print("______RUN SCRIPT______")
  folder = base_dir # request.form.get('folder')
  prompt = request.form.get('prompt')
  file_paths = []
  file_names = []
  with tempfile.TemporaryDirectory() as temp_dir:
    for key, file_storage in request.files.items():
      # Save the file to the temporary directory
      file_path = os.path.join(temp_dir, file_storage.filename)
      file_storage.save(file_path)
      # Append the absolute path to the list
      file_paths.append(os.path.abspath(file_path))
      file_names.append(file_storage.filename)
    print("paths", file_paths)

    try:
      req = Request(prompt, folder, file_names)
      store.add_request(req.id, req)
      req.load_images_descriptions(file_paths)
      history = store.get_history()
      req.parse(history)
      req.execute(history)
      return jsonify(request_id=req.id), 200
    except Exception as e:
      print('Global Error', e)
      return jsonify(error=str(e)), 500

@app.route('/responses', methods=['GET'])
def get_responses():
  try:
    return [store.requests[value].to_dict() for value in store.requests], 200
  except Exception as e:
    print('Error', e)
    return jsonify(error=str(e)), 500

@app.route('/clear-conversation', methods=['POST'])
def clear_conversation():
  try:
    store.clear()
    return jsonify(True), 200
  except Exception as e:
    print('Error', e)
    return jsonify(error=str(e)), 500


@app.route('/get-status', methods=['GET'])
def get_status():
  print("______GET STATUS______")
  request_id = request.args.get('request_id')
  try:
    request = store.get_request(request_id)
    return request.to_dict(), 200
  except Exception as e:
    print('Error', e)
    return jsonify(error=str(e)), 500


if __name__ == '__main__':
  app.run(debug=True)