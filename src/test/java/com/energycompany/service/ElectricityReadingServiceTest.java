package com.energycompany.service;

import com.energycompany.domain.ElectricityReading;
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
public class ElectricityReadingServiceTest {

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
        pricePlanRepository.save(new com.energycompany.domain.PricePlan("price-plan-0", "Test Supplier", 1.0));
    }

    @Test
    void testCallsRepositoryToStoreReadings() {
        String meterId = "meter-" + UUID.randomUUID();
        long time1 = TimeConverter.isoFormatToUnixTime("2015-03-02T08:55:00");
        long time2 = TimeConverter.isoFormatToUnixTime("2015-09-02T08:55:00");

        Map<String, Object> payload = Map.of(
                "smartMeterId", meterId,
                "electricityReadings", List.of(
                        Map.of("time", time1, "reading", 0.812),
                        Map.of("time", time2, "reading", 0.23)
                )
        );

        List<ElectricityReading> result = electricityReadingService.storeReading(payload);

        assertNotNull(result);
        assertEquals(2, result.size());
        assertEquals(time1, result.get(0).getTime());
        assertEquals(0.812, result.get(0).getReading());
        assertEquals(time2, result.get(1).getTime());
        assertEquals(0.23, result.get(1).getReading());
    }
}

