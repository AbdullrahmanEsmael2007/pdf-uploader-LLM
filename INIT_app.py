#-----------------
#IMPORTS
#-----------------

import os
import openai
import sys
from termcolor import colored
from openai import OpenAI
sys.path.append('../..')
import streamlit as st

import dotenv

#-----------------
#FUNCTIONS
#-----------------

def load_pdfs_from_folder(files):
    import documentLoading as dl
    return dl.load_pdfs_from_folder(files)

def process_loaded_documents(files, max_tokens, overlap):
    print(colored("Processing loaded documents...", 'green'))
    import documentSplitting as ds
    return ds.process_loaded_documents(files, max_tokens=max_tokens, overlap=overlap)

def get_embedding_function(api_key):
    print(colored("Getting embedding function...", 'yellow'))
    import embeddings as emb
    return emb.get_embedding_function(api_key)

def create_chroma_db(chunked_results, embedding_function, persist_directory):
    print(colored(f"Creating Chroma DB at: {persist_directory}", 'cyan'))
    import chroma_DB as cdb
    return cdb.create_chroma_db(chunked_results, embedding_function, persist_directory)

#-----------------
#STREAMLIT APP
#-----------------
def init_app():
    # API KEY
    dotenv.load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")

    st.title("Database Initialization")

    # FOLDER PATH
    import tempfile

    uploaded_files = st.file_uploader("Upload files", type=["pdf", "docx"], accept_multiple_files=True)
    
    
    temp_dir = tempfile.mkdtemp()
    if uploaded_files:
        file_paths = []
        
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)

        st.write(file_paths)

    # MAX TOKENS
    max_tokens = st.slider("Max tokens per chunk:", min_value=10, max_value=100, value=30)

    # OVERLAP
    overlap = st.slider("Chunk overlap:", min_value=0, max_value=10, value=1)

    # NUMBER OF RESULTS

    # PERSIST DIRECTORY
    persist_directory = "docs/chroma"

    # LOAD PDFS
    if st.button("Initialize DB") and file_paths:
        with st.spinner("Loading PDFs..."):
            files = load_pdfs_from_folder(temp_dir)
            st.write(f"Loaded {len(files)} PDFs")
            st.write(f"First PDF: {files[0]}")
        # PROCESS LOADED DOCUMENTS
        with st.spinner("Processing loaded documents..."):
            chunked_results = process_loaded_documents(files, max_tokens, overlap)
            st.write(f"Processed {len(chunked_results)} documents")
            st.write(f"First document: {chunked_results[0]}")

        # GET EMBEDDING FUNCTION
        with st.spinner("Getting embedding function..."):
            embedding_function = get_embedding_function(api_key)
            st.write("Embedding function created")
            st.write(embedding_function)

        # CREATE CHROMA DB
        with st.spinner("Creating Chroma DB..."):
            database = create_chroma_db(chunked_results, embedding_function, persist_directory)

        st.success("Documents loaded and processed successfully!")
    else:   
        st.info("Please upload PDFs to initialize the database.")
