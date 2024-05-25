class Store:
  def __init__(self):
    self.requests = {}

  def add_request(self, key, value):
    self.requests[key] = value

  def set_response(self, key, value):
    self.requests[key]["response"] = value

  def remove_request(self, key):
    del self.requests[key]

  def get_request(self, key):
    return self.requests[key]
