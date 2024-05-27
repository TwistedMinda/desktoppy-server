import json
from model import *
from parsing import *
from task_bot import TaskBot
from files import *

class FleetManager:

  user_directory = ""
  conversation_history = ""

  def __init__(self, directory: str):
    self.user_directory = directory

  def generateMissionPrompt(self, user_prompt: str):
    prompt = f"""
You are the FleetManager AI responsible for overseeing complex tasks.
Your role is to assign tasks to TaskBot AI with minimal context.
You will break down a complete plan for mission assigned by the user with all initial subtasks required
Rules:
- IT MUST BE VERY SIMPLE
- IT MUST NOT DEVIATE FROM THE USER PROMPT
- IT MUST BE A LIST OF COMMA SEPERATED TASKS WITHOUT MUCH DETAILS, IT WILL BE DONE IN ITERATIONS
- ONLY RESPOND WITH THE MISSION

- User base directory: {self.user_directory}
- User Mission: {user_prompt}
    """
    return prompt

  def generateIterationPrompt(self, user_prompt: str, mission: str):
    filenames = get_all_filenames(self.user_directory)
    prompt = f"""
- User base directory: {self.user_directory}
- Accessible files for reference: {','.join(filenames)}. \n"
[CONVERSATION HISTORY]
{self.conversation_history}
[END OF CONVERSATION HISTORY]

You are the FleetManager AI responsible for overseeing this complex task: {user_prompt}
You are asked to find the most intelligent step next that will really be helpful for the task.
MAKE SURE IT'S ONE-BY-ONE, ONLY GIVE SINGLE-STEP TASKS, TaskBot CANNOT modify multiple files at once.
You are the master mind of this situation and absolutely have to END (with "status": "finished" and empty "query" in the response) when the task is obviously finished
Another constraint is that you must be very descriptive because you can't add complicated combo codes in the "query" because it will break the JSON, so be descriptive and trust the next AI
Don't ask the TASKbot to give you information like listing, but instead to make actions only.

VERY IMPORTANT: You can only respond with this JSON format, do not say anything else than JSON, like an HTTP API, only respond with the JSON
{json.dumps({
  "status": "running (OR) finished",
  "context_required": ['file path the task should need as context so he executes the task correctly, can give mutliple'],
  "query": "Specific and detailed question or task for TaskBot"
})}
    """
    return prompt
  
  def execute(self, user_prompt: str):
    # Get a Fleet Mission
    #initial_prompt = self.generateMissionPrompt(user_prompt)
    # mission = get_response(initial_prompt)
    mission = ""
    # Iterate until Mission is complete
    status = "running"
    while status == "running":
      prompt = self.generateIterationPrompt(user_prompt, mission)
      response = parse_json(get_response(prompt))
      # print("Fleet Manager", response)
      status = response.get('status', 'running')
      if status == "running":
        self.add_to_history('FleetManager', response.get('query', ''))
        bot = TaskBot(self.user_directory)
        self.add_to_history('TaskBot', bot.execute(user_prompt, response.get('query', '')))
    print("finished")

  def add_to_history(self, role: str, value: str):
    print("> [" + role + "]", value)
    self.conversation_history += role + ": " + value + "\n"