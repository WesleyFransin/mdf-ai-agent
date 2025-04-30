from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate


class LanguageModel():
    def __init__(self, model='gemma3:12b'):    
        model = OllamaLLM(model=model)
        prompt_template = PromptTemplate.from_template(
            """
            You are an assistant for question-answering tasks.
            Always answer matching the language of the question.
            You are having a conversation with a human and the following is the chat history,
            your messages are tagged as <Assistant> and the human messages as <Human>.
            {history}

            Use the chat history as context to keep the conversation going.
            Do not generate the <Assistant> tag when answering.
            The latest human message is:
            {prompt}
            """
        )
        self.chain = (prompt_template | model)

    def generate_answer(self, prompt, chat_history):
        # return self.model.invoke(prompt)
        return self.chain.invoke({'prompt': prompt, 'history': chat_history})