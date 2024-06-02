class Store:
  def __init__(self):
    self.requests = {}

  def add_request(self, key, value):
    self.requests[key] = value

  def get_request(self, key):
    return self.requests[key]
  
  def get_history(self):
    history = []
    for request in self.requests.values():
      history.append(f"User: {request.prompt}\nAI Agent: {request.response}")
    return "\n".join(history)
  
  def clear(self):
    self.requests = {}