from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker , Session  
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw

from dotenv import load_dotenv
import os
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from utility import RAG

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
FILE_STORED_LOCATION = os.getenv('FILE_STORED_LOCATION')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)

Base.metadata.create_all(bind=engine)  # Create tables

app = FastAPI()

# app.add_middleware(TrustedHostMiddleware, 
#                    allowed_hosts=["localhost", "https://virtual-buddy-1.onrender.com/"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    user_id: int
    message: str

class AdminRequest(BaseModel):
    username: str
    password: str


@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    print("data received : ",data.username, " ", data.password)
    
    hashed_password = hashpw(data.password.encode('utf-8'), gensalt())
    new_user = User(username=data.username, password=hashed_password.decode('utf-8'))
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        print("Exception : ", e , e.__traceback__)


@app.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user and checkpw(data.password.encode('utf-8'), user.password.encode('utf-8')):
        return {"user_id": user.id,"is_admin": user.is_admin, "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/create_admin")
def create_admin(data: AdminRequest, db: Session = Depends(get_db), current_user: User = Depends(get_db)):
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    
    hashed_password = hashpw(data.password.encode('utf-8'), gensalt())
    new_admin = User(username=data.username, password=hashed_password.decode('utf-8'), is_admin=True)
    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return {"message": "Admin created successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_db)):
    # print(current_user)
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    
    os.makedirs(FILE_STORED_LOCATION, exist_ok=True)
    
    file_location = os.path.join(FILE_STORED_LOCATION, file.filename)
    try:
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        
        RAG.create_vector_storage()

        return {"message": f"File '{file.filename}' uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@app.delete("/delete-file/")
async def delete_file(filename: str,db: Session = Depends(get_db), current_user: User = Depends(get_db)):
    # print(current_user)
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Permission denied")

    file_location = f"{FILE_STORED_LOCATION}/{filename}"
    
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_location)
        RAG.create_vector_storage()
        return {"message": f"File '{filename}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
    
@app.get("/list-files/")
async def list_files(db: Session = Depends(get_db), current_user: User = Depends(get_db)):

    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    
    if not os.path.exists(FILE_STORED_LOCATION):
        os.makedirs(FILE_STORED_LOCATION)
    
    files = os.listdir(FILE_STORED_LOCATION)

    if not files:
        raise HTTPException(status_code=404, detail="No files found in the directory.")

    return {"files": files}


@app.post("/chat")
async def chat(data: ChatRequest, db: Session = Depends(get_db)):
# async def chat(data: ChatRequest):
   
    ai_response = RAG.get_llm_response(data.message)
    print("ai_response : ",ai_response)
    chat = ChatHistory(user_id=data.user_id, user_message=data.message, ai_response=ai_response['doc_ans'])
    db.add(chat)
    db.commit()

    if ai_response['is_doc']:
        return  {"response":ai_response['doc_ans']} 
    else :
        return {"response": ai_response['normal_response']}

