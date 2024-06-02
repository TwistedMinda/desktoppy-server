from text_model import *
from request import *

prompt = """
Generate a dog image that flies into space
then generate a cat with bunny ears
"""

req = Request(prompt)
req.execute()

print(req.to_dict())