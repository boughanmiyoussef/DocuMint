import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
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
        length_function=len,
        is_separator_regex=False # Fixed spelling from 'seperator' to 'separator'
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    
    chunks_with_ids = calculate_chunk_ids(chunks) # Fixed function name (removed 's')
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in database: {len(existing_ids)}")
    
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("No new documents to add")
        
def calculate_chunk_ids(chunks): # This matches the function name
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        
def ingest_file(file_path):
    """Ingest a single file into the database"""
    from langchain_community.document_loaders import PyPDFLoader
    
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    chunks = split_documents(documents)
    
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    
    chunks_with_ids = calculate_chunk_ids(chunks) # Fixed function name here too
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
    
    if new_chunks:
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
        return f"Added {len(new_chunks)} new chunks from {os.path.basename(file_path)}"
    else:
        return f"No content to add from {os.path.basename(file_path)}"

if __name__ == "__main__":
    main()