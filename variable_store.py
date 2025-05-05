from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class VariableStore():

    def __init__(self):
        embedding_model_name = "sentence-transformers/all-mpnet-base-v2"

        model_kwargs = {"device": "cuda"}
        embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs=model_kwargs
        )

        self.vector_store = Chroma(
            collection_name="db_variables",
            embedding_function=embeddings,
            persist_directory="./variables_db",
        )

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