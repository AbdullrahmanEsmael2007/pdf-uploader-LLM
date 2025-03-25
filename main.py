from INIT_app import init_app
from QA_app import qa_app
import streamlit as st

def main():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Init App", "QA App"])
    if selected_page == "Init App":
        init_app()
    elif selected_page == "QA App":
        qa_app()

if __name__ == "__main__":
    main()
