from flask import Flask, request, jsonify
from parsing import *
from dispatcher import *
from flask_cors import CORS
from store import Store
from request import Request
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
base_dir = os.getenv("BASE_TEST_DIR")

app = Flask(__name__)
CORS(app)

store = Store()

@app.route('/run-script', methods=['POST'])
def run_script():
  print("______RUN SCRIPT______")
  data = request.get_json()
  folder = base_dir # data.get('folder')
  prompt = data.get('prompt')
  file_paths = data.get('file_paths')
  try:
    req = Request(prompt, folder, file_paths)
    history = store.get_history()
    print("history", history)
    store.add_request(req.id, req)
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
    return True, 200
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