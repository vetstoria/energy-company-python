package com.energycompany.repository;

import com.energycompany.domain.ElectricityReading;
import com.energycompany.domain.PricePlan;
import com.energycompany.domain.SmartMeter;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
@ActiveProfiles("test")
public class ElectricityReadingRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private ElectricityReadingRepository electricityReadingRepository;

    @Autowired
    private SmartMeterRepository smartMeterRepository;

    @Autowired
    private PricePlanRepository pricePlanRepository;

    private PricePlan testPricePlan;

    private PricePlan getPricePlan() {
        return testPricePlan;
    }

    private SmartMeter createSmartMeter(String meterId) {
        PricePlan plan = getPricePlan();
        SmartMeter meter = new SmartMeter();
        meter.setSmartMeterId(meterId);
        meter.setPricePlan(plan);
        return entityManager.persistAndFlush(meter);
    }

    @BeforeEach
    void setUp() {
        electricityReadingRepository.deleteAll();
        smartMeterRepository.deleteAll();
        pricePlanRepository.deleteAll();
        
        // Create price plan needed for tests
        testPricePlan = new PricePlan("price-plan-0", "Test Supplier", 1.0);
        entityManager.persistAndFlush(testPricePlan);
    }

    @Test
    void testStoreAndFetchReadings() {
        String meterIdStr = "meter-" + UUID.randomUUID();
        SmartMeter meter = createSmartMeter(meterIdStr);

        ElectricityReading reading1 = new ElectricityReading();
        reading1.setSmartMeter(meter);
        reading1.setTime(1507375234L);
        reading1.setReading(0.5);
        entityManager.persistAndFlush(reading1);

        ElectricityReading reading2 = new ElectricityReading();
        reading2.setSmartMeter(meter);
        reading2.setTime(1510053634L);
        reading2.setReading(0.75);
        entityManager.persistAndFlush(reading2);

        List<ElectricityReading> readings = electricityReadingRepository.findBySmartMeterId(meterIdStr);
        assertEquals(2, readings.size());
        assertEquals(1507375234L, readings.get(0).getTime());
        assertEquals(0.5, readings.get(0).getReading());
        assertEquals(1510053634L, readings.get(1).getTime());
        assertEquals(0.75, readings.get(1).getReading());
    }

    @Test
    void testAppendReadingsToExistingMeter() {
        String meterIdStr = "meter-" + UUID.randomUUID();
        SmartMeter meter = createSmartMeter(meterIdStr);

        ElectricityReading reading1 = new ElectricityReading();
        reading1.setSmartMeter(meter);
        reading1.setTime(1507375234L);
        reading1.setReading(0.5);
        entityManager.persistAndFlush(reading1);

        ElectricityReading reading2 = new ElectricityReading();
        reading2.setSmartMeter(meter);
        reading2.setTime(1510053634L);
        reading2.setReading(0.75);
        entityManager.persistAndFlush(reading2);

        ElectricityReading reading3 = new ElectricityReading();
        reading3.setSmartMeter(meter);
        reading3.setTime(1510572000L);
        reading3.setReading(0.32);
        entityManager.persistAndFlush(reading3);

        List<ElectricityReading> readings = electricityReadingRepository.findBySmartMeterId(meterIdStr);
        assertEquals(3, readings.size());
    }
}

