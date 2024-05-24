# 🫠 Desktoppy 🫠

## Introduction

Welcome to our AI project's safe zone! Link a directory, your safe zone, and start interacting with the AI to manipulate the files with you.

## Installation

To get started, you'll need to install the necessary dependencies. You can do this by running the following commands:

First create a virtual env (_[and activate it](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)_) and install dependencies in it.

```sh
$ python3 -m venv myenv
$ python3 -m pip install -r requirements.txt
```

Almost done!
We'll now need our local model (LLama3 by default but feel free to change)

[Install Ollama](https://ollama.com/download)

Test your installation by installing the model of your choice

```sh
$ ollama pull llama3
```

## Launch

Once you have everything installed, you're ready to start exploring the world of AI! Simply run the main script or application and follow the prompts to begin.

```
python3 server.py
```

You can use `curl` to test your installation, send a GET request from the terminal. Here's how you can do it:

```sh
$ curl --get \
  --data-urlencode "folder=C:/Users/Julien/projects/ai/safe_zone/" \
  --data-urlencode "prompt=Create a fancy file for me" \
  --data-urlencode "file_paths=path/to/file1,path/to/file2" \
  "http://localhost:5000/run-script"
```

## Web UI

🫠 Coming soon 🫠
