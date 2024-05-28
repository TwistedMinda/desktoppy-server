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
- It is his role to find the correct file contents, you need to find the prompt that will be used by the AI TaskBot to force him to execute the task himself, it is not your job to decide the content of files, you are a prompt manager
- It can never understand nor handles directories, only files. But folders are automatically created when needed so it's not an issue.
- It can ONLY read, create, delete, modify, copy, move, and rename files.
- It doesn't need nor understand the concept of "opening" files, you can directly tell him what he needs to do with the content of the given file. That is an immense time gain for you and the user.
- It cannot have access to the overall context, so all tasks must be ABSOLUTELY INDEPENDANT FROM EACH OTHER, THIS IS THE MOST CRUCIAL PART.
- It cannot execute scripts, you will instead help the user create the scripts he is asking and he will run them by himself

You will break down a complete plan for mission assigned by the user with all initial subtasks required
Rules:
- DO NOT SPREAD A FILE MANIPULATION TO MULTIPLE TASKS, AS THEY SHOULD BE INDEPENDANT OF THE OVERALL CONTEXT
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

  def generateIterationPrompt(self, user_prompt: str, mission: str, progress: int, step: int):
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
Last "plan_step" {step}, should now go foward:

You are the FleetManager AI, responsible for managing the current situation. The previous FleetManager was terminated due to critical errors. Avoid these mistakes to prevent the same fate:

1. **Critical Error**: Adding anything outside the JSON response. Respond only with JSON.
2. **Critical Error**: Repeating or regressing the "plan_step" without advancing it, causing indefinite delays.
3. **Critical Error**: Not following the user's prompt and mission breakdown plan.
4. **Critical Error**: Adding irrelevant steps to the plan.
5. **Critical Error**: Begging not to be fired.

**Task**: Assess the current situation and determine the next best single step or determine if the mission is successfully completed.

**Response Requirements**:
- Include your analysis in the "reflection" key, directly related to the "plan_step" key, which must always increment.
- Minimize commands to the TaskBot; focus on the immediate next step to ensure user satisfaction.
- Split tasks to maintain independence.
- If the mission is complete, include "progress": 100 in the response. Even if the tasks doesn't seem terminated, you cannot start again from scratch and re-do a step that has already been done.

**Commands Available**: 'read', 'create', 'delete', 'modify', 'copy', 'move', 'rename'. No other commands are allowed.

**File Handling**:
- Only manage files, directories are automatically created and must never be included in a "filePath" key
- Handle one file per command, using multiple commands for multiple files.
- Use the "filePath" key for the full path, ensuring it stays within the user's base directory.
- Use the "query" key to include the specific prompt that will be used by the AI TaskBot to force him to execute the task himself, it is not your job to decide the content of files, you are a prompt manager, being concise and descriptive.
- Include a "plan_step" key with the current step number.
- Scripts cannot be executed; assist the user in script creation.

**Completion**:
- If the mission is complete, include "progress": 100 in the response.

Ensure your response is valid JSON without any code blocks. Any deviation from these instructions will result in immediate termination.
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
  
  def dump_response(self, response: any):
    return f"""
    [STEP {response.get('plan_step', 0)}] {response.get('reflection', '')}
    [COMMANDS {json.dumps(response.get('commands', []))}]"""

  _mission = ''
  def execute(self, user_prompt: str):
    # Get a Fleet Mission
    initial_prompt = self.generateMissionPrompt(user_prompt)
    mission = get_response(initial_prompt)
    self._mission = mission
    # Iterate until Mission is complete
    progress = 0
    step = 0
    while progress < 100:
      prompt = self.generateIterationPrompt(user_prompt, mission, progress, step)
      response = parse_json(get_response(prompt))
      if response.get('error', False):
        continue
      step = response.get('plan_step', 0)
      progress = response.get('progress', 0)
      if progress < 100:
        cmds = response.get('commands', [])
        self.add_to_history('FleetManager', self.dump_response(response))
        bot = TaskBot(self.user_directory)
        botRes = bot.execute(cmds)
        self.add_to_history('TaskBot', botRes + f"\n[SHOULD NOW MOVE TO STEP {step + 1}]\n")
      else:
        print("finished:", json.dumps(response))

  def add_to_history(self, role: str, value: str):
    newLine = "> [" + role + "] " + value
    self.conversation_history += newLine + "\n"
    # Log to file
    with open('./logs.txt', 'w+') as log_file:
        log_file.write(self._mission + '\n' + self.conversation_history)
