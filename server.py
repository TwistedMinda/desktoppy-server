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

@app.route('/run-script', methods=['GET'])
def run_script():
  folder = base_dir #request.args.get('folder', default='', type=str)
  prompt = request.args.get('prompt', default='', type=str)
  filePaths = request.args.get('filePaths', default='', type=str)
  
  try:
    entry(folder, prompt, filePaths)
    return jsonify(str("ok")), 200
  except Exception as e:
    print(e)
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
  app.run(debug=True)