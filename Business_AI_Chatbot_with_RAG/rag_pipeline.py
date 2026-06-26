import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import PGVector

load_dotenv()

CONNECTION_STRING = "postgresql+psycopg2://admin:adminpassword@127.0.0.1:5433/rag_db"
COLLECTION_NAME = "business_docs_v3"

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


def process_and_store_data(file_path=None, url=None):
    documents = []

    if file_path:
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
        print(f"Loaded PDF: {file_path}")
    elif url:
        loader = WebBaseLoader(url)
        documents.extend(loader.load())
        print(f"Loaded Website: {url}")
    else:
        print("Please provide a file_path or url.")
        return False

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings and storing in pgvector...")
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
    )

    print("Data successfully stored in pgvector!")
    return True


if __name__ == "__main__":
    print("Storing sample PDF into pgvector...")
    success = process_and_store_data(file_path="sample_business_info.pdf")
    if success:
        print("Done! Now you can query the bot.")