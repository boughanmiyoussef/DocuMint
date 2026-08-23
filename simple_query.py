"""
Simple working query script - uses langchain-chroma
"""

import os
import sys
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"
MODEL = "tinyllama"

def query_documents(query_text):
    """Query documents using direct retrieval + LLM"""
    
    print(f"🔍 Query: {query_text}")
    print("=" * 50)
    
    # Check database
    if not os.path.exists(CHROMA_PATH):
        print("❌ Database not found!")
        print("💡 Run: python populate_database.py first")
        return
    
    # Load database
    print("📚 Loading database...")
    try:
        embeddings = get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        print("✅ Database loaded!")
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        return
    
    # Get relevant documents
    print("🔍 Searching for relevant documents...")
    try:
        results = db.similarity_search_with_score(query_text, k=3)
    except Exception as e:
        print(f"❌ Error searching: {e}")
        return
    
    if not results:
        print("❌ No relevant documents found!")
        return
    
    print(f"✅ Found {len(results)} relevant chunks")
    
    # Show chunks
    print("\n📄 Relevant chunks:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\nChunk {i} (score: {score:.3f}):")
        print(f"{doc.page_content[:300]}...")
    
    # Build context
    context = "\n\n".join([doc.page_content for doc, _ in results])
    
    # Prepare prompt
    prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query_text}

Answer (be concise):"""
    
    print("\n🤖 Generating answer with TinyLlama...")
    print("⏳ This might take 10-30 seconds...")
    
    # Get LLM
    llm = OllamaLLM(
        model=MODEL,
        base_url="http://localhost:11434",
        temperature=0.3
    )
    
    # Generate answer
    try:
        answer = llm.invoke(prompt)
        print("\n💡 Answer:")
        print("=" * 50)
        print(answer)
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        print("💡 Try: ollama pull tinyllama")

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is this paper about?"
    query_documents(query)