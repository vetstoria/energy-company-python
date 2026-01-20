package com.energycompany.service;

import com.energycompany.domain.ElectricityReading;
import com.energycompany.domain.PricePlan;
import com.energycompany.domain.SmartMeter;
import com.energycompany.repository.ElectricityReadingRepository;
import com.energycompany.repository.PricePlanRepository;
import com.energycompany.repository.SmartMeterRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class ElectricityReadingService {
    private static final String DEFAULT_PRICE_PLAN_ID = "price-plan-0";

    private final ElectricityReadingRepository electricityReadingRepository;
    private final SmartMeterRepository smartMeterRepository;
    private final PricePlanRepository pricePlanRepository;

    public ElectricityReadingService(
            ElectricityReadingRepository electricityReadingRepository,
            SmartMeterRepository smartMeterRepository,
            PricePlanRepository pricePlanRepository) {
        this.electricityReadingRepository = electricityReadingRepository;
        this.smartMeterRepository = smartMeterRepository;
        this.pricePlanRepository = pricePlanRepository;
    }

    @Transactional
    public List<ElectricityReading> storeReading(Map<String, Object> json) {
        String smartMeterId = (String) json.get("smartMeterId");
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> readingsData = (List<Map<String, Object>>) json.get("electricityReadings");

        // Ensure the smart meter exists
        SmartMeter smartMeter = ensureSmartMeterExists(smartMeterId, DEFAULT_PRICE_PLAN_ID);

        // Create and save readings
        List<ElectricityReading> readings = readingsData.stream()
                .map(readingData -> {
                    ElectricityReading reading = new ElectricityReading();
                    reading.setSmartMeter(smartMeter);
                    reading.setTime(((Number) readingData.get("time")).longValue());
                    reading.setReading(((Number) readingData.get("reading")).doubleValue());
                    return reading;
                })
                .toList();

        return electricityReadingRepository.saveAll(readings);
    }

    public List<ElectricityReading> retrieveReadingsFor(String smartMeterId) {
        return electricityReadingRepository.findBySmartMeterId(smartMeterId);
    }

    private SmartMeter ensureSmartMeterExists(String smartMeterId, String pricePlanId) {
        Optional<SmartMeter> existingMeter = smartMeterRepository.findBySmartMeterId(smartMeterId);
        if (existingMeter.isPresent()) {
            return existingMeter.get();
        }

        // Create new smart meter
        PricePlan pricePlan = pricePlanRepository.findByPlanId(pricePlanId)
                .orElseThrow(() -> new IllegalArgumentException("Unknown price plan '" + pricePlanId + "'"));

        SmartMeter smartMeter = new SmartMeter();
        smartMeter.setSmartMeterId(smartMeterId);
        smartMeter.setPricePlan(pricePlan);
        return smartMeterRepository.save(smartMeter);
    }
}

