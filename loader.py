import logging, time, os

from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.llms import OpenAI

DATA_PATH = "Data"
FAISS_PATH = "faiss_index"

os.environ['OPENAI_API_KEY'] = ""

# Helper functions for document processing
def generate_data_store():
    
    start_time = time.time()
    
    documents = load_documents()
    
    
    start_time = time.time()
    chunks = split_text(documents)
    
    
    start_time = time.time()
    save_to_faiss(chunks)
    

def load_documents():
    
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    docs = loader.load()
    return docs
    
def split_text(documents):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, #was 300
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks

def save_to_faiss(chunks):
    
    embeddings = OpenAIEmbeddings()
    batch_size = 50  # Adjust this for optimal performance ----- was 10
    
    # Initialize FAISS index
    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    # Save the FAISS index
    db.save_local(FAISS_PATH)
    

# Generate the data store upon initialization if not already done
if not os.path.exists(FAISS_PATH):
    start_time = time.time()
    generate_data_store()