from fastapi import APIRouter
from . import fipe as fipe_controller

VERSION = "v1"

router = APIRouter()

@router.get("/v1/types")
async def types_endpoint(vehicleType: int = 0):
    return fipe_controller.get_types(vehicleType)

@router.get("/v1/brands/{type}")
async def brands_endpoint(type: int):
    return await fipe_controller.get_brands(type)

@router.get("/v1/models/{type}/{brand}")
async def models_endpoint(type: int, brand: int):
    return await fipe_controller.get_models(type, brand)

@router.get("/v1/years/{type}/{brand}/{model}")
async def years_endpoint(type: int, brand: int, model: int):
    return await fipe_controller.get_years(type, brand, model)

@router.get("/v1/details/{type}/{brand}/{model}/{year}")
async def details_endpoint(
    type: int, 
    brand: int, 
    model: int, 
    year: int, 
    typeGas: int = 1, 
    typeSearch: str = "tradicional"
):
    return await fipe_controller.get_details(type, brand, model, year, typeGas, typeSearch)

# Rota adicional
@router.get(f"/{VERSION}")
def get_version():
    return {"version": "1.0", "fipe_update": "2023-03"}
