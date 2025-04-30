## Description

This project intends to create a demo for a GenAI agent to interact with INCA data files, plotting data though chat prompts.

## How to run

Simply run it locally with `flask --app backend run` and it will be ready to be accessed on `localhost`.  


## Technologies
The web UI does not use React/Vue or similar library, relying only on regular JS.

The backend is written in Python for its simplicity, using Flask as the main library for the REST API and LangChain to interact with the LLM.