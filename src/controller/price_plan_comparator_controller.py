from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends

from ..service.price_plan_service import PricePlanService

router = APIRouter(prefix="/price-plans", tags=["price-plans"])


def _service() -> PricePlanService:
    return PricePlanService()


@router.get("/compare-all/{smart_meter_id}")
async def compare_all(smart_meter_id: str, service: PricePlanService = Depends(_service)):
    return {
        "pricePlanId": None,
        "pricePlanComparisons": await service.get_list_of_spend_against_each_price_plan_for(
            smart_meter_id
        ),
    }


@router.get("/recommend/{smart_meter_id}")
async def recommend_price_plans(
    smart_meter_id: str,
    limit: Optional[int] = None,
    service: PricePlanService = Depends(_service),
):
    return await service.get_list_of_spend_against_each_price_plan_for(
        smart_meter_id, limit
    )
