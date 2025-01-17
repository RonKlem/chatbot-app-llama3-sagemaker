from langchain.llms import LLaMa3
from langchain import LangChain
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Initialize LLaMa3 model with API key from environment variables
llama = LLaMa3(model="llama-3-model", api_key=os.getenv('LLaMa3_API_KEY'))

# Initialize LangChain with the LLaMa3 model
langchain = LangChain(llm=llama)

