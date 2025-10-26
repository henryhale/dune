<div align=center>

# dune

🏜️ Navigate the landscape of user intent by shifting language into action.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/henryhale/dune/blob/dev/notebooks/collab.ipynb)

</div>

## Overview

Most AI voice agents or assitants have an underlying text-to-command model that infers the user's intent from their voice transcript or prompt. Such applications(like Google Assistant or Apple's Siri) help the end user to run a sequence of operations that they would otherwise have to do ~manually~ themselves - swiping through screen to complete a task. More use cases for text-to-command models include AI agents like Anthropic's Claude Code or OpenAI's Codex - they infer intent from user's prompt and execute commands on confirmation.

The motivating idea for this project is rooted from the ability to infer intent and expand on it in a way that enables end users to operate any form of application - primarily the web space for now.

## Context

I am building an AI driven application that consists of;

- Text to command model (receives user input and outputs a predefined command to execute)
- Basic TODO App (a simple web app in which input is obtained and the commands will be executed)
- Command Execution Engine (a client side tool to manage model execution and state like intent, confirmation and client side needs like navigation that a user would otherwise do themselves)
- Server running Websockets or REST API or Server Sent Events bridge for sending input and recieving output

To spice things up, the TODO app will capture input using WebSpeech API, convert to text, and send it over to
the server. The app receives a response, sends it to the command execution engine within which execution is done and feedback is collected.

> This is not another Jarvis app. Nope.
> This is an experiment to develop a model that powers a command driven application.

For the MVP demo, consider a multi tab TODO app; `home`, `settings`, `new item form`, `items list`.
Meta conversation commands like `help`, `confirm`, `repeat`, and `explain` are included.

## Commands

List of commands included:

- Navigation: `GO_TO`, `GO_BACK`
- Item selection: `SELECT_ITEM`, `NEXT_ITEM`, `PREVIOUS_ITEM`, `VIEW_ITEM`
- Item management: `CREATE_ITEM`, `EDIT_ITEM`, `DELETE_ITEM`
- Form input: `FILL_FIELD`, `CLEAR_FIELD`, `SUBMIT_FORM`, `CANCEL_FORM`
- Meta commands: `HELP`, `EXPLAIN`, `CONFIRM`, `CANCEL`, `UNDO`, `REDO`, `REPEAT`

## Features

- 20+ command classifications (navigation, CRUD operations, meta commands)
- NLTK-based data augmentation
- scikit-learn TF-IDF + LinearSVC pipeline
- NOOP handling for out-of-domain queries
- Confidence thresholding
- Argument extraction from commands (using Named Entity Recognition)

## Installation

```bash
# clone repository
git clone https://github.com/henryhale/dune.git
cd dune

# create virtual environment
python -m venv venv
source venv/bin/activate  # on windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

## Quick start

After installation, you have to train the model and then use it to predict commands.

1. Using the command line

   ```sh
   # train the model
   python src/train.py

   # run the model interactively
   python src/predict.py --interactive
   ```

2. Using notebooks

   ```sh
   jupyter lab
   ```

   Start with [notebooks/training.ipynb](./notebooks/training.ipynb), the proceed to [notebooks/testing.ipynb](./notebooks/testing.ipynb)

<!--

## Usage

### Training

### Inference

### API Server

## Dataset

## Evaluation -->

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feat/xyz`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feat/xyz`)
5. Open pull request

## Acknowledgments

- scikit-learn for ML framework
- NLTK for NLP preprocessing

## License

MIT License - see [./LICENSE.txt](LICENSE) file
