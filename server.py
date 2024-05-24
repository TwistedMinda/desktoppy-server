from flask import Flask, request, jsonify
from entry import *  # Import your function from main.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run-script', methods=['GET'])
def run_script():
  folder = request.args.get('folder', default='', type=str)
  prompt = request.args.get('prompt', default='', type=str)
  filePaths = request.args.get('filePaths', default='', type=str)
  
  try:
    entry(folder, prompt, filePaths)
    return jsonify(str("ok")), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
  app.run(debug=True)