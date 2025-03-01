import streamlit as st
import tempfile
import os 

# Import your custom modules
import documentLoading as dl
import documentSplitting as ds
import embeddings as emb
import chroma_DB as cdb
import questionLLM as llm
from openai import OpenAI

# Load API key from .env
# Initialize your OpenAI client here if needed

# Sidebar configuration for constants
def sidebar_config():
    st.sidebar.header("Configuration")
    
    num_results = st.sidebar.slider("Number of Results", value=3, step=1,min_value=1, max_value=10)

def check_api_key(api_key):
    client = OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "say SA"}
            ],
        max_tokens=1
        )
        print(completion.choices[0].message.content)
        return True
    except Exception as e:
        return False

def force_api_key():
    apikey = None
    api_key = st.text_input("OpenAI API Key")

    if st.button("Enter API key"):
        all_true = api_key is not None and check_api_key(api_key) 
        if all_true:
            st.session_state.api_key = api_key
            return api_key

        elif api_key is None:
            st.error("Please enter your OpenAI API key.")
        elif check_api_key(api_key):
            st.error("Invalid API key.")
        
   
        


# Persist directory remains fixed
PERSIST_DIRECTORY = 'docs/chroma/'
sidebar_config()
st.title("PDF Question Answering App")

st.session_state["database"] = None

st.session_state.api_key = force_api_key()
# File uploader (multiple PDFs)
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

with st.expander("Configuration"):
    max_tokens = st.slider("Max Tokens", value=30, step=1,min_value=30, max_value=1000)
    overlap = st.slider("Overlap", value=3, step=1,min_value=0, max_value=10)

if uploaded_files and st.button("Process PDFs") and st.session_state.database is None and st.session_state.api_key is not None:
    with st.spinner("Processing uploaded PDF files..."):
        st.session_state["loaded"] = False  
    # Create a temporary directory to store uploaded files
    with tempfile.TemporaryDirectory() as tmpdirname:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(tmpdirname, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # DOCUMENT LOADING
        files = dl.load_pdfs_from_folder(tmpdirname)
        
        # DOCUMENT PROCESSING
        with st.spinner("Processing documents..."):
            chunked_results = ds.process_loaded_documents(files, max_tokens=max_tokens, overlap=overlap)
        
        # EMBEDDING FUNCTION
        with st.spinner("Creating embedding function..."):
            embedding_function = emb.get_embedding_function(api_key)
        st.write(api_key)
        
        # CHROMA DB
        with st.spinner("Creating Chroma DB..."):
            database = cdb.create_chroma_db(chunked_results, embedding_function, PERSIST_DIRECTORY)
        
        # Store the database in session_state for reuse during Q&A
        st.session_state["database"] = database
        st.session_state["loaded"] = True

# Check if the database has been created
if st.session_state.get("loaded", False):
    st.subheader("Ask a Question")
    question = st.text_input("Enter your question:")
    if st.button("Submit Question") and question:
        st.info("Performing similarity search...")
        database = st.session_state["database"]
        docs = database.similarity_search(question, k=num_results)
        
        # Display documents used for answering and accumulate their content
        combined_info = ""
        st.write("### Documents found:")
        for doc in docs:
            st.write(doc.page_content)
            combined_info += doc.page_content
        
        st.info("Generating answer...")
        answer = llm.answer_question(question, combined_info, api_key)
        st.write("**Answer:**", answer)

