import streamlit as st
import os
import tempfile
import dotenv

# Import your custom modules
import documentLoading as dl
import documentSplitting as ds
import embeddings as emb
import chroma_DB as cdb
import questionLLM as llm

# Load API key from .env
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize your OpenAI client here if needed

# Sidebar configuration for constants
st.sidebar.header("Configuration")
max_tokens = st.sidebar.slider("Max Tokens", value=30, step=1,min_value=30, max_value=1000)
overlap = st.sidebar.slider("Overlap", value=3, step=1,min_value=0, max_value=10)
num_results = st.sidebar.slider("Number of Results", value=3, step=1,min_value=1, max_value=10)

# Persist directory remains fixed
PERSIST_DIRECTORY = 'docs/chroma/'

st.title("PDF Question Answering App")

# File uploader (multiple PDFs)
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files and st.button("Process PDFs"):
    st.info("Processing uploaded PDF files...")
    # Create a temporary directory to store uploaded files
    with tempfile.TemporaryDirectory() as tmpdirname:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(tmpdirname, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.write(f"Saved files to temporary folder: {tmpdirname}")

        # DOCUMENT LOADING
        files = dl.load_pdfs_from_folder(tmpdirname)
        st.write(f"Loaded {len(files)} PDF file(s).")
        
        # DOCUMENT PROCESSING
        st.info("Processing documents...")
        chunked_results = ds.process_loaded_documents(files, max_tokens=max_tokens, overlap=overlap)
        
        # EMBEDDING FUNCTION
        st.info("Initializing embedding function...")
        embedding_function = emb.get_embedding_function()
        
        # CHROMA DB
        st.info("Creating Chroma DB...")
        database = cdb.create_chroma_db(chunked_results, embedding_function, PERSIST_DIRECTORY)
        st.success("Database created successfully!")
        
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
        answer = llm.answer_question(question, combined_info)
        st.write("**Answer:**", answer)
