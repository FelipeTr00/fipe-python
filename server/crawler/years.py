import asyncio
import httpx
import sqlite3
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
BASE_URL = "http://127.0.0.1:8000/v1"  # Ajuste conforme necessário
DB_URI = os.getenv("DB_URI", "./server/database/db.sqlite")

# Função para obter todos os modelos do banco de dados
def get_models():
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("SELECT value, codigoMarca, codigoTipoVeiculo FROM models")
    models = cursor.fetchall()
    conn.close()
    return models  # Lista de tuplas [(model_id, brand_id, type_id), ...]

# Função para salvar anos no banco de dados
def save_years(years, type_id, brand_id, model_id):
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    
    for year in years:
        try:
            cursor.execute("""
                INSERT INTO years (value, label, codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo, updatedAt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(value, codigoMarca, codigoModelo) DO NOTHING;
            """, (
                year["Value"], year["Label"], year["codigoTabelaReferencia"], 
                year["codigoTipoVeiculo"], year["codigoMarca"], 
                year["codigoModelo"], year["updatedAt"]
            ))
        except Exception as e:
            print(f"[Erro ao salvar ano {year['Label']}: {e}]")
    
    conn.commit()
    conn.close()

# Função assíncrona para buscar os anos de cada modelo
async def fetch_years(client, model_id, brand_id, type_id):
    url = f"{BASE_URL}/years/{type_id}/{brand_id}/{model_id}"
    try:
        response = await client.get(url)
        data = response.json()
        if data.get("success") and "data" in data:
            save_years(data["data"], type_id, brand_id, model_id)
            print(f"✔ {len(data['data'])} anos salvos para modelo {model_id} (marca {brand_id}, tipo {type_id})")
    except Exception as e:
        print(f"[Erro ao buscar anos para modelo {model_id}]: {e}")

# Função principal para buscar e salvar os anos dos modelos
async def main():
    async with httpx.AsyncClient() as client:
        models = get_models()  # Lista de tuplas [(model_id, brand_id, type_id), ...]
        tasks = [fetch_years(client, model_id, brand_id, type_id) for model_id, brand_id, type_id in models]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
