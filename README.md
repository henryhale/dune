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

>More details can be found in the [notebooks](./notebooks/) folder.

### Commands

List of commands included:

- Navigation: `GO_TO`, `GO_BACK`
- Item selection: `SELECT_ITEM`, `NEXT_ITEM`, `PREVIOUS_ITEM`, `VIEW_ITEM`
- Item management: `CREATE_ITEM`, `EDIT_ITEM`, `DELETE_ITEM`
- Form input: `FILL_FIELD`, `CLEAR_FIELD`, `SUBMIT_FORM`, `CANCEL_FORM`
- Meta commands: `HELP`, `EXPLAIN`, `CONFIRM`, `CANCEL`, `UNDO`, `REDO`, `REPEAT`

### Dataset

Generated 4 samples per class manually. Then used Google Gemini to generate more samples to raise the number to
100 samples per class.

### Augmentation

- Current dataset: 5 samples per class (120 total samples / 25 classes).
- To improve: Apply augmentation 60-100x per original sample to get to ~300-500 per class. 
This ensures the model has enough diverse examples to learn robust patterns for each command.

TODO: Use data augmentation techniques (synonyms, paraphrasing) to expand this to 300-500 samples per class.

### Training
The following are some of the approaches to building a classification model entirely using scikit-learn;
1. TF-IDF + Multinomial Naive Bayes
2. TF-IDF + LinearSVC(Support Vector Classifier)
>Currently using option 1

### NOOP

Test threshold: After training, you can also add a confidence threshold—if model confidence < 0.6, treat as NOOP even if it picks a class.

This way your model learns to reject unclear inputs gracefully.
