from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import sqlite3

import os

class VariableStore():

    def __init__(self, collection_name='db_variables', persist_directory='./variables_db'):
        embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
        os.environ['http_proxy'] = ''
        os.environ['https_proxy'] = ''

        model_kwargs = {"device": "cuda"}
        embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs=model_kwargs
        )

        self.vector_store = Chroma(
            collection_name= collection_name,
            embedding_function=embeddings,
            persist_directory= persist_directory,
        )

        self.persist_directory = persist_directory
        self.sql_con = None
        self.sql_cur = None

    def find_match(self, description, n=5):
        matches = self.vector_store.similarity_search(
            description,
            k=n)

        variables = [] # (name, description)
        for m in matches:
            name = m.metadata['signal_name']
            description = m.page_content
            variables.append((name, description))

        return variables
    
    def get_sql_cursor(self):
        if(self.sql_cur):
            return self.sql_cur

        self.sql_con = sqlite3.connect("variables_db/chroma.sqlite3")
        self.sql_cur = self.sql_con.cursor()
        return self.sql_cur
    
    def close_sql_con(self):
        self.sql_con.close()