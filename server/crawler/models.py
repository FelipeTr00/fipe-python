import asyncio
import httpx
import sqlite3
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
BASE_URL = "http://127.0.0.1:8000/v1"  # Ajuste conforme necessário
DB_URI = os.getenv("DB_URI", "./server/database/db.sqlite")

# Função para obter todas as marcas do banco de dados (Value e codigoTipoVeiculo)
def get_brands():
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("SELECT Value, codigoTipoVeiculo FROM brands")
    brands = cursor.fetchall()
    conn.close()
    return brands  # Retorna uma lista de tuplas [(brand_id, type_id), ...]

# Função para salvar modelos no banco de dados
def save_models(models, type_id, brand_id):
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    
    for model in models:
        try:
            cursor.execute("""
                INSERT INTO models (value, label, brand_id, type_id, codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, updatedAt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(value, brand_id, type_id) DO NOTHING;
            """, (
                model["Value"], model["Label"], brand_id, type_id, 
                model.get("codigoTabelaReferencia"), model.get("codigoTipoVeiculo"), 
                model.get("codigoMarca"), model.get("updatedAt")
            ))
        except Exception as e:
            print(f"[Erro ao salvar modelo {model['Label']}: {e}]")
    
    conn.commit()
    conn.close()

# Função assíncrona para capturar modelos de cada marca respeitando seu type_id correto
async def fetch_models(client, brand_id, type_id):
    url = f"{BASE_URL}/models/{type_id}/{brand_id}"
    try:
        response = await client.get(url)
        data = response.json()
        if data.get("success") and "data" in data:
            save_models(data["data"], type_id, brand_id)
            print(f"✔ {len(data['data'])} modelos salvos para brand {brand_id} (tipo {type_id})")
    except Exception as e:
        print(f"[Erro ao buscar modelos para brand {brand_id} com tipo {type_id}]: {e}")

# Função principal para buscar e salvar todos os modelos
async def main():
    async with httpx.AsyncClient() as client:
        brands = get_brands()  # Lista de tuplas [(brand_id, type_id), ...]
        tasks = [fetch_models(client, brand_id, type_id) for brand_id, type_id in brands]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
