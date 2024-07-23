from fastapi import FastAPI, File, UploadFile
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from pydantic import BaseModel
import os
import shutil


app=FastAPI()

load_dotenv()
loader = PyPDFDirectoryLoader('data/')
print("1")
documents = loader.load()
print("2")
#print(documents)
print("3")
#print(documents[0].page_content)


text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)
print("4")

chunks = text_splitter.split_documents(documents)
chunks
chunks[7]
print("5")

index = Chroma.from_documents(chunks, OllamaEmbeddings(model="mxbai-embed-large",show_progress=True))
print("6")

retriever = index.as_retriever()

template = """

Answer the following question :
Question: {question}

Answer the question based only on the following context:
{context}

"""
print("7")
prompt = ChatPromptTemplate.from_template(template)
model = Ollama(model="qwen2:0.5b")
print("8")

rag_chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question")
    }
    | prompt
    | model
    | StrOutputParser()
)

class Uploadda(BaseModel):
    name: str

UPLOAD_DIR = "/Users/sushilpandey/Documents/Mine/Research/Korosuke/Server/data"  # Directory where files will be saved
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get('/')
async def root():
    return {"message": rag_chain.invoke({"question": "What is evil quartet? explain properly"})}

@app.post('/ask')
async def ask_question(data: Uploadda):
    print(data)
    response = rag_chain.invoke({"question": data.name})
    return {"message": response}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}