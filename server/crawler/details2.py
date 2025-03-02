import asyncio
import httpx
import sqlite3
import os
import json

# Carregar configurações do JSON
with open("server/config.json", "r") as file:
    config = json.load(file)

# Configuração de variáveis globais
VERSION = config.get("VERSION", "v1")
BASE_URL = f"http://127.0.0.1:8000/{VERSION}"
DB_URI = config.get("DB_URI", "./server/database/db.sqlite")
semaphore = asyncio.Semaphore(5)  # Limite de requisições concorrentes


def get_request_urls():
    """Gera as URLs das requisições com base na query SQL otimizada."""
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()

    query = """
SELECT
    'http://127.0.0.1:8000/v1/details/' ||
    m.codigoTipoVeiculo || '/' ||
    m.codigoMarca || '/' ||
    m.value || '/' ||
    substr(y.value, 1, instr(y.value, '-') - 1) || 
    '?typeGas=' || 
    CASE 
        WHEN instr(y.value, '-') > 0 THEN substr(y.value, instr(y.value, '-') + 1) 
        ELSE '1' 
    END AS uri,
    m.codigoTipoVeiculo,
    m.codigoMarca,
    m.value AS codigoModelo,
    substr(y.value, 1, instr(y.value, '-') - 1) AS anoModelo,
    CASE 
        WHEN instr(y.value, '-') > 0 THEN substr(y.value, instr(y.value, '-') + 1) 
        ELSE '1' 
    END AS codigoTipoCombustivel 
FROM models m
LEFT JOIN years y ON y.codigoModelo = m.value
WHERE y.codigoModelo IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM details d
    WHERE d.codigoTipoVeiculo = m.codigoTipoVeiculo
      AND d.codigoMarca = m.codigoMarca
      AND d.codigoModelo = m.value
      AND d.anoModelo = substr(y.value, 1, instr(y.value, '-') - 1)
);


    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return rows  # Retorna uma lista de tuplas (url, tipoVeiculo, marca, modelo, ano)


def save_details(details):
    """Insere os detalhes na tabela 'details', evitando duplicatas."""
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO details (
                Valor, Marca, Modelo, Combustivel, MesReferencia, Autenticacao,
                TipoVeiculo, SiglaCombustivel, DataConsulta, codigoTabelaReferencia,
                codigoTipoVeiculo, codigoMarca, codigoModelo, anoModelo,
                codigoTipoCombustivel, tipoConsulta, updatedAt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo, anoModelo) 
            DO NOTHING;
        """,
            (
                details.get("Valor"),
                details.get("Marca"),
                details.get("Modelo"),
                details.get("Combustivel"),
                details.get("MesReferencia"),
                details.get("Autenticacao"),
                details.get("TipoVeiculo"),
                details.get("SiglaCombustivel"),
                details.get("DataConsulta"),
                details.get("codigoTabelaReferencia"),
                details.get("codigoTipoVeiculo"),
                details.get("codigoMarca"),
                details.get("codigoModelo"),
                details.get("anoModelo"),
                details.get("codigoTipoCombustivel"),
                details.get("tipoConsulta"),
                details.get("updatedAt"),
            ),
        )
    except Exception as e:
        print(f"[Erro ao salvar detalhes: {e}]")
    finally:
        conn.commit()
        conn.close()


async def fetch_details(client, url, type_id, brand_id, model_id, year_int, type_gas):
    """Faz a requisição HTTP e salva os detalhes no banco."""
    async with semaphore:
        try:
            response = await client.get(url, timeout=10)
            data = response.json()

            if data.get("success") and "data" in data:
                save_details(data["data"])
                print(f"✔ Detalhes salvos para: {url} (typeGas={type_gas})")

                # Aguarde 6 segundos antes da próxima requisição
                await asyncio.sleep(0.5)
            else:
                print(f"[Nenhum 'data' encontrado para: {url}]")
        except httpx.RequestError as e:
            print(f"[Erro na requisição para {url}]: {e}")
        except Exception as e:
            print(f"[Erro ao processar {url}]: {e}")




async def main():
    """Executa as requisições de forma assíncrona."""
    async with httpx.AsyncClient() as client:
        request_data = get_request_urls()
        tasks = [
            fetch_details(client, url, type_id, brand_id, model_id, year_int, type_gas)
            for url, type_id, brand_id, model_id, year_int, type_gas in request_data  
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
