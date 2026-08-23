from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.embeddings.bedrock import BedrockEmbeddings

def get_embedding_function():
    # For local Ollama (use this)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # For AWS Bedrock (uncomment if you have AWS credentials)
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    return embeddings