from flask import Flask, request, jsonify
from entry import *
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
base_dir = os.getenv("BASE_TEST_DIR")

app = Flask(__name__)
CORS(app)

@app.route('/run-script', methods=['POST'])
def run_script():
  data = request.get_json()
  folder = base_dir # data.get('folder')
  prompt = data.get('prompt')
  filePaths = data.get('filePaths')
  try:
    entry(folder, prompt, filePaths)
    return jsonify(str("ok")), 200
  except Exception as e:
    print(e)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
  app.run(debug=True)