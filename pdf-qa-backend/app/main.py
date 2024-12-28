from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
import fitz  # PyMuPDF
from sqlalchemy.orm import Session
from app.models import Document
from app.database import SessionLocal, engine

app = FastAPI()

# Enable CORS (Allow requests from your frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains to make requests, use specific URLs for security in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize database
Document.metadata.create_all(bind=engine)

class QuestionRequest(BaseModel):
    question: str
    file_name: str

# Helper function to process PDF text
def process_pdf(file_path: str):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Endpoint to upload PDF
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    file_location = f"pdfs/{file.filename}"
    os.makedirs("pdfs", exist_ok=True)
    
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Save the document metadata to the database
    db = SessionLocal()
    db.add(Document(file_name=file.filename, file_path=file_location))
    db.commit()
    db.refresh(Document)
    db.close()

    return {"filename": file.filename}

# Endpoint to ask a question about a PDF
@app.post("/ask/")  # You can now make requests to this endpoint from your frontend
def ask_question(request: QuestionRequest):
    # Retrieve the PDF text from file
    file_path = f"pdfs/{request.file_name}"
    if not Path(file_path).exists():
        return JSONResponse(status_code=404, content={"message": "File not found"})
    
    pdf_text = process_pdf(file_path)
    
    # Here, you can integrate with LangChain or another NLP tool for question answering
    # For now, we will return a dummy response
    answer = f"Answer based on {request.question} from {request.file_name}"
    
    return {"answer": answer}
