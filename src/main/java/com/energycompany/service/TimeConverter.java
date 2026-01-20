package com.energycompany.service;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

public class TimeConverter {
    private static final DateTimeFormatter[] FORMATTERS = {
            DateTimeFormatter.ISO_LOCAL_DATE_TIME,
            DateTimeFormatter.ISO_DATE_TIME,
            DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss"),
            DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS")
    };

    public static long isoFormatToUnixTime(String isoFormatString) {
        for (DateTimeFormatter formatter : FORMATTERS) {
            try {
                LocalDateTime dateTime = LocalDateTime.parse(isoFormatString, formatter);
                return dateTime.toEpochSecond(ZoneOffset.UTC);
            } catch (DateTimeParseException e) {
                // Try next formatter
            }
        }
        throw new IllegalArgumentException("Unable to parse date: " + isoFormatString);
    }

    public static double timeElapsedInHours(long earliestUnixTimestamp, long latestUnixTimestamp) {
        return (latestUnixTimestamp - earliestUnixTimestamp) / 3600.0;
    }
}

