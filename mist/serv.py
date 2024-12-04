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
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],   
)
 
class QueryRequest(BaseModel):
    query: str
 
loader = None
documents = None
vector = None
retriever = None
model = None
document_chain = None
retrieval_chain = None 
UPLOAD_DIRECTORY = "data/"
 
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
 
def setup_files():
    global loader, documents, vector, retriever, model, document_chain, retrieval_chain

    try:
        loader = PyPDFDirectoryLoader(UPLOAD_DIRECTORY)
        docs = loader.load()
        if not docs:
            raise HTTPException(status_code=400, detail="No PDFs found in the uploaded directory.")
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key='KkhrcMWl3aJqOXNbRfRLf3jZKXHZl3sz')
        vector = Chroma.from_documents(documents, embeddings)
        retriever = vector.as_retriever()  # Fixed here
        model = ChatMistralAI(mistral_api_key='uI1XdxkkIiYwixEbndeYDYjknjU5w2Yv')
 
        prompt = ChatPromptTemplate.from_template("""You are an expert assistant. Answer the question below accurately and concisely based solely on the provided context. If the context does not provide enough information, respond with "The provided context does not contain enough information to answer this question."
<context>
{context}
</context>
Question: {input}
Answer:
""")
 
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        logging.info("Files have been processed and system is ready.")
    except Exception as e:
        logging.error(f"Error in setting up files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):  
    try: 
        for existing_file in os.listdir(UPLOAD_DIRECTORY):
            file_path = os.path.join(UPLOAD_DIRECTORY, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
 
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logging.info(f"File uploaded successfully: {file.filename}")
 
        setup_files()

        return {"filename": file.filename, "message": "File uploaded successfully and system reconfigured."}
    except Exception as e:
        logging.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

 
@app.post("/process_embeddings/")
async def process_embeddings():
    try: 
        setup_files()
        return {"message": "Embeddings have been processed successfully and system is ready for queries."}
    except Exception as e:
        logging.error(f"Error processing embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
 
@app.post("/query/")
async def get_answer(query_request: QueryRequest):
    try: 
        if not retrieval_chain:
            raise HTTPException(status_code=400, detail="Files are not uploaded or processed yet.")
         
        response = retrieval_chain.invoke({"input": query_request.query})
        return {"answer": response["answer"]}
    except Exception as e:
        logging.error(f"Error during query processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
 
@app.post("/clear_database/")
async def clear_database(): 
    global vector, retriever, retrieval_chain

    try: 
        if vector is None:
            raise HTTPException(status_code=400, detail="Vector store is not initialized.")
 
        vector._client.reset()   
 
        vector = None
        retriever = None
        retrieval_chain = None

        logging.info("ChromaDB cleared successfully.")
        return {"message": "ChromaDB has been cleared successfully."}
    except Exception as e:
        logging.error(f"Error clearing ChromaDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing ChromaDB: {str(e)}")
