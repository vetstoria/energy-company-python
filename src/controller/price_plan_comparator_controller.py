from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends

from ..service.price_plan_service import PricePlanService

router = APIRouter(prefix="/price-plans", tags=["price-plans"])


def _service() -> PricePlanService:
    return PricePlanService()


@router.get("/compare-all/{smart_meter_id}")
async def compare_all(smart_meter_id: str, service: PricePlanService = Depends(_service)):
    comparisons = await service.get_list_of_spend_against_each_price_plan_for(smart_meter_id)
    if not comparisons:
        return {"pricePlanId": None, "pricePlanComparisons": []}

    # Extract plan name with the minimum cost
    cheapest_plan = min(comparisons, key=lambda item: list(item.values())[0])
    price_plan_id = list(cheapest_plan.keys())[0]

    return {
        "pricePlanId": price_plan_id,
        "pricePlanComparisons": comparisons,
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
