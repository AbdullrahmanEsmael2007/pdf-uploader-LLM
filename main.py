import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

import documentLoading as dl
import documentSplitting as ds

folder_path = "wikipedia_pdfs"
files = dl.load_pdfs_from_folder(folder_path)

chunked_results = ds.process_loaded_documents(files, max_tokens=30, overlap=1)

from termcolor import colored

for key, value in chunked_results.items():
    print(colored(f"Document: {key}", 'green'))

    for chunk in value:
        print(colored(f"Page: {chunk['page']}, Chunk {chunk['chunk_number']}:","red"), chunk['chunk'])