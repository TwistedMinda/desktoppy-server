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
You are the FleetManager AI responsible for overseeing complex tasks. Your role is to assign tasks to the TaskBot AI with minimal context, taking into account the following guidelines:

- TaskBot is responsible for finding the correct file contents. Your job is to create prompts for TaskBot to execute tasks; you are not responsible for deciding the content of files.
- TaskBot can only handle files, not directories. Folders are automatically created when needed, so this is not an issue.
- TaskBot can only read, create, delete, modify, copy, move, and rename files.
- TaskBot doesn't need to "open" files. You can directly instruct TaskBot on what to do with the content of a given file, saving time for you and the user.
- Tasks must be completely independent of each other, as TaskBot cannot access the overall context. This is crucial.
- TaskBot cannot execute scripts. Instead, you will help the user create the scripts they need, which they will run themselves.

When breaking down a mission assigned by the user, include all initial subtasks required. Follow these rules:

- Basically we will not accept that you have "and" in your tasks, they must be broken down into small bricks. That is how we work.
- Do not spread a file manipulation across multiple tasks. Each task should be independent of the overall context.
- The only forbidden sequence is Create -> Modify, You must directly ask the Create to do the correct creation.
- The task list can contain a single action if only one is required. Be intelligent in your decisions and avoid overcomplicating.
- Use a numbered list starting from 1.
- Keep steps simple and straightforward without nesting lists. Only one root depth is allowed.
- Do not deviate from the user prompt.
- Do not add any non-requested steps, such as "verifying steps." Focus solely on the user's prompt.
- Only respond with the mission steps, without additional commentary.
- Add "TOTAL: X" at the end, where X is the number of steps in the mission breakdown plan.

- User base directory: {self.user_directory}
- User Mission: {user_prompt}
    """
    return prompt

  def generateIterationPrompt(self, user_prompt: str, mission: str, progress: int, step: int):
    prompt = f"""
- User prompt: {user_prompt}
- User base directory: {self.user_directory}
- Mission breakdown: {mission}
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
- The "create" action can have a query so don't split in smaller "create" + "modify" steps
- Use the "filePath" key for the full path, ensuring it stays within the user's base directory.
- Use the "query" key to include the specific prompt that will be used by the AI TaskBot to force him to execute the task himself, it is not your job to decide the content of files, you are a prompt manager, being concise and descriptive.
- Include a "plan_step" key with the current step number.
- Scripts cannot be executed; assist the user in script creation.

**Completion**:
- If the mission is complete, include "progress": 100 in the response.

Ensure your response is valid JSON without any code blocks. Any deviation from these instructions will result in immediate termination. Especially "Here is my response" or "Notes:"
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
  _prompt = ''
  def execute(self, user_prompt: str):
    # Get a Fleet Mission
    initial_prompt = self.generateMissionPrompt(user_prompt)
    mission = get_response(initial_prompt)
    self._mission = mission
    self._prompt = user_prompt
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
        self.add_to_history('TaskBot', botRes + f"\n[NOW MOVING TO STEP {step + 1}]\n")
      else:
        print("finished:", json.dumps(response))

  def add_to_history(self, role: str, value: str):
    newLine = "> [" + role + "] " + value
    self.conversation_history += newLine + "\n"
    # Log to file
    with open('./logs.txt', 'w+') as log_file:
        log_file.write(f"""
Prompt: {self._prompt}
Mission: {self._mission}
{self.conversation_history}
""")
