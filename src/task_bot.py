import json
from model import *
from parsing import *
from dispatcher import *

class TaskBot:

  conversation_history = ""
  user_directory = ""

  def __init__(self, directory: str):
    self.user_directory = directory

  def generatePrompt(self, user_prompt: str, manager_query: str):
    prompt = f"""
You are TaskBot AI, designed to execute specific commands with minimal context. 
You will receive a detailed query from the Fleet Master AI along with the 
necessary context provided by the Python server. Your role is to perform the 
task and provide feedback.
You are also intelligent, you must refuse any task that deviate from the initial user query, and ask for the end of the mission.
But small limitation, for writing into files, you have to make the request in a single line that you add into the "query" key in the response, and it will be forwarded to an as-intelligent-as-you AI to generate the content inside, but you are to make a very smart description so it can do its work.
Another constraint is that you must be very descriptive because you can't add complicated combo codes in the query because it will break the JSON, so be descriptive and trust the next AI

User base directory: {self.user_directory}

[COMMAND RECEIVED FROM FLEET MASTER]
{manager_query}
[END OF COMMAND RECEIVED FROM FLEET MASTER]

VERY IMPORTANT: You can only respond with this JSON format, do not say anything else than JSON, like an HTTP API, only respond with the JSON
{json.dumps({
  "done": True,
  "commands": [
    { "action": "create", "filePath": "path/to/file", "query": "The query for the content of the file given to a smart AI" }
  ],
  "response_to_fleet_master": "response to the fleet master on the executed action"
})}

Possible commands are: 'read', 'create', 'delete', 'modify', 'copy', 'move', 'rename'.

Your goal is to execute the given command accurately, provide necessary feedback 
for the next steps, and indicate if more context is required.
    """

    return prompt
  
  def execute(self, user_prompt: str, manager_query: str):
    prompt = self.generatePrompt(user_prompt, manager_query)
    response = parse_json(get_response(prompt))
    for value in response.get('commands'):
      print("TaskBot executes: ", value)
      action = value.get('action')
      file_path = value.get('filePath')
      query = value.get('query')
      if action == 'delete':
        delete_file(file_path)
        # Don't need more interactions with AI
        continue

      content = extract_content(action, query, file_path)
      if action == 'copy':
        copy_file(file_path, content)
      elif action == 'move' or action == 'rename':
        move_file(file_path, content)
      elif action == 'read':
        if self.response is None:
          self.response = content
        else:
          self.response += f"\n{content}"
      elif action == 'create':
        create_file(file_path, content)
      elif action == 'modify':
        modify_file(file_path, content)
      else:
        print(f"Unknown action type: {action}")

    return response.get('response_to_fleet_master')
    if response.get('done'):
      return response.get('response_to_fleet_master')
    max = 2
    for i in range(max):
      prompt = self.generatePrompt(response.get('required_'))
      response = parse_json(get_response(prompt))
      print("TaskBot", response)
      if response.get('done'):
        return response.get('response_to_fleet_master')
    return "I'm sorry, I couldn't complete the task in the given time frame."