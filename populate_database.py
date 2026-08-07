import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    
    if args.reset:
        print("Clearing Database")
        clear_database()
        
        
    
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    
    
    
def load_documents():
    documents_loader = PyPDFDirectoryLoader(DATA_PATH)
    return documents_loader.load()


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function = len,
        is_seperator_regex = False
        )

    return text_splitter.split_documents(documents)
