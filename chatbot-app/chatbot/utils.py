import logging
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# Load environment variables
load_dotenv()

def setup_logging(log_file: str):
    """
    Set up logging configuration.
    
    Parameters:
    log_file (str): Path to the log file.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def log_error(error: Exception):
    """
    Log an error message.

    Parameters:
    error (Exception): The exception to log.
    """
    logging.error(f"An error occurred: {str(error)}")

def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
    Connection: A SQLAlchemy database connection.
    """
    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)
    return engine.connect()

def format_query_results(results: pd.DataFrame) -> str:
    """
    Format query results for better readability.

    Parameters:
    results (pd.DataFrame): The query results as a Pandas DataFrame.

    Returns:
    str: The formatted query results as a string.
    """
    return results.to_string(index=False)