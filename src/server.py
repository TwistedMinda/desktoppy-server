from flask import Flask, request, jsonify, send_file
from parsing import *
from flask_cors import CORS
from store import Store
from request import Request
import os
import tempfile
# from dotenv import load_dotenv
# load_dotenv()
# env_var = os.getenv("ENV_VAR")

app = Flask(__name__)
CORS(app)

store = Store()

@app.route('/run-script', methods=['POST'])
def run_script():
  print("______RUN SCRIPT______")
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

    try:
      req = Request(prompt, file_names)
      store.add_request(req.id, req)
      req.load_images_descriptions(file_paths)
      history = store.get_history()
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

@app.route('/images', methods=['GET'])
def serve_static_image():
  try:
    filename = request.args.get('name', default = '', type = str)
    # Create the directory if it doesn't exist
    path = '../images/' + filename
    return send_file(path, mimetype='image/gif')
  except Exception as e:
    print('Error', e)
    return send_file('../images/404.png', mimetype='image/gif')

@app.route('/clear-conversation', methods=['POST'])
def clear_conversation():
  try:
    store.clear()
    return jsonify(True), 200
  except Exception as e:
    print('Error', e)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
  app.run(debug=True)