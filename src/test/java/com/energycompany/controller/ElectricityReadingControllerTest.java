package com.energycompany.controller;

import com.energycompany.domain.PricePlan;
import com.energycompany.repository.ElectricityReadingRepository;
import com.energycompany.repository.PricePlanRepository;
import com.energycompany.repository.SmartMeterRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;
import java.util.stream.Stream;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
public class ElectricityReadingControllerTest {

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
        pricePlanRepository.save(new PricePlan("price-plan-0", "Test Supplier", 1.0));
    }

    private String generateMeterId() {
        return "meter-" + UUID.randomUUID();
    }

    @Test
    void testStoreReadingNewMeter() throws Exception {
        String meterId = generateMeterId();
        String payload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":1505825656,\"reading\":0.6}]}",
                meterId
        );

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated());
    }

    @Test
    void testStoreReadingExistingMeter() throws Exception {
        String meterId = generateMeterId();
        String firstPayload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":1505825838,\"reading\":0.6},{\"time\":1505825848,\"reading\":0.65}]}",
                meterId
        );
        String secondPayload = String.format(
                "{\"smartMeterId\":\"%s\",\"electricityReadings\":[{\"time\":1605825849,\"reading\":0.7}]}",
                meterId
        );

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(firstPayload))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(secondPayload))
                .andExpect(status().isCreated());

        String response = mockMvc.perform(get("/readings/read/" + meterId))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        assert response.contains("\"time\":1505825838");
        assert response.contains("\"reading\":0.6");
        assert response.contains("\"time\":1505825848");
        assert response.contains("\"reading\":0.65");
        assert response.contains("\"time\":1605825849");
        assert response.contains("\"reading\":0.7");
    }

    @Test
    void testNoReadingsReturns404() throws Exception {
        String meterId = "non-existent-meter-" + UUID.randomUUID();
        mockMvc.perform(get("/readings/read/" + meterId))
                .andExpect(status().isNotFound());
    }

    @ParameterizedTest
    @MethodSource("validationErrorPayloads")
    void testValidationErrors(String payload) throws Exception {
        mockMvc.perform(post("/readings/store")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isUnprocessableEntity());
    }

    private static Stream<Arguments> validationErrorPayloads() {
        return Stream.of(
                Arguments.of("{\"electricityReadings\":[]}"),  // missing smartMeterId
                Arguments.of("{\"smartMeterId\":\"x\"}")       // missing readings
        );
    }
}

