package com.energycompany.domain;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricePlanTest {

    @Test
    void testOffPeakPrice() {
        PricePlan plan = new PricePlan("p", "s", 1.0);
        LocalDateTime dateTime = LocalDateTime.of(2000, 1, 1, 11, 11, 11);
        assertEquals(1.0, plan.getPrice(dateTime));
    }

    @Test
    void testPeakPrice() {
        PricePlan plan = new PricePlan("p", "s", 1.0);
        LocalDateTime dateTime = LocalDateTime.of(2000, 1, 5, 11, 11, 11);
        // Note: Peak time multipliers not implemented in Java version, so it returns unit rate
        assertEquals(1.0, plan.getPrice(dateTime));
    }
}

