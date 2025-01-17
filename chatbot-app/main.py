from chatbot.vector_database import initialize_vector_store, load_data_into_vector_store, query_vector_store
from chatbot.text_processing import create_prompt_template, format_prompt
from chatbot.database import fetch_data_from_db
from chatbot.utils import setup_logging, log_error, format_query_results
import os
from dotenv import load_dotenv
import sagemaker
from sagemaker.predictor import Predictor

class QueryBuilder:
    
    def __init__(self):
        """
        Initialize the QueryBuilder class and load environment variables.
        """
        load_dotenv()
        setup_logging('chatbot.log')
        self.vector_store = initialize_vector_store()
        
        # Create a SageMaker Predictor
        self.predictor = Predictor(endpoint_name=os.getenv('SAGEMAKER_ENDPOINT_NAME'))

    def generate_sql_query(self, question: str) -> str:
        """
        Generate an SQL query based on the user's financial or accounting question using LLaMa3.

        Parameters:
        question (str): The user's question.

        Returns:
        str: The generated SQL query.
        """
        prompt_template = """
        You are an AI assistant designed to help users with financial and accounting queries. Based on the user's question, generate an appropriate SQL query to fetch the required data.

        User Question: "{question}"

        SQL Query:
        """
        prompt = prompt_template.format(question=question)
        
        # Use SageMaker to generate the SQL query
        sql_query = self.predict(prompt)
        
        # Return the generated SQL query as a string
        return sql_query.strip()

    def predict(self, data):
        """
        Make predictions using the deployed SageMaker model.

        Parameters:
        data (Any): Input data for prediction.

        Returns:
        Any: Prediction result.
        """
        try:
            response = self.predictor.predict(data)
            return response
        except Exception as e:
            log_error(e)
            return None

    def fetch_and_predict(self, query: str):
        """
        Fetch data from the database and then make predictions using the SageMaker model.

        Parameters:
        query (str): The SQL query to execute.

        Returns:
        Any: The prediction result.
        """
        try:
            # Fetch data from the database
            db_results = fetch_data_from_db(query)
            if db_results is not None:
                formatted_results = format_query_results(db_results.toPandas())
                # Use the fetched data as input to the SageMaker model
                prediction = self.predict(formatted_results)
                return prediction
            else:
                return "No results found in database."
        except Exception as e:
            log_error(e)
            return None

    def answer_financial_question(self, question: str):
        """
        Generate an answer to the user's financial or accounting question.

        Parameters:
        question (str): The user's question.

        Returns:
        str: The generated answer.
        """
        try:
            # Generate SQL query based on the question
            sql_query = self.generate_sql_query(question)
            
            # Fetch data from the database and predict
            prediction = self.fetch_and_predict(sql_query)
            return prediction
        except Exception as e:
            log_error(e)
            return ""

# Execution block
if __name__ == "__main__":
    qb = QueryBuilder()
    
    # Example of asking a financial question
    question = "What was the total revenue last quarter?"
    answer = qb.answer_financial_question(question)
    print(answer)
