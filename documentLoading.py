import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdf_pages(pdf_path):
    loader = PyPDFLoader(pdf_path)
    return loader.load()

def load_pdfs_from_folder(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            loader = load_pdf_pages(os.path.join(folder_path, filename))
            files.extend(loader)
    return files



