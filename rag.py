import os
import ollama
import chromadb
from pypdf import PdfReader


# ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="course_material"
)


# Convert text into embeddings
def get_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]


# Read PDF
def load_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Split course material into chunks
def split_text(text, chunk_size=800):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks


# Add PDF to vector database
def add_pdf(file_path):

    print("Reading course material...")

    text = load_pdf(file_path)

    chunks = split_text(text)

    print(f"Created {len(chunks)} chunks.")

    for i, chunk in enumerate(chunks):

        embedding = get_embedding(chunk)

        collection.add(
            ids=[f"{os.path.basename(file_path)}_{i}"],
            documents=[chunk],
            embeddings=[embedding]
        )

    print("Course material added successfully!")


# Search relevant course content
def search_course(query, n_results=3):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]


# Answer questions using only the retrieved course content
def ask_question(question, model="qwen2.5:3b"):

    documents = search_course(question)
    context = "\n\n---\n\n".join(documents)

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful study assistant. Answer only from the "
                    "provided course material. If the answer is not present, "
                    "say that the course material does not contain enough "
                    "information."
                ),
            },
            {
                "role": "user",
                "content": f"Course material:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    return response["message"]["content"]