from app.services.vector_service import (
    add_knowledge,
    search_knowledge
)


# Add sample knowledge documents
add_knowledge(
    document_id="course_001",
    text="B.Tech is an undergraduate engineering degree.",
    category="course"
)

add_knowledge(
    document_id="dept_001",
    text="The AIML department focuses on artificial intelligence "
         "and machine learning.",
    category="department"
)

add_knowledge(
    document_id="dept_002",
    text="The CSE department focuses on computer science "
         "and software engineering.",
    category="department"
)


# Search the knowledge base
results = search_knowledge(
    "What do students learn in artificial intelligence?",
    n_results=3
)

for result in results:
    print(f"ID: {result['id']}")
    print(f"Text: {result['text']}")
    print(f"Category: {result['category']}")
    print(f"Distance: {result['distance']}")
    print("-" * 40)