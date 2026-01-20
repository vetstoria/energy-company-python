package com.energycompany.config;

import com.energycompany.domain.ElectricityReading;
import com.energycompany.domain.PricePlan;
import com.energycompany.domain.SmartMeter;
import com.energycompany.generator.ElectricityReadingGenerator;
import com.energycompany.repository.ElectricityReadingRepository;
import com.energycompany.repository.PricePlanRepository;
import com.energycompany.repository.SmartMeterRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Component
@org.springframework.boot.autoconfigure.condition.ConditionalOnProperty(
        name = "app.data.initialize",
        havingValue = "true",
        matchIfMissing = true
)
public class DataInitializer implements CommandLineRunner {
    private static final String DR_EVILS_DARK_ENERGY = "Dr Evil's Dark Energy";
    private static final String THE_GREEN_ECO = "The Green Eco";
    private static final String POWER_FOR_EVERYONE = "Power for Everyone";

    private static final String MOST_EVIL = "price-plan-0";
    private static final String RENEWABLES = "price-plan-1";
    private static final String STANDARD = "price-plan-2";

    private static final int NUM_METERS = 10;
    private static final int NUM_READINGS_PER_METER = 5;

    private final PricePlanRepository pricePlanRepository;
    private final SmartMeterRepository smartMeterRepository;
    private final ElectricityReadingRepository electricityReadingRepository;

    public DataInitializer(
            PricePlanRepository pricePlanRepository,
            SmartMeterRepository smartMeterRepository,
            ElectricityReadingRepository electricityReadingRepository) {
        this.pricePlanRepository = pricePlanRepository;
        this.smartMeterRepository = smartMeterRepository;
        this.electricityReadingRepository = electricityReadingRepository;
    }

    @Override
    public void run(String... args) {
        populatePricePlans();
        populateSmartMeters();
        populateRandomReadings();
    }

    private void populatePricePlans() {
        List<PricePlan> plans = List.of(
                new PricePlan(MOST_EVIL, DR_EVILS_DARK_ENERGY, 10.0),
                new PricePlan(RENEWABLES, THE_GREEN_ECO, 2.0),
                new PricePlan(STANDARD, POWER_FOR_EVERYONE, 1.0)
        );

        for (PricePlan plan : plans) {
            Optional<PricePlan> existing = pricePlanRepository.findByPlanId(plan.getPlanId());
            if (existing.isEmpty()) {
                pricePlanRepository.save(plan);
            }
        }
    }

    private void populateSmartMeters() {
        String[] planNames = {MOST_EVIL, RENEWABLES, STANDARD};

        for (int i = 0; i < NUM_METERS; i++) {
            String smartId = "smart-meter-" + i;
            String planName = planNames[i % 3];

            Optional<SmartMeter> existing = smartMeterRepository.findBySmartMeterId(smartId);
            if (existing.isEmpty()) {
                PricePlan pricePlan = pricePlanRepository.findByPlanId(planName)
                        .orElseThrow(() -> new RuntimeException("Price plan not found: " + planName));

                SmartMeter smartMeter = new SmartMeter();
                smartMeter.setSmartMeterId(smartId);
                smartMeter.setPricePlan(pricePlan);
                smartMeterRepository.save(smartMeter);
            }
        }
    }

    private void populateRandomReadings() {
        for (int i = 0; i < NUM_METERS; i++) {
            String smartId = "smart-meter-" + i;
            SmartMeter smartMeter = smartMeterRepository.findBySmartMeterId(smartId)
                    .orElseThrow(() -> new RuntimeException("Smart meter not found: " + smartId));

            // Only populate if no readings exist
            List<ElectricityReading> existingReadings = electricityReadingRepository.findBySmartMeterId(smartId);
            if (!existingReadings.isEmpty()) {
                continue;
            }

            List<Map<String, Object>> readingsData = ElectricityReadingGenerator.generateElectricityReadings(NUM_READINGS_PER_METER);

            List<ElectricityReading> readings = readingsData.stream()
                    .map(readingData -> {
                        ElectricityReading reading = new ElectricityReading();
                        reading.setSmartMeter(smartMeter);
                        reading.setTime(((Number) readingData.get("time")).longValue());
                        reading.setReading(((Number) readingData.get("reading")).doubleValue());
                        return reading;
                    })
                    .toList();

            electricityReadingRepository.saveAll(readings);
        }
    }
}

