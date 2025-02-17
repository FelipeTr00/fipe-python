from fastapi import APIRouter
from . import fipe as fipe_controller

VERSION = "v1"

router = APIRouter()

@router.get("/{VERSION}/types")
async def types_endpoint(vehicleType: int = 0):
    return fipe_controller.get_types(vehicleType)

@router.get("/{VERSION}/brands/{type}")
async def brands_endpoint(type: int):
    return await fipe_controller.get_brands(type)

@router.get("/{VERSION}/models/{type}/{brand}")
async def models_endpoint(type: int, brand: int):
    return await fipe_controller.get_models(type, brand)

@router.get("/{VERSION}/years/{type}/{brand}/{model}")
async def years_endpoint(type: int, brand: int, model: int):
    return await fipe_controller.get_years(type, brand, model)

@router.get("/{VERSION}/details/{type}/{brand}/{model}/{year}")
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
    return {"title": "FIPE-Python", "author": "Felipe Alves de Morais", "version": "v.1 - 20250216"}
