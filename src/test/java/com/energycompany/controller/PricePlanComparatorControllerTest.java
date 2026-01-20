package com.energycompany.controller;

import com.energycompany.domain.PricePlan;
import com.energycompany.repository.ElectricityReadingRepository;
import com.energycompany.repository.PricePlanRepository;
import com.energycompany.repository.SmartMeterRepository;
import com.energycompany.service.TimeConverter;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
public class PricePlanComparatorControllerTest {

    @Autowired
    private MockMvc mockMvc;

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
        pricePlanRepository.save(new PricePlan("price-plan-0", "Dr Evil's Dark Energy", 10.0));
        pricePlanRepository.save(new PricePlan("price-plan-1", "The Green Eco", 2.0));
        pricePlanRepository.save(new PricePlan("price-plan-2", "Power for Everyone", 1.0));
    }

    private String generateMeterId() {
        return "test-meter-" + UUID.randomUUID();
    }

    @Test
    void testCompareAllPricePlans() throws Exception {
        String meterId = generateMeterId();
        long time1 = TimeConverter.isoFormatToUnixTime("2020-01-05T10:00:00");
        long time2 = TimeConverter.isoFormatToUnixTime("2020-01-05T11:00:00");
        String payload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":%d,\"reading\":10.0},{\"time\":%d,\"reading\":20.0}]}",
                meterId, time1, time2
        );

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated());

        String response = mockMvc.perform(get("/price-plans/compare-all/" + meterId))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        assert response.contains("\"pricePlanId\"");
        assert response.contains("\"pricePlanComparisons\"");
        assert response.contains("price-plan-0") || response.contains("price-plan-1") || response.contains("price-plan-2");
    }

    @Test
    void testRecommendCheapestPlans() throws Exception {
        String meterId = generateMeterId();
        long time1 = TimeConverter.isoFormatToUnixTime("2020-01-05T10:30:00");
        long time2 = TimeConverter.isoFormatToUnixTime("2020-01-05T11:00:00");
        String payload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":%d,\"reading\":35.0},{\"time\":%d,\"reading\":5.0}]}",
                meterId, time1, time2
        );

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated());

        String response = mockMvc.perform(get("/price-plans/recommend/" + meterId))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        assert response.contains("price-plan-2");
        assert response.contains("price-plan-1");
        assert response.contains("price-plan-0");
    }

    @Test
    void testCompareAllWithInsufficientReadings() throws Exception {
        String meterId = generateMeterId();
        long time = TimeConverter.isoFormatToUnixTime("2024-01-01T10:00:00");
        String payload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":%d,\"reading\":10.0}]}",
                meterId, time
        );

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated());

        mockMvc.perform(get("/price-plans/compare-all/" + meterId))
                .andExpect(status().isUnprocessableEntity());
    }

    @Test
    void testRecommendWithInsufficientReadings() throws Exception {
        String meterId = generateMeterId();
        long time = TimeConverter.isoFormatToUnixTime("2024-01-01T10:00:00");
        String payload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":%d,\"reading\":15.0}]}",
                meterId, time
        );

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated());

        mockMvc.perform(get("/price-plans/recommend/" + meterId))
                .andExpect(status().isUnprocessableEntity());
    }
}

