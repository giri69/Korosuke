from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from pydantic import BaseModel
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
import shutil
import logging

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Create a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str

# Setup components (for now, placeholders)
loader = None
documents = None
vector = None
retriever = None
model = None
document_chain = None
retrieval_chain = None

# Directory to store uploaded files
UPLOAD_DIRECTORY = "data/"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Setup the model and embeddings (to be called after uploading files)
def setup_files():
    global loader, documents, vector, retriever, model, document_chain, retrieval_chain

    try:
        # Load documents from the directory where PDFs are uploaded
        loader = PyPDFDirectoryLoader(UPLOAD_DIRECTORY)
        docs = loader.load()
        if not docs:
            raise HTTPException(status_code=400, detail="No PDFs found in the uploaded directory.")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)

        # Define the embedding model
        embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key='SgiDaJqKGryyjYEONUYbp9OQTjXZWcia')

        # Create the vector store
        vector = Chroma.from_documents(documents, embeddings)

        # Define retriever interface
        retriever = vector.as_retriever()

        # Define LLM
        model = ChatMistralAI(mistral_api_key='SgiDaJqKGryyjYEONUYbp9OQTjXZWcia')

        # Define prompt template
        prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

        # Create a retrieval chain to answer questions
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        logging.info("Files have been processed and system is ready.")
    except Exception as e:
        logging.error(f"Error in setting up files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# FastAPI endpoint to upload files
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to the 'data/' directory
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        logging.info(f"File uploaded successfully: {file.filename}")

        # After saving, setup the files and embeddings
        setup_files()

        return {"filename": file.filename, "message": "File uploaded successfully and system reconfigured."}
    except Exception as e:
        logging.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# FastAPI endpoint to process embeddings before querying
@app.post("/process_embeddings/")
async def process_embeddings():
    try:
        # Process embeddings (loading documents, splitting, and embedding them)
        setup_files()
        return {"message": "Embeddings have been processed successfully and system is ready for queries."}
    except Exception as e:
        logging.error(f"Error processing embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# FastAPI endpoint to query the uploaded files
@app.post("/query/")
async def get_answer(query_request: QueryRequest):
    try:
        # Ensure the system is set up before querying
        if not retrieval_chain:
            raise HTTPException(status_code=400, detail="Files are not uploaded or processed yet.")
        
        # Run the retrieval chain to get the response
        response = retrieval_chain.invoke({"input": query_request.query})
        return {"answer": response["answer"]}
    except Exception as e:
        logging.error(f"Error during query processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with `uvicorn`:
# uvicorn fastapi_server:app --reload
