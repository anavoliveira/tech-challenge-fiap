from fastapi import FastAPI, Depends, HTTPException, status, Header
from typing import Optional
import jwt
import datetime

app = FastAPI()

JWT_SECRET = "SEGREDO"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600
TEST_USERNAME = "admin"
TEST_PASSWORD = "secret"

def create_token(username: str):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Formato inválido")
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["username"]
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

@app.post("/login")
def login(username: str, password: str):
    if username == TEST_USERNAME and password == TEST_PASSWORD:
        token = create_token(username)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")


