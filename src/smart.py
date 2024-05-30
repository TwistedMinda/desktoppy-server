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
  # Introduction
  intro = (
f"""
[STEPS ALREADY APPLIED]:
{previous_steps}
[END OF PREVIOUS STEPS]
Please help me find the best next small step to help our beloved user correctly after we've done all these tasks already.
Let's focus on one.
"""
  ) if len(previous_steps) > 0 else (
"""
Please help me find the first small step to help our beloved user correctly.
Let's focus on one.
"""
  )

  # Disclaimer
  disclaimer = """
Since there is no validation part, you must just trust the process and assess if all steps of user request have already been addressed and choose to end.
Otherwise, user will be stuck waiting forever
""" if len(previous_steps) > 0 else ""
  
  # Final prompt
  rules = f"""
[User prompt]
{prompt}
[End of User prompt]
Use this directory for all "file_path": "C:/Users/Julien/projects/ai/safe_zone"

{intro}

We need to reduce the workload to the smallest task possible that is now required.

An Action is a JSON object with the following keys:
- "file_path": The file to be manipulated, cannot be a directory or include regular expression, just one file, CANNOT BE EMPTY
- "action_type": One of ['create', 'modify', 'read', 'delete', 'copy', 'move', 'rename'], CANNOT BE EMPTY
- "follow_up": Add your note that will added to the history for follow-up, use Past-tense here. CANNOT BE EMPTY
- "query": What the Executor AI should do for the user, be very descriptive, CANNOT BE EMPTY

If no action is needed to complete the user mission, simply return "finished" to true
{disclaimer}

Constraints:

General:
- do not add quality check/verification steps
- do not add any non-requested steps
- do not add steps to execute or run scripts
- do not use "Create + Modify" pattern, instead, use the "query" key of the create action

You will precisely respond with only one JSON object, no code-block, no other content, and no introduction, just raw JSON.
"""
  res = execute(rules)
  pprint.pprint(res)
  if res.get('finished', False):
    print("> Done")
    return res
  
  history = ''
  try:
    run(res.get('action_type', ''), res.get('query', ''), res.get('file_path', ''), previous_steps)
    history = previous_steps + "\n" + res.get('follow_up', '')
  except Exception as e:
    print('Error', e)
  return do_complete_task(prompt, history)

res = do_complete_task("""
Hi, i want all these tasks please to be done:
- Create 5 poems with distinct styles
- delete the file test.txt
- create a small script that transcribes a string to speech-to-text in script.py, use gtts library
Also need the requirements.txt that list the dependencies for the script
""")
