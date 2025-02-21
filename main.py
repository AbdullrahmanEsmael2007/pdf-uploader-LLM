import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

import documentLoading as dl
import documentSplitting as ds
import embeddings as emb
import chroma_DB as cdb

folder_path = "wikipedia_pdfs"
files = dl.load_pdfs_from_folder(folder_path)

chunked_results = ds.process_loaded_documents(files, max_tokens=30, overlap=1)

embedding_function = emb.get_embedding_function()

persist_directory = 'docs/chroma/'
database = cdb.create_chroma_db(chunked_results, embedding_function, persist_directory)


question = "In what weight category does Veronika  Mykolaivna compete?"

docs = database.similarity_search(question,k=3) # k is the number of results to return

for doc in docs:
    print(doc.page_content)