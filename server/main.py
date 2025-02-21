import sys
import os
import json
from fastapi import FastAPI
from server.src.routes import router

with open("server/config.json", "r") as file:
    config = json.load(file)

# Add swagger
app = FastAPI(
    title="API FIPE-PYTHON",
    description="Felipe Alves de Morais.",
    version=config.get("VERSION", "v1"),
    contact={
        "name": "Felipe Alves de Morais"
    },
)

VERSION = config.get("VERSION", "api")
SERVER_PORT = config.get("SERVER_PORT", 8000)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "API rodando com sucesso!", "docs": f"http://localhost:{SERVER_PORT}/docs"}

if __name__ == "__main__":
    import uvicorn
    print(f"Link API: http://localhost:{SERVER_PORT}/{VERSION}")
    print(f"Documentação Swagger: http://localhost:{SERVER_PORT}/docs")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
