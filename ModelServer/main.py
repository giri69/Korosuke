from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

app = FastAPI()

def startmodal(username: str):
    global runningproject
    runningproject=username
    print(runningproject)
    load_dotenv()
    loader = PyPDFDirectoryLoader('data/'+username)
    documents = loader.load()
    for i, document in enumerate(documents):
        print(f"Document {i}: {document}")
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=200,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    
    index = Chroma.from_documents(chunks, OllamaEmbeddings(model="mxbai-embed-large", show_progress=True), persist_directory="./chroma_db")
    retriever = index.as_retriever()
    
    template = """
    Answer the following question:
    Question: {question}
    Answer the question based only on the following context:
    {context}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = Ollama(model="qwen2:0.5b")
    
    global rag_chain
    rag_chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question")
        }
        | prompt
        | model
        | StrOutputParser()
    )

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

UPLOAD_DIR = "/Users/sushilpandey/Documents/Mine/Research/Korosuke/ModelServer/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Uploadda(BaseModel):
    name: str

class Usermodel:
    def __init__(self, username: str):
        self.username = username

@app.get('/')
async def root():
    return {"message": "API is up and running"}

@app.get("/files/")
async def list_files(username: str = Query(...)):
    try:
        userobj = Usermodel(username=username) 
        UPLOAD_DIR = 'data' + '/' + userobj.username
        if not os.path.exists(UPLOAD_DIR):
            return {"error": "Directory not found"}
        files = [file for file in os.listdir(UPLOAD_DIR) if file.endswith('.pdf')]
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
async def ask_question(data: Uploadda):
    try:
        response = rag_chain.invoke({"question": data.name})
        return {"message": response}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload/")
async def upload_file(username: str = Form(...), file: UploadFile = File(...)):
    userobj = Usermodel(username=username) 
    global runningproject
    runningproject = "fileschanged"
    UPLOAD_DIR = 'data' + '/' + userobj.username
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True) 
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/start_model/")
async def start_model_endpoint(username: str = Form(...)):
    try:
        userobj = Usermodel(username=username) 
        startmodal(userobj.username)
        return {"message": "Model preparation started successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/delete/{filename}")
async def delete_file(filename: str, username: str = Form(...)):
    try:
        userobj = Usermodel(username=username) 
        runningproject="fileschanged"
        UPLOAD_DIR = 'data' + '/' + userobj.username
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            return {"message": f"File '{filename}' deleted successfully"}
        else:
            return {"error": "File not found"}
    except Exception as e:
        return {"error": str(e)}

@app.get('/currentmodel/')
async def getmodelname():
    try:
        print("asked")
        return {
            "modelname": runningproject
        }
    except Exception as e:
        return {"error": str(e)}
runningproject="default"
startmodal(runningproject)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
