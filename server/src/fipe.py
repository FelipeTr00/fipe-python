import os
from datetime import datetime
import asyncio
import httpx
from fastapi import APIRouter, Query
from dotenv import load_dotenv
from src.db import find, add

# Carregar variáveis do .env
load_dotenv()

# Configurações
URL_BASE = "https://veiculos.fipe.org.br/api/veiculos/"
DATA_TABLE = int(os.getenv("FIPE_TABLE", "318"))
# dataTableUpdate como data fixa (no exemplo, 2025-02-01T00:00:00.000Z)
DATA_TABLE_UPDATE = datetime(2025, 2, 1)
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "false").lower() == "true"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

router = APIRouter()

def get_types(vehicle_type: int = 0):
    if vehicle_type:
        if vehicle_type == 1:
            return "carros"
        elif vehicle_type == 2:
            return "motos"
        else:
            return "caminhões"
    else:
        return {
            "success": True,
            "data": [
                {"Value": 1, "Label": "carros"},
                {"Value": 2, "Label": "motos"},
                {"Value": 3, "Label": "caminhões"},
            ]
        }

async def get_brands(vehicle_type: int):
    table_name = "brands"
    if not vehicle_type:
        ret = {"success": False, "error": "Vehicle type is required!"}
        if DEBUG:
            print(ret)
        return ret

    payload = {
        "codigoTabelaReferencia": DATA_TABLE,
        "codigoTipoVeiculo": vehicle_type
    }

    data = {}
    data_cached = None

    if CACHE_ENABLED:
        if DEBUG:
            print("Cache enabled")
        data_cached = await asyncio.to_thread(find, table_name, payload)
    else:
        if DEBUG:
            print("Cache disabled")

    if data_cached and CACHE_ENABLED and len(data_cached) > 0:
        data = data_cached
    else:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    URL_BASE + "ConsultarMarcas",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                return {"success": False, "error": str(e)}

        if isinstance(data, list) and len(data) > 0:
            for element in data:
                element.update(payload)
                # Armazena a data de atualização no formato ISO 8601 (UTC)
                element["updatedAt"] = datetime.utcnow().isoformat() + "Z"
            if CACHE_ENABLED:
                await asyncio.to_thread(add, table_name, data)

    ret = {
        "success": True,
        "updatedAt": DATA_TABLE_UPDATE.isoformat() + "Z",
        "type": vehicle_type,
        "type_label": get_types(vehicle_type),
        "data": data
    }
    return ret

async def get_models(vehicle_type: int, brand_code: int):
    table_name = "models"
    if not vehicle_type:
        ret = {"success": False, "error": "Vehicle type is required!"}
        if DEBUG:
            print(ret)
        return ret
    if not brand_code:
        ret = {"success": False, "error": "Brand code is required!"}
        if DEBUG:
            print(ret)
        return ret

    payload = {
        "codigoTabelaReferencia": DATA_TABLE,
        "codigoTipoVeiculo": vehicle_type,
        "codigoMarca": brand_code
    }

    data = {}
    data_cached = None

    if CACHE_ENABLED:
        if DEBUG:
            print("Cache enabled")
        data_cached = await asyncio.to_thread(find, table_name, payload)
    else:
        if DEBUG:
            print("Cache disabled")

    if data_cached and CACHE_ENABLED and len(data_cached) > 0:
        if DEBUG:
            print("Data returned from local database.")
        data["Modelos"] = data_cached
    else:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    URL_BASE + "ConsultarModelos",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                return {"success": False, "error": str(e)}

        if data.get("Modelos") and len(data["Modelos"]) > 0:
            for element in data["Modelos"]:
                element.update(payload)
                element["updatedAt"] = datetime.utcnow().isoformat() + "Z"
            if CACHE_ENABLED:
                await asyncio.to_thread(add, table_name, data["Modelos"])

    ret = {
        "success": True,
        "updatedAt": DATA_TABLE_UPDATE.isoformat() + "Z",
        "type": vehicle_type,
        "type_label": get_types(vehicle_type),
        "brand": brand_code,
        "data": data.get("Modelos", [])
    }
    return ret

