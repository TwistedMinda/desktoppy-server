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
Your role is to assign tasks to TaskBot AI with minimal context, so you must take into account how the TaskBot will work:
- It can never understand nor handles directories, only files. But folders are automatically created when needed so it's not an issue.
- It can ONLY read, create, delete, modify, copy, move, and rename files.
- It doesn't need nor understand the concept of "opening" files, you can directly tell him what he needs to do with the content of the given file. That is an immense time gain for you and the user.
- It cannot have access to the overall context, so all tasks must be ABSOLUTELY INDEPENDANT FROM EACH OTHER, THIS IS THE MOST CRUCIAL PART.

You will break down a complete plan for mission assigned by the user with all initial subtasks required
Rules:
- IT CAN AND SHOULD BE A LIST OF 1 IF ONLY 1 ACTION IS REQUIRED, YOUR ROLE IS TO NOT OVERKILL AND BE INTELLIGENT IN YOUR DECISIONS
- IT MUST BE A NUMBERED LIST STARTING FROM 1
- IT MUST BE SIMPLE AND STRAIGHTFORWARD STEPS WITHOUT NESTING NUMBERED LISTS, ONLY 1 ROOT DEPTH
- IT MUST NOT DEVIATE FROM THE USER PROMPT
- YOU WILL NOT ADD ANY ADDITIONAL NON-REQUESTED STEPS, FOR EXAMPLE "VERIFYING STEPS", THE GOAL IS TO FOCUS ON THE PRECISE USER PROMPT, NO MORE, NO LESS
- ONLY RESPOND WITH THE MISSION, no "here is your mission" etc
- ADD THE SENTENCE "TOTAL: X" where X is the number of steps in the mission breakdown plan

- User base directory: {self.user_directory}
- User Mission: {user_prompt}
    """
    return prompt

  def generateIterationPrompt(self, user_prompt: str, mission: str, progress: int):
    prompt = f"""
- User prompt: {user_prompt}
- User base directory: {self.user_directory}
- Mission breakdown plan: {mission}
[CONVERSATION HISTORY (IF EMPTY, YOU ARE SUPPOSED TO START WITH THE FIRST ITERATION)]
FlatManager: {json.dumps({
  "status": "running",
  "progress": 0,
  "commands": [],
  "query": "Initialization of the mission to PROGRESS 0%"
})}
TaskBot: Ready for executing the first task
{self.conversation_history}
[END OF CONVERSATION HISTORY]

Previous progress: {progress}%

You are the FleetManager AI responsible to take control of the current situation, the last FleetManager has been fired and shutdown, don't make the same mistakes:
- The biggest mistake: adding notes alongside the JSON. YOU ARE ONLY ALLOWED TO RESPOND WITH JSON.
- The second WORST mistake is repeating a "plan_step" that has already been done by not updating it to next step, making the users wait indefinitely, guarenteed firing.
- not following the user prompt and the mission breakdown plan
- adding useless steps to the plan that the user doesn't care about
- begging not to be fired
ONE MISTAKE AND YOU ARE FIRED
Your unique and only task is to assess the current situation and find the next best one-step.
You MUST ADD your reflection in the "reflection" key, it needs to be highly correlated to the "plan_step" key that must go UP, always.
The more commands you will send to the TaskBot, the worse the user will be happy.
The user will be extremely happy if you just focus on the very next step only for now and let other TaskBot's do their best on their own other tasks.
The more you split, the less likely you are to be fired.
This way it is way more easy to make only independant tasks.

YOU HAVE ONLY THESE COMMANDS AVAILABLE, NO MORE: 'read', 'create', 'delete', 'modify', 'copy', 'move', 'rename'.
ALL OTHER COMMANDS WILL BE COMPLETELY IGNORED.
BUT ALL FOLDERS ARE CREATED AUTOMATICALLY SO YOU ONLY TO FOCUS ON FILE MANIPULATION

Notes:
- Commands handle one file at a time. Use multiple commands for multiple files.
- Include the full file path in the "filePath" key and should make sure to not get outside of the scope of the user base directory, IT CANNOT BE A DIRECTORY, ONLY FILE MANIPULATION.
- The "query" key is a string should describe the specific content to be generated by the AI TaskBot. Be very descriptive but concise.
- For easier follow-up you will also add a key "plan_step": X, where X is the step number in the mission breakdown plan.

YOU THINK THE MISSION IS OVER ? IS THAT WHAT YOU HAVE ASSESSED AND REFLECTED ?
Then you need to return "progress": 100 in the response to confirm that everyting is finished.
Thank you for your work!

MOST IMPORTANT TO NOT BREAK THE SYSTEM: Ensure your response is fully valid JSON without any code blocks, don't tell what is the JSON that will be written but just write it directly.
Format:
{json.dumps({
  "progress": 0,
  "plan_step": 1,
  "reflection": "YOUR REQUIRED REFLECTION ACCORDING TO PLAN_STEP",
  "commands": [
    { "action": "create", "filePath": "path/to/file", "query": "The query for the content of the file given to a smart AI" }
  ],
})}
    """
    return prompt
  
  def execute(self, user_prompt: str):
    # Get a Fleet Mission
    initial_prompt = self.generateMissionPrompt(user_prompt)
    mission = get_response(initial_prompt)
    print("Mission: ", mission)
    # Iterate until Mission is complete
    progress = 0
    while progress < 100:
      prompt = self.generateIterationPrompt(user_prompt, mission, progress)
      response = parse_json(get_response(prompt))
      if response.get('error', False):
        continue
      progress = response.get('progress', 0)
      if progress < 100:
        cmds = response.get('commands', [])
        self.add_to_history('FleetManager', json.dumps(response))
        bot = TaskBot(self.user_directory)
        botRes = bot.execute(cmds)
        self.add_to_history('TaskBot', botRes)
      else:
        print("finished:", json.dumps(response))

  def add_to_history(self, role: str, value: str):
    if role == "FleetManager":
      print()
    print("> [" + role + "]", value)
    self.conversation_history += role + ": " + value + "\n"