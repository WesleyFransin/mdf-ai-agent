from flask import Flask, render_template, request, send_file
from llm import LanguageModel
from variable_store import VariableStore


import mdfreader as mr

app = Flask('backend')
llm_model = LanguageModel(model='qwen3:14b')
variables_store = VariableStore()

file = mr.Mdf(r"", no_data_loading=True)
llm_model.set_file(file)
llm_model.set_variables_store(variables_store)

'''
Please, plot me three different figures. The first one should contain ambient temperature. The second, IBS3_SOC and battery voltage at the terminals. The third, rpm and speed
'''

@app.route("/")
def home():
    return render_template('index.html')

@app.post('/send-message')
def chat():
    data = request.json
    chat_history = '\n'.join(data['history'])
    response = llm_model.generate_answer(data['message'], chat_history)

    if(isinstance(response, str)):
        return {'response': response}
        
    return send_file(response, mimetype='image/png')

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