from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from chatbot.utils import log_error

def parse_output():
    """
    Initialize and return a string output parser.

    Returns:
    StrOutputParser: A string output parser.
    """
    try:
        return StrOutputParser()
    except Exception as e:
        log_error(e)
        return None

def load_documents(file_path: str):
    """
    Load documents from the specified file.

    Parameters:
    file_path (str): The path to the file to load documents from.

    Returns:
    List: A list of loaded documents.
    """
    try:
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        return documents
    except Exception as e:
        log_error(e)
        return []

def split_text(documents):
    """
    Split documents into smaller chunks for processing.

    Parameters:
    documents (List): A list of documents to split.

    Returns:
    List: A list of document chunks.
    """
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        return chunks
    except Exception as e:
        log_error(e)
        return []

def create_prompt_template():
    """
    Create and return a prompt template for generating responses.

    Returns:
    PromptTemplate: A prompt template for generating responses.
    """
    try:
        template = ("""
        You are an AI-powered chatbot designed to provide 
        information and assistance for customers
        based on the context provided to you only. 

        Context: {context}
        Question: {question}
        """)
        prompt = PromptTemplate.from_template(template=template)
        return prompt
    except Exception as e:
        log_error(e)
        return None

def format_prompt(prompt, context, question):
    """
    Format the prompt template with the given context and question.

    Parameters:
    prompt (PromptTemplate): The prompt template to format.
    context (str): The context to include in the prompt.
    question (str): The question to include in the prompt.

    Returns:
    str: The formatted prompt.
    """
    try:
        return prompt.format(context=context, question=question)
    except Exception as e:
        log_error(e)
        return ""
