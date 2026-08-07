from langchain_community.embeddings import OllamaEmbeddings

def get_embedding_function():
    """get the embedding function for ollama"""
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )
    return embeddings