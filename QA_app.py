import streamlit as st
from langchain_community.vectorstores import Chroma
import embeddings as emb  # Import your custom embedding function
import dotenv
import os
import questionLLM as llm

def qa_app():
    # Load environment variables
    dotenv.load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")

    # Define the persist directory
    PERSIST_DIRECTORY = "docs/chroma"
    NUMBER_OF_RESULTS = 3

    # Load the embedding function
    embedding_function = emb.get_embedding_function(api_key)

    # Load the existing Chroma database
    try:
        st.title("AI-Powered Question Answering System") 
        st.write("Enter your question below, and the AI will retrieve relevant documents and generate an answer.")

        question = st.text_input("Enter your question:")
        number_of_results = st.slider("Number of results:", min_value=1, max_value=10, value=3)
        database = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)
    except:
        st.error(f"Please initialize the app first, before using it")

    # Streamlit UI

    if st.button("Get Answer"):
        if question:
            st.write("**Performing similarity search...**")
            docs = database.similarity_search(question, k=NUMBER_OF_RESULTS)
            
            st.write("### Relevant Documents")
            information = ""
            for doc in docs:
                st.write(doc.page_content)
                information += doc.page_content + "\n\n"
            
            st.write("### Generating Answer...")
            answer = llm.answer_question(question, information, api_key)
            
            st.success("**Answer:**")
            st.write(answer)
        else:
            st.warning("Please enter a question.")
