package com.energycompany.service;

import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class AccountService {
    private static final Map<String, String> planIdsByMeter = new HashMap<>();

    static {
        planIdsByMeter.put("smart-meter-0", "price-plan-0");
        planIdsByMeter.put("smart-meter-1", "price-plan-1");
        planIdsByMeter.put("smart-meter-2", "price-plan-0");
        planIdsByMeter.put("smart-meter-3", "price-plan-2");
        planIdsByMeter.put("smart-meter-4", "price-plan-1");
    }

    public String getPricePlan(String smartMeterId) {
        return planIdsByMeter.get(smartMeterId);
    }
}

