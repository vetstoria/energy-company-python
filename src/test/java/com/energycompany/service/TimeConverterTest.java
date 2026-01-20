package com.energycompany.service;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class TimeConverterTest {

    @Test
    void testIsoToUnix() {
        assertEquals(0, TimeConverter.isoFormatToUnixTime("1970-01-01T00:00:00"));
        assertEquals(3601, TimeConverter.isoFormatToUnixTime("1970-01-01T01:00:01"));
        assertEquals(1583017961, TimeConverter.isoFormatToUnixTime("2020-02-29T23:12:41"));
    }

    @Test
    void testElapsedHours() {
        long earlier = TimeConverter.isoFormatToUnixTime("2018-05-24T11:30:00");
        long later = TimeConverter.isoFormatToUnixTime("2018-05-24T12:00:00");
        assertEquals(0.5, TimeConverter.timeElapsedInHours(earlier, later), 0.001);
    }
}

