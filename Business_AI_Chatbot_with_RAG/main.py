import os
import asyncio
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

app = FastAPI(title="Business AI Chatbot API")


DB_URL = "postgresql+psycopg2://admin:adminpassword@127.0.0.1:5433/rag_db"
COLLECTION = "business_docs_v4"


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)


vector_store = PGVector(
    collection_name=COLLECTION,
    connection_string=DB_URL,
    embedding_function=embeddings,
)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 8}
)

system_prompt = (
    "You are an advanced, highly analytical AI assistant.\n"
    "Your strict rule is to answer questions using ONLY the provided context. Never use outside knowledge.\n"
    "However, you must act intelligently. If the user asks a complex, indirect, or analytical question, deeply analyze the context to infer and synthesize the correct answer.\n"
    "Connect the dots between different sentences in the context to form a logical response. Understand acronyms, synonyms, and implied meanings.\n"
    "For example, if the text mentions 'scalable architecture', and the user asks 'Can the system handle growth?', you should answer 'Yes, because it uses a scalable architecture'.\n"
    "If the answer cannot be logically deduced from the context under any circumstances, simply say: 'Not found in document.'\n"
    "Keep answers insightful, clear, and professional.\n\n"
    "Context:\n{context}"
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

qa_chain = create_stuff_documents_chain(llm, prompt_template)
rag_pipeline = create_retrieval_chain(retriever, qa_chain)


class QueryRequest(BaseModel):
    question: str


@app.post("/chat")
async def process_chat(request: QueryRequest):
    """Handles incoming chat queries and retrieves context-aware responses."""
    try:
        result = rag_pipeline.invoke({"input": request.question})
        return {"answer": result.get("answer", "No valid response generated.")}
    except Exception as err:
        return {"answer": f"Internal Server Error: {str(err)}"}


def index_document(file_path: str):
    """Parses, splits, and stores document embeddings in the vector database."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    
    document_chunks = text_splitter.split_documents(documents)

    PGVector.from_documents(
        embedding=embeddings,
        documents=document_chunks,
        collection_name=COLLECTION,
        connection_string=DB_URL,
    )


@app.post("/upload")
async def handle_file_upload(file: UploadFile = File(...)):
    """Handles PDF uploads and triggers the indexing pipeline."""
    storage_dir = "data"
    os.makedirs(storage_dir, exist_ok=True)
    file_path = os.path.join(storage_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    index_document(file_path)
    return {"status": "success", "message": "Document processed and indexed successfully."}