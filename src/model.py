import ollama

def image_to_text(image_path: str):
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

def stream_image_to_text(image_path: str):
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

def get_response(prompt: str, model = 'json_model'):
  return ollama.chat(
    model="json_model",
    messages=[
      {
        'role': 'user',
        'content': prompt,
      }
    ]
  ).get('message').get('content')

def stream_response(prompt: str):
  stream = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
  )

  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)