from fastapi import FastAPI, Depends, HTTPException, status, Form, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt, hashlib, paramiko, json, asyncio
from fastapi.concurrency import run_in_threadpool

# === DATABASE ===
DATABASE_URL = "sqlite:///backend/db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === MODELS ===
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ip = Column(String)
    ssh_user = Column(String)
    ssh_password = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

# === SCHEMAS ===
class ServerCreate(BaseModel):
    name: str
    ip: str
    ssh_user: str
    ssh_password: str

# === AUTH ===
SECRET_KEY = "verysecret"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter_by(username=username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# === APP ===
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or user.hashed_password != hashlib.sha256(password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/servers")
def list_servers(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Server).filter_by(owner_id=user.id).all()

@app.post("/servers")
def create_server(server: ServerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_server = Server(
        name=server.name,
        ip=server.ip,
        ssh_user=server.ssh_user,
        ssh_password=server.ssh_password,
        owner_id=current_user.id
    )
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

@app.delete("/servers/{server_id}")
def delete_server(server_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    server = db.query(Server).filter_by(id=server_id, owner_id=user.id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server)
    db.commit()
    return {"detail": "Deleted"}

@app.get("/servers/{server_id}/stats")
def get_stats(server_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    server = db.query(Server).filter_by(id=server_id, owner_id=user.id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server.ip, username=server.ssh_user, password=server.ssh_password, timeout=5)
        stdin, stdout, stderr = ssh.exec_command("python3 /opt/monitor-agent/stats.py")
        output = stdout.read()
        ssh.close()
        return json.loads(output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/servers/{server_id}/stats")
async def websocket_server_stats(websocket: WebSocket, server_id: int, token: str, db: Session = Depends(get_db)):
    await websocket.accept()

    try:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            if not username:
                await websocket.close(code=1008)
                return
            user = db.query(User).filter_by(username=username).first()
            if not user:
                await websocket.close(code=1008)
                return
        except jwt.PyJWTError:
            await websocket.close(code=1008)
            return

        server = db.query(Server).filter_by(id=server_id, owner_id=user.id).first()
        if not server:
            await websocket.close(code=1008)
            return

        while True:
            try:
                def fetch_stats():
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(server.ip, username=server.ssh_user, password=server.ssh_password, timeout=5)
                    stdin, stdout, stderr = ssh.exec_command("python3 /opt/monitor-agent/stats.py")
                    output = stdout.read()
                    ssh.close()
                    return output.decode()

                output = await run_in_threadpool(fetch_stats)
                await websocket.send_text(output)
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("WebSocket disconnected")
