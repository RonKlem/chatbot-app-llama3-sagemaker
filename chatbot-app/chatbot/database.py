from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os
from chatbot.utils import get_db_connection, log_error

# Load environment variables
load_dotenv()

def fetch_data_from_db(query: str):
    """
    Fetch data from the database using the given SQL query.
    
    Parameters:
    query (str): The SQL query to execute.

    Returns:
    DataFrame: A PySpark DataFrame containing the query results.
    """
    try:
        db_url = os.getenv('DATABASE_URL')
        spark = SparkSession.builder.getOrCreate()
        
        # Use the get_db_connection utility to manage the connection
        with get_db_connection() as connection:
            result = spark.read \
                .format("jdbc") \
                .option("url", db_url) \
                .option("query", query) \
                .load()
        
        return result
    except Exception as e:
        log_error(e)
        return None

