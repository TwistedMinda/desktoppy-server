# 🫠 Desktoppy Server 🫠

## Introduction

Experience a free-to-use AI in a simple, customizable environment. This project empowers anyone with a decent GPU to bypass the costs and limits of paid services. Use it for daily tasks or fun projects. Ready to get started?

All you need is Python3 🐍, `npm` 📦 & a GPU 💻 !

Features:

- Cross-platform 🌐
- Free-to-use 💸
- Highly customizable 🛠️
- Perfect for everyday tasks ✅
- Great for creative projects 🎨

![Web UI](https://github.com/TwistedMinda/desktoppy-server/blob/main/images/screenshot.png?raw=true)

## Installation

To get started, you'll need to install the necessary dependencies. You can do this by running the following commands:

First create a virtual env (_[and activate it](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)_) and install dependencies in it.

```sh
$ python3 -m venv myenv
$ python3 -m pip install -r requirements.txt
```

(If you don't have CUDA enabled, remove `-i https://download.pytorch.org/whl/cu117` line 8 of `requirements.txt`)

Almost done!
We'll now need our local model

[Install Ollama](https://ollama.com/download)

Download llama3 (text generation) and llava (image recognition) models (get ready for 5GB+)

```sh
$ ollama pull llama3
$ ollama pull llava
```

Apply our custom model blueprint to llama3 (`desktoppy_model.modelfile`)

```sh
$ ./apply_model_blueprint
```

Now you're ready.

## Usage

Simply start the server.

```
python3 src/server.py
```

You can use `curl` to test your installation, sending a POST request from the terminal. Here's how you can do it:

```sh
$ curl --request POST \
  --url "http://localhost:5000/run-script" \
  --data-urlencode "prompt=Show me a cat with elephant ears"
```

## Web UI

🫠 Desktoppy-web available for free directly on [Github](https://github.com/TwistedMinda/desktoppy-web) 🫠
