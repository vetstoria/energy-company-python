from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..service.electricity_reading_service import ElectricityReadingService

router = APIRouter(prefix="/readings", tags=["readings"])


def _service() -> ElectricityReadingService:
    # Simple dependency so we can override in tests later
    return ElectricityReadingService()


@router.post("/store", status_code=status.HTTP_201_CREATED)
async def store_readings(
    payload: dict, service: ElectricityReadingService = Depends(_service)
):
    try:
        return await service.store_reading(payload)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/read/{smart_meter_id}")
async def read_readings(
    smart_meter_id: str, service: ElectricityReadingService = Depends(_service)
):
    return await service.retrieve_readings_for(smart_meter_id)
