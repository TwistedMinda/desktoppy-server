class Store:
  def __init__(self):
    self.requests = {}

  def add_request(self, key, value):
    self.requests[key] = value

  def get_request(self, key):
    return self.requests[key]
