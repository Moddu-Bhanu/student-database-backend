import chromadb

from app.core.config import settings
# Store the vector database locally
client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

# Create or load the knowledge collection
collection = client.get_or_create_collection(
    name="student_knowledge",
    metadata={"description": "Knowledge base for the student chatbot"}
)


def add_knowledge(
    document_id: str,
    text: str,
    category: str = "general"
):
    """Add or update a knowledge document."""
    collection.upsert(
        ids=[document_id],
        documents=[text],
        metadatas=[{"category": category}]
    )


def search_knowledge(
    query: str,
    n_results: int = 3
):
    """Find knowledge documents semantically related to a query."""
    if not query.strip():
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    return [
        {
            "id": ids[i],
            "text": documents[i],
            "category": metadatas[i].get("category", "general"),
            "distance": distances[i]
        }
        for i in range(len(documents))
    ]