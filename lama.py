import ollama

def image_to_text(image_path):
  return ollama.chat(
    model="llava",
    messages=[
      {
        'role': 'user',
        'content': 'Describe this image in 20 characters',
        'images': [image_path]
      }
    ],
  ).get('message').get('content')

def stream_image_to_text(image_path):
  stream = ollama.chat(
    model="llava",
    messages=[
      {
        'role': 'user',
        'content': 'Describe this image in 20 characters',
        'images': [image_path]
      }
    ],
    stream=True
  )
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

def get_response(prompt):
  return ollama.chat(
    model="llama3",
    messages=[
      {
        'role': 'user',
        'content': prompt,
      }
    ]
  ).get('message').get('content')

def stream_response(prompt):
  stream = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
  )

  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)