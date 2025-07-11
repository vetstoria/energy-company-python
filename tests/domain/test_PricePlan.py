from datetime import datetime

from src.domain.price_plan import PricePlan

def test_off_peak_price():
    peak = PricePlan.PeakTimeMultiplier(PricePlan.DayOfWeek.WEDNESDAY, 10)
    plan = PricePlan("p", "s", 1, [peak])
    assert plan.get_price(datetime(2000, 1, 1, 11, 11, 11)) == 1

def test_peak_price():
    peak = PricePlan.PeakTimeMultiplier(PricePlan.DayOfWeek.WEDNESDAY, 10)
    plan = PricePlan("p", "s", 1, [peak])
    assert plan.get_price(datetime(2000, 1, 5, 11, 11, 11)) == 10
