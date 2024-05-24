import os

def read_file(file_path):
  try:
    with open(file_path, 'r') as f:
      return f.read()
  except Exception as e:
    return ""

def get_all_filenames(directory):
  filenames = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      filenames.append(os.path.join(root, file))
  return filenames

def create_file(file_path, content):
  with open(file_path, 'w+') as f:
    f.write(content)

def delete_file(file_path):
  if os.path.exists(file_path):
    os.remove(file_path)

def modify_file(file_path, content):
  with open(file_path, 'w+') as f:
    f.write(content)
