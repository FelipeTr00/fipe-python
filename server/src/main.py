import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv
from fastapi import FastAPI
from src.routes import router

load_dotenv()

app = FastAPI()

SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

app.include_router(router)

if __name__ == "__main__":
    
    import uvicorn
    print(f"Abra o link para acessar a API: http://localhost:{SERVER_PORT}/v1")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
