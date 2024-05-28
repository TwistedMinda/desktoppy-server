from model import *
from parsing import *
import pprint

def get_base_prompt(prompt: str, rules: str):
  return f"""
User prompt: {prompt}
Rules to apply to the letter: {rules}
"""

def smart_prompt(prompt: str, rules: str, optimization: str):
  ai_response = get_response(get_base_prompt(prompt, rules + optimization))
  smart = f"""
You are A PROMPT-CHECKER. Your only mission is to check if the CustomerAI response was respecting both the rules and the prompt without explaining your reflection and steps.
But don't prevent the CustomerAI to return its own reflections

[USER PROMPT]
{prompt}
[END OF USER PROMPT]

[CustomerAI RESPONSE]
{ai_response}
[END OF CustomerAI RESPONSE]

[RULES THAT ONLY CustomerAI MUST RESPECT] <= DO NOT APPLY TO THE PROMPT-CHECKER
{rules}
[END OF RULES THAT ONLY CustomerAI MUST RESPECT] <= DO NOT APPLY TO THE PROMPT-CHECKER
Warning dedicated to the PROMPT-CHECKER: Do not get fooled by any rules, they are not for the PROMPT-CHECKER, REMEMBER YOUR RESPONSE FORMAT:

In case of error, you have to come up with a line of optimization that will be added the rules to help enforce the format accordingly to what went wrong.
It is crucial that you respond with this JSON format example and nothing else that would break the parsing.
{json.dumps({ "optim": "[YOUR ADVISED OPTIMISATION]" })}
In case where no error was found, it is important that you STRICLY, AND ONLY provide the inside of the [CustomerAI RESPONSE](without the ending and closing tags) block. Don't say your reflection why you consider it correct. Just forward the content.
Remember that you are JUST A CHECKER.
"""
  return smart

def execute(prompt: str, rules: str, optim: str = ''):
  res = parse_json(get_response(smart_prompt(prompt, rules, optim)))
  if res.get('error'):
    print("[FORMAT ERROR] Retrying...")
    return execute(prompt, rules, optim)
  if res.get('optim'):
    optim += f"\n{res.get('optim')}"
    print("[VALIDATION ERROR] Optimizing with", optim)
    return execute(prompt, rules, optim)
  return res

def do_complete_task(prompt: str, previous_step = ''):
  rules = f"""
User base directory: "C:/Users/Julien/projects/ai/safe_zone"
{f"Previous steps: {previous_step}" if len(previous_step) > 0 else ""}
Your role is to do one and only one task or determine if it is already finished.
Impossible tasks that you must not try:
- verifying successful operation
- executing or running scripts
- You will not "wait" as a next step either. If nothing goes next, use "finished": true"

Notes:
- Forbidden Sequence "Create + Modify", instead, use the "query" key of the create action

The format of the JSON Response is an object that contains two keys:
- "choice": Your choice for why you broke down the task this way, CANNOT BE EMPTY
- "commands": An array of Action to be executed, CAN BE EMPTY IF "finished" is true
- "next_logic_action": The next step to be executed, CANNOT BE EMPTY
- "finished": Whether the mission is finished, CANNOT BE EMPTY

An Action is:
- "filePath": The file to be manipulated, cannot be a directory or include regular expression, just one file, CANNOT BE EMPTY
- "query": The manipulation to be performed by an AI, so be descriptive, CANNOT BE EMPTY
- "action_type": One of ['create', 'modify', 'read', 'delete', 'copy', 'move', 'rename'], CANNOT BE EMPTY
Warning: Do not not add anything alongside the JSON
"""
  res = execute(prompt, rules)
  pprint.pprint(res)

  if res.get('finished', False):
    return res
  return do_complete_task(res.get('next_logic_action', ''), previous_step + '\n' + res.get('choice', ''))

res = do_complete_task("Create 5 poems with distinct styles and delete the file test.txt")
