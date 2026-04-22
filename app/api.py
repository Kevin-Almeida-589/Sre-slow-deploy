"""API endpoints"""

import os
import random
import time
from sqlite3 import InternalError
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

TOKEN_FIXO = os.getenv("TOKEN_FIXO")
leak = []


def verify_token(x_token: str = Header(...)):
    """
    Verify token.
    """
    if x_token != TOKEN_FIXO:
        raise HTTPException(status_code=401, detail="Token inválido")
    return True


@app.get("/")
def read_root(_authenticated: Annotated[bool, Depends(verify_token)]):
    """
    Read root endpoint
    """
    return {"message": "Hello, World!"}


@app.get("/health")
def health(_authenticated: Annotated[bool, Depends(verify_token)]):
    """
    Health endpoint
    """
    return {"message": "Healthy"}


@app.get("/slow")
def slow(ms: int, _authenticated: Annotated[bool, Depends(verify_token)]):
    """
    Slow endpoint
    """
    time.sleep(ms / 1000)
    return {"message": f"Slow {ms}ms completed"}


@app.get("/compute")
def compute(_authenticated: Annotated[bool, Depends(verify_token)]):
    """
    Compute endpoint
    """
    for _ in range(10000000):
        pass
    return {"message": "Computation completed"}


@app.get("/leak")
def memory_leak(_authenticated: Annotated[bool, Depends(verify_token)]):
    """
    Memory leak endpoint
    """
    leak.append("x" * 60_000_000)  # 10MB a cada request
    return {"size": len(leak)}


@app.get("/random-error")
def random_error(_authenticated: Annotated[bool, Depends(verify_token)]):
    """
    Random error endpoint
    """
    if random.random() < 0.5:
        raise InternalError("Random error")
    return {"message": "No error"}
