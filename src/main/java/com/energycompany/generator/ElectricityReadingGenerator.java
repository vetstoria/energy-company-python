package com.energycompany.generator;

import com.energycompany.service.TimeConverter;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class ElectricityReadingGenerator {
    private static final Random random = new Random();

    public static List<Map<String, Object>> generateElectricityReadings(int num) {
        List<Map<String, Object>> readings = new ArrayList<>();
        LocalDateTime now = LocalDateTime.now();

        for (int i = 0; i < num; i++) {
            LocalDateTime randomTime = now.minusSeconds(i * 60);
            String isoTime = randomTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            long unixTime = TimeConverter.isoFormatToUnixTime(isoTime);
            double randomReading = Math.floor(random.nextDouble() * 1000) / 1000.0;

            readings.add(Map.of(
                    "time", unixTime,
                    "reading", randomReading
            ));
        }

        return readings;
    }
}

