# from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import io

from llm_tools import make_plots

class LanguageModel():
    def __init__(self, model='qwen3:14b'):    
        # model = OllamaLLM(model=model)
        model = ChatOllama(model=model)

        self.tools_mapping = {
            'make_plots': make_plots
        }
        model = model.bind_tools([self.tools_mapping[t] for t in self.tools_mapping])

        prompt_template = PromptTemplate.from_template(
            """
            You are an assistant for question-answering tasks.
            Always answer matching the language of the question.
            You are having a conversation with a human and the following is the chat history,
            your messages are tagged as <Assistant> and the human messages as <Human>.
            {history}

            Use the chat history as context to keep the conversation going.
            Do not generate the <Assistant> tag when answering. Use tools when convenient. 
            The latest human message is:
            {prompt}
            """
        )
        self.chain = (prompt_template | model)

        self.file = None

    def set_file(self, file):
        self.file = file

    def set_variables_store(self, store):
        self.variables_store = store

    def generate_answer(self, prompt, chat_history):
        response = self.chain.invoke({'prompt': prompt, 'history': chat_history})

        if(not response.tool_calls):
            return response.content

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"].lower()
            selected_tool = self.tools_mapping[tool_name]

            if(tool_name == 'make_plots'):
                if(not self.file):
                    return 'Please add a file before plotting'
                
                args = tool_call["args"]
                args['variables_store'] = self.variables_store

                tool_output = selected_tool.invoke(args)

                plt_fig = self.file.plot_backend(tool_output)
                buf = io.BytesIO()
                plt_fig.savefig(buf, format='png')
                buf.seek(0)
                return buf

            tool_output = selected_tool.invoke(tool_call["args"])


        print(response)
