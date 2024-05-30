from model import *
from parsing import *
from dispatcher import *
import pprint

def run(action: str, query: str, file_path: str, history: str = ""):
  if action == 'delete':
    delete_file(file_path)
    # Don't need more interactions with AI
    return

  content = extract_content(action, query, file_path)
  if action == 'copy':
    copy_file(file_path, content)
  elif action == 'move' or action == 'rename':
    move_file(file_path, content)
  elif action == 'read':
    return content
  elif action == 'create':
    create_file(file_path, content)
  elif action == 'modify':
    modify_file(file_path, content)

def execute(prompt: str):
  res = parse_json(get_response(prompt))
  if res.get('error'):
    print("[FORMAT ERROR] Retrying...")
    return execute(prompt)
  return res

def do_complete_task(prompt: str, previous_steps = ''):
  user_prompt = f"""
[User prompt]
{prompt}
[End of User prompt]
"""

  rules = f"""
You are a File Manipulator AI.
You have the sole purpose to manipulate 1 file at a time.
You are the brain of this operation, we will execute the command for you.
Here are the available operations: ['create', 'modify', 'delete', 'copy', 'move', 'rename']

{user_prompt}
Use this directory for all "file_path": "C:/Users/Julien/projects/ai/safe_zone"
[PREVIOUS STEPS]
{previous_steps}
[END OF PREVIOUS STEPS]

Verify if all steps have been completed, and return a JSON object with the following key:
{json.dumps({"finished": True})}

Otherwise, deduce the most adequate next step, one that has not been previously done.
You cannot extrapolate:
- only propose an action explicitly requested in the [User Prompt].
- do not try to use files that you don't have knowledge of
Do not provide any "verification", "review" or "confirmation" steps, Finish instead.

An Action is a JSON object with the following keys:
- "file_path": The file to be manipulated, if none is provided, invent one. Cannot be a directory or include regular expression, just one file, CANNOT BE EMPTY
- "action_type": One of ['create', 'modify', 'delete', 'copy', 'move', 'rename'], CANNOT BE EMPTY
- "follow_up": Add a very precise note of your action to add to the Previous Steps (past-tense). CANNOT BE EMPTY
- "query": Descriptive description of what we need to do on the specified file. CANNOT BE EMPTY

You will precisely respond with only one JSON object, no code-block, no other content, and no introduction, just raw JSON.
"""
  res = execute(rules)
  pprint.pprint(res)
  if res.get('finished', False):
    print("> Done")
    return res
  
  history = ''
  try:
    run(res.get('action_type', ''), res.get('query', ''), res.get('file_path', ''), user_prompt + '\n' + previous_steps)
    history = previous_steps + "\n" + res.get('follow_up', '')
  except Exception as e:
    print('Error', e)
  return do_complete_task(prompt, history)

res = do_complete_task("""
Hi, i want all these tasks please to be done:
- Create 2 poems with distinct styles
- delete the file test.txt
- create a small script that transcribes a string to speech-to-text in script.py, use gtts library
- Also generate the requirements.txt that list the dependencies for the script
""")
