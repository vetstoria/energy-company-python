package com.energycompany.generator;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class ElectricityReadingGeneratorTest {

    @Test
    void testGenerateElectricityReadings() {
        List<Map<String, Object>> generated = ElectricityReadingGenerator.generateElectricityReadings(10);
        assertEquals(10, generated.size());
        
        LocalDateTime now = LocalDateTime.now();
        for (Map<String, Object> reading : generated) {
            Long time = (Long) reading.get("time");
            Double readingValue = (Double) reading.get("reading");
            
            LocalDateTime readingTime = LocalDateTime.ofEpochSecond(time, 0, java.time.ZoneOffset.UTC);
            assertEquals(now.getYear(), readingTime.getYear());
            assertTrue(readingValue >= 0);
            assertTrue(readingValue <= 1);
        }
    }
}

