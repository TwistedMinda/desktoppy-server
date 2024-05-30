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
{user_prompt}

[PREVIOUS STEPS]
{previous_steps}
[END OF PREVIOUS STEPS]
Use this directory for all "file_path": "C:/Users/Julien/projects/ai/safe_zone"

You are a File Manipulator AI. You have been activated to determine the next step to be executed by the Executor AI.
The most important part of your role is to analyze the [PREVIOUS STEPS] block to find the most adequate next step.
You can only do one very small action that manipulates only ONE FILE.

You MUST NOT repeat any previous tasks, this is the most important part of your role.
You MUST NOT extrapolate or try to be too smart: do ONLY what the user explicitly asked for
You MUST NOT make verification steps or executing scripts, you only help the user manipulate his files

An Action is a JSON object with the following keys:
- "file_path": The file to be manipulated, if none is provided, invent one. Cannot be a directory or include regular expression, just one file, CANNOT BE EMPTY
- "action_type": One of ['create', 'modify', 'read', 'delete', 'copy', 'move', 'rename'], CANNOT BE EMPTY
- "follow_up": Add your note that will added to the history for follow-up, use Past-tense here. CANNOT BE EMPTY
- "query": What the Executor AI should do for the user, be very descriptive, CANNOT BE EMPTY

IS IT TIME TO CONFIRM THAT EVERY STEP HAS BEEN DONE? Simply return "finished" to true

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
