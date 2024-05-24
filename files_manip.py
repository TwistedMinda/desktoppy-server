import os

def create_file(file_path, content):
  with open(file_path, 'w+') as f:
    f.write(content)

def delete_file(file_path):
  if os.path.exists(file_path):
    os.remove(file_path)

def modify_file(file_path, content):
  with open(file_path, 'w+') as f:
    f.write(content)
