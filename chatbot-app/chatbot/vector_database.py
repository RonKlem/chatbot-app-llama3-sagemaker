from langchain_community.vectorstores import FAISS
from chatbot.text_processing import load_documents, split_text
from chatbot.utils import log_error
import sagemaker
from sagemaker.predictor import Predictor
import os

# Load environment variables
load_dotenv()

class VectorDatabase:
    def __init__(self):
        self.sagemaker_predictor = Predictor(endpoint_name=os.getenv('SAGEMAKER_ENDPOINT_NAME'))
        self.faiss_index = FAISS.create_index(self.sagemaker_predictor.dim)
        
    def load_data_into_vector_store(self, file_path: str):
        """
        Load data from the given file into the FAISS vector store.

        Parameters:
        file_path (str): Path to the file containing data.
        """
        try:
            documents = load_documents(file_path)
            chunks = split_text(documents)
            texts = [chunk['text'] for chunk in chunks]
            
            # Use SageMaker to generate embeddings
            embeddings = self.sagemaker_predictor.predict(texts)
            
            for i, embedding in enumerate(embeddings):
                self.faiss_index.add(embedding, {"text": texts[i]})
                
        except Exception as e:
            log_error(e)

    def query_vector_store(self, query: str):
        """
        Query the FAISS vector store with the given query.

        Parameters:
        query (str): The query string to search in the vector store.

        Returns:
        List: A list of results from the vector store.
        """
        try:
            query_embedding = self.sagemaker_predictor.predict(query)
            results = self.faiss_index.similarity_search(query_embedding)
            return results
        except Exception as e:
            log_error(e)
            return []