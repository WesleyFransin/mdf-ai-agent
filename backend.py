from flask import Flask, render_template, request
from llm import LanguageModel
from variable_store import VariableStore

app = Flask('backend')
llm_model = LanguageModel(model='gemma3:12b')
variables_store = VariableStore()

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

@app.route('/variables/search')
def search_variable():
    if(request.method == 'GET'):
        var_description = request.args.get('description')
        results_number = request.args.get('size')
    else:
        data = request.json
        var_description = data.get('description')
        results_number = request.args.get('size')
    
    if(results_number):
        return variables_store.find_match(var_description, n=int(results_number))
    return variables_store.find_match(var_description)