async def get_years(vehicle_type: int, brand_code: int, model_code: int):
    table_name = "years"
    if not vehicle_type:
        ret = {"success": False, "error": "Vehicle type is required!"}
        if DEBUG:
            print(ret)
        return ret
    if not brand_code:
        ret = {"success": False, "error": "Brand code is required!"}
        if DEBUG:
            print(ret)
        return ret
    if not model_code:
        ret = {"success": False, "error": "Model code is required!"}
        if DEBUG:
            print(ret)
        return ret

    payload = {
        "codigoTabelaReferencia": DATA_TABLE,
        "codigoTipoVeiculo": vehicle_type,
        "codigoMarca": brand_code,
        "codigoModelo": model_code
    }

    data = {}
    data_cached = None

    if CACHE_ENABLED:
        if DEBUG:
            print("Cache enabled")
        data_cached = await asyncio.to_thread(find, table_name, payload)
    else:
        if DEBUG:
            print("Cache disabled")

    if data_cached and CACHE_ENABLED and len(data_cached) > 0:
        data = data_cached
    else:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    URL_BASE + "ConsultarAnoModelo",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                return {"success": False, "error": str(e)}

        if isinstance(data, list) and len(data) > 0:
            for element in data:
                element.update(payload)
                element["updatedAt"] = datetime.utcnow().isoformat() + "Z"
            if CACHE_ENABLED:
                await asyncio.to_thread(add, table_name, data)

    ret = {
        "success": True,
        "updatedAt": DATA_TABLE_UPDATE.isoformat() + "Z",
        "type": vehicle_type,
        "type_label": get_types(vehicle_type),
        "brand": brand_code,
        "model": model_code,
        "data": data
    }
    return ret

async def get_details(vehicle_type: int, brand_code: int, model_code: int, year_code: int, type_gas: int = 1, type_search: str = "tradicional"):
    table_name = "details"
    if not vehicle_type:
        ret = {"success": False, "error": "Vehicle type is required!"}
        if DEBUG:
            print(ret)
        return ret
    if not brand_code:
        ret = {"success": False, "error": "Brand code is required!"}
        if DEBUG:
            print(ret)
        return ret
    if not model_code:
        ret = {"success": False, "error": "Model code is required!"}
        if DEBUG:
            print(ret)
        return ret
    if not year_code:
        ret = {"success": False, "error": "Year code is required!"}
        if DEBUG:
            print(ret)
        return ret

    payload = {
        "codigoTabelaReferencia": DATA_TABLE,
        "codigoTipoVeiculo": vehicle_type,
        "codigoMarca": brand_code,
        "codigoModelo": model_code,
        "anoModelo": year_code,
        "codigoTipoCombustivel": type_gas or 1,
        "tipoConsulta": type_search or "tradicional"
    }

    data = {}
    data_cached = None

    if CACHE_ENABLED:
        if DEBUG:
            print("Cache enabled")
        data_cached = await asyncio.to_thread(find, table_name, payload)
    else:
        if DEBUG:
            print("Cache disabled")

    if data_cached and CACHE_ENABLED and len(data_cached) > 0:
        data = data_cached
    else:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    URL_BASE + "ConsultarValorComTodosParametros",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                return {"success": False, "error": str(e)}

        if data:
            data.update(payload)
            data["updatedAt"] = datetime.utcnow().isoformat() + "Z"
            if CACHE_ENABLED:
                await asyncio.to_thread(add, table_name, [data])

    ret = {
        "success": True,
        "updatedAt": DATA_TABLE_UPDATE.isoformat() + "Z",
        "type": vehicle_type,
        "type_label": get_types(vehicle_type),
        "brand": brand_code,
        "model": model_code,
        "year": year_code,
        "data": data
    }
    return ret

# -----------------------------
# API Endpoints (FastAPI routes)
# -----------------------------

@router.get("/v1/types")
async def types_endpoint(vehicleType: int = 0):
    return get_types(vehicleType)

@router.get("/v1/brands/{type}")
async def brands_endpoint(type: int):
    return await get_brands(type)

@router.get("/v1/models/{type}/{brand}")
async def models_endpoint(type: int, brand: int):
    return await get_models(type, brand)

@router.get("/v1/years/{type}/{brand}/{model}")
async def years_endpoint(type: int, brand: int, model: int):
    return await get_years(type, brand, model)

@router.get("/v1/details/{type}/{brand}/{model}/{year}")
async def details_endpoint(
    type: int, 
    brand: int, 
    model: int, 
    year: int, 
    typeGas: int = Query(1), 
    typeSearch: str = Query("tradicional")
):
    return await get_details(type, brand, model, year, typeGas, typeSearch)

# Opcional: exportar funções para testes
__all__ = [
    "get_types", "get_brands", "get_models", "get_years", "get_details",
    "types_endpoint", "brands_endpoint", "models_endpoint", "years_endpoint", "details_endpoint"
]
