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
  rules = f"""
<Directory>C:/Users/Julien/projects/ai/safe_zone</Directory>
<Prompt>{prompt}</Prompt>
<PreviousSteps>
{previous_steps}
</PreviousSteps>
"""
  res = execute(rules)
  if res.get('finished', False):
    print("> Done")
    return res
  pprint.pprint('>' + res.get('follow_up', ''))
  
  history = ''
  try:
    run(res.get('action_type', ''), res.get('query', ''), res.get('file_path', ''))
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
