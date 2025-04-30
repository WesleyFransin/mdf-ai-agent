from flask import Flask, render_template, request
from llm import LanguageModel

app = Flask('backend')
llm_model = LanguageModel(model='gemma3:12b')

@app.route("/")
def home():
    return render_template('index.html')

@app.post('/send-message')
def chat():
    data = request.json
    chat_history = '\n'.join(data['history'])
    response = llm_model.generate_answer(data['message'], chat_history)
    return {'response': response}

@app.route('/variables')
def variables():
    return render_template('variables.html')