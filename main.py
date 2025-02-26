import os
import openai
import sys
from termcolor import colored
from openai import OpenAI
sys.path.append('../..')

import dotenv


dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
print(colored(f"API Key: {api_key}", 'red'))

import documentLoading as dl
import documentSplitting as ds
import embeddings as emb
import chroma_DB as cdb

folder_path = "pdfs"
print(colored(f"Loading PDFs from folder: {folder_path}", 'blue'))
files = dl.load_pdfs_from_folder(folder_path)

print(colored("Processing loaded documents...", 'green'))
chunked_results = ds.process_loaded_documents(files, max_tokens=30, overlap=1)

print(colored("Getting embedding function...", 'yellow'))
embedding_function = emb.get_embedding_function()

persist_directory = 'docs/chroma/'
print(colored(f"Creating Chroma DB at: {persist_directory}", 'cyan'))
database = cdb.create_chroma_db(chunked_results, embedding_function, persist_directory)

question = "When was Jan born?"
print(colored(f"Performing similarity search for question: {question}", 'magenta'))
docs = database.similarity_search(question, k=3)  # k is the number of results to return

print(colored("Documents found:", 'red'))
for doc in docs:
    print(colored(doc.page_content, 'white'))
