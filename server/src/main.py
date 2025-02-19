import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ..config import config
from fastapi import FastAPI
from src.routes import router

app = FastAPI()

VERSION = config.get("VERSION", "api")
SERVER_PORT = config.get("SERVER_PORT", 8000)

app.include_router(router)

if __name__ == "__main__":
    
    import uvicorn
    print(f"Abra o link para acessar a API: http://localhost:{SERVER_PORT}/{VERSION}")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
