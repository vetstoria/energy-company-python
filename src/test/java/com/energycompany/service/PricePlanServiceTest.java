package com.energycompany.service;

import com.energycompany.repository.ElectricityReadingRepository;
import com.energycompany.repository.PricePlanRepository;
import com.energycompany.repository.SmartMeterRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
public class PricePlanServiceTest {

    @Autowired
    private PricePlanService pricePlanService;

    @Autowired
    private ElectricityReadingService electricityReadingService;

    @Autowired
    private ElectricityReadingRepository electricityReadingRepository;

    @Autowired
    private SmartMeterRepository smartMeterRepository;

    @Autowired
    private PricePlanRepository pricePlanRepository;

    @BeforeEach
    void setUp() {
        electricityReadingRepository.deleteAll();
        smartMeterRepository.deleteAll();
        pricePlanRepository.deleteAll();
        
        // Create price plans needed for tests
        pricePlanRepository.save(new com.energycompany.domain.PricePlan("price-plan-0", "Dr Evil's Dark Energy", 10.0));
        pricePlanRepository.save(new com.energycompany.domain.PricePlan("price-plan-1", "The Green Eco", 2.0));
        pricePlanRepository.save(new com.energycompany.domain.PricePlan("price-plan-2", "Power for Everyone", 1.0));
    }

    @Test
    void testCalculateCostsAgainstAllPricePlans() {
        String meterId = "test-meter-" + UUID.randomUUID();
        long time1 = TimeConverter.isoFormatToUnixTime("2017-11-10T09:00:00");
        long time2 = TimeConverter.isoFormatToUnixTime("2017-11-10T09:30:00");
        long time3 = TimeConverter.isoFormatToUnixTime("2017-11-10T10:00:00");

        Map<String, Object> payload = Map.of(
                "smartMeterId", meterId,
                "electricityReadings", List.of(
                        Map.of("time", time1, "reading", 0.65),
                        Map.of("time", time2, "reading", 0.35),
                        Map.of("time", time3, "reading", 0.5)
                )
        );

        electricityReadingService.storeReading(payload);

        List<Map<String, Double>> spend = pricePlanService.getListOfSpendAgainstEachPricePlanFor(meterId, null);

        assertNotNull(spend);
        assertTrue(spend instanceof List);
        assertTrue(spend.stream().allMatch(item -> item instanceof Map));
        assertEquals(3, spend.size());
    }
}

