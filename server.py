import os
import time
from flask import Flask, render_template, request, jsonify, g
from flask_expects_json import expects_json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

DATA_PATH = "Data"
FAISS_PATH = "faiss_index"


# Get OpenAI API key from environment variable
os.environ['OPENAI_API_KEY'] = ""

# Create Flask app and authentication
app = Flask(__name__, static_url_path='', static_folder='static')
auth = HTTPBasicAuth()

# User authentication setup
users = {
    "sree": generate_password_hash("secret"),
    "sayankita": generate_password_hash("secret"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# JSON schema for request validation
schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"}
    },
    "required": ["query"]
}

# Load the FAISS index
try:
    embeddings = OpenAIEmbeddings()
    start_time = time.time()
   # db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
except Exception as e:
    print(e)


# Flask routes
@app.route("/", methods=['GET', 'POST'])
@auth.login_required
def index():
    return render_template('index.html')

@app.route("/query", methods=['POST'])
@expects_json(schema)
def query():
    query = g.data['query']
    try:
        start_time = time.time()
        docs = db.similarity_search(query)
        

        start_time = time.time()
        result = chain.run(input_documents=docs, question=query)
        

        return jsonify({"answer": result})
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)