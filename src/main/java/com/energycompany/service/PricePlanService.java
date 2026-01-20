package com.energycompany.service;

import com.energycompany.domain.ElectricityReading;
import com.energycompany.domain.PricePlan;
import com.energycompany.repository.PricePlanRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class PricePlanService {
    private final ElectricityReadingService electricityReadingService;
    private final PricePlanRepository pricePlanRepository;

    public PricePlanService(
            ElectricityReadingService electricityReadingService,
            PricePlanRepository pricePlanRepository) {
        this.electricityReadingService = electricityReadingService;
        this.pricePlanRepository = pricePlanRepository;
    }

    public List<Map<String, Double>> getListOfSpendAgainstEachPricePlanFor(String smartMeterId, Integer limit) {
        List<ElectricityReading> readings = electricityReadingService.retrieveReadingsFor(smartMeterId);

        if (readings.size() < 2) {
            throw new ResponseStatusException(
                    HttpStatus.UNPROCESSABLE_ENTITY,
                    "Not enough readings to calculate usage. At least 2 readings are required."
            );
        }

        double average = calculateAverageReading(readings);
        double timeElapsed = calculateTimeElapsed(readings);

        if (timeElapsed == 0) {
            throw new ResponseStatusException(
                    HttpStatus.UNPROCESSABLE_ENTITY,
                    "Invalid readings: timestamps must not all be equal."
            );
        }

        double consumedEnergy = average / timeElapsed;

        List<PricePlan> pricePlans = pricePlanRepository.findAll();
        List<PricePlan> cheapestPlansFirst = cheapestPlansFirst(pricePlans);

        List<Map<String, Double>> listOfSpend = cheapestPlansFirst.stream()
                .map(plan -> Map.of(plan.getPlanId(), consumedEnergy * plan.getUnitRate()))
                .collect(Collectors.toList());

        // Match Python behavior: list_of_spend[:limit] - if limit is None, returns full list
        if (limit != null) {
            return listOfSpend.stream().limit(limit).collect(Collectors.toList());
        }

        return listOfSpend;
    }

    private List<PricePlan> cheapestPlansFirst(List<PricePlan> pricePlans) {
        return pricePlans.stream()
                .sorted(Comparator.comparing(PricePlan::getUnitRate))
                .collect(Collectors.toList());
    }

    private double calculateAverageReading(List<ElectricityReading> readings) {
        return readings.stream()
                .mapToDouble(ElectricityReading::getReading)
                .average()
                .orElse(0.0);
    }

    private double calculateTimeElapsed(List<ElectricityReading> readings) {
        long minTime = readings.stream()
                .mapToLong(ElectricityReading::getTime)
                .min()
                .orElse(0L);

        long maxTime = readings.stream()
                .mapToLong(ElectricityReading::getTime)
                .max()
                .orElse(0L);

        return TimeConverter.timeElapsedInHours(minTime, maxTime);
    }
}

