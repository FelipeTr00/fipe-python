import asyncio
import httpx
import sqlite3
import os
import json

with open("server/config.json", "r") as file:
    config = json.load(file)

VERSION = config.get("VERSION", "v1")
BASE_URL = f"http://127.0.0.1:8000/{VERSION}"
DB_URI = config.get("DB_URI", "./server/database/db.sqlite")

semaphore = asyncio.Semaphore(5)

def get_years():
    """
    Lê os registros da tabela 'years' e trata a coluna 'value' para
    extrair o ano como inteiro. Se houver '-' no valor, utiliza a parte antes do hífen.
    """
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            value,          -- coluna que pode vir como "2008-3" ou "2008"
            codigoMarca,
            codigoModelo,
            codigoTipoVeiculo
        FROM years
    """)
    rows = cursor.fetchall()
    conn.close()

    processed_rows = []
    for value, codigoMarca, codigoModelo, codigoTipoVeiculo in rows:
        # Converte o valor para string e extrai a parte antes do "-" se existir
        value_str = str(value)
        if '-' in value_str:
            year_part = value_str.split('-')[0]
        else:
            year_part = value_str

        try:
            year_int = int(year_part)
        except ValueError:
            print(f"Valor inválido para o ano: {value_str}")
            continue

        processed_rows.append((year_int, codigoMarca, codigoModelo, codigoTipoVeiculo))

    return processed_rows

def save_details(details):
    conn = sqlite3.connect(DB_URI)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO details (
                Valor,
                Marca,
                Modelo,
                Combustivel,
                MesReferencia,
                Autenticacao,
                TipoVeiculo,
                SiglaCombustivel,
                DataConsulta,
                codigoTabelaReferencia,
                codigoTipoVeiculo,
                codigoMarca,
                codigoModelo,
                anoModelo,
                codigoTipoCombustivel,
                tipoConsulta,
                updatedAt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo, anoModelo) 
            DO NOTHING;
        """, (
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
            details.get("anoModelo"),               # <--- anoModelo
            details.get("codigoTipoCombustivel"),
            details.get("tipoConsulta"),            # <--- tipoConsulta (lowercase)
            details.get("updatedAt")
        ))
    except Exception as e:
        print(f"[Erro ao salvar detalhes: {e}]")
    finally:
        conn.commit()
        conn.close()

async def fetch_details(client, year_int, brand_id, model_id, type_id):
    async with semaphore:
        url = f"{BASE_URL}/details/{type_id}/{brand_id}/{model_id}/{year_int}"
        try:
            response = await client.get(url, timeout=10)
            data = response.json()

            if data.get("success") and "data" in data:
                # "data" contém o objeto com as chaves necessárias
                save_details(data["data"])
                print(
                    f"✔ Detalhes salvos para: "
                    f"Year={year_int}, Modelo={model_id}, Marca={brand_id}, Tipo={type_id}"
                )
                await asyncio.sleep(0.1)
            else:
                print(
                    f"[Nenhum 'data' encontrado em detalhes para "
                    f"Year={year_int}, Modelo={model_id}, Marca={brand_id}, Tipo={type_id}]"
                )
        except httpx.RequestError as e:
            print(
                f"[Erro de requisição ao buscar detalhes para "
                f"Year={year_int}, Modelo={model_id}, Marca={brand_id}, Tipo={type_id}]: {e}"
            )
        except Exception as e:
            print(
                f"[Erro ao processar detalhes para "
                f"Year={year_int}, Modelo={model_id}, Marca={brand_id}, Tipo={type_id}]: {e}"
            )

async def main():
    async with httpx.AsyncClient() as client:
        years_records = get_years()
        tasks = []
        for (year_int, brand_id, model_id, type_id) in years_records:
            tasks.append(fetch_details(client, year_int, brand_id, model_id, type_id))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
