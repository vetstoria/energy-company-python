package com.energycompany.controller;

import com.energycompany.domain.ElectricityReading;
import com.energycompany.dto.ElectricReadingDto;
import com.energycompany.service.ElectricityReadingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/readings")
public class ElectricityReadingController {
    private final ElectricityReadingService electricityReadingService;

    public ElectricityReadingController(ElectricityReadingService electricityReadingService) {
        this.electricityReadingService = electricityReadingService;
    }

    @PostMapping("/store")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, Object> storeReadings(@Valid @RequestBody ElectricReadingDto payload) {
        try {
            Map<String, Object> json = new HashMap<>();
            json.put("smartMeterId", payload.getSmartMeterId());
            json.put("electricityReadings", payload.getElectricityReadings().stream()
                    .map(r -> {
                        Map<String, Object> reading = new HashMap<>();
                        reading.put("time", r.getTime());
                        reading.put("reading", r.getReading());
                        return reading;
                    })
                    .collect(Collectors.toList()));

            List<ElectricityReading> readings = electricityReadingService.storeReading(json);

            // Return format matching Python: {smartMeterId: "...", electricityReadings: [...]}
            Map<String, Object> response = new HashMap<>();
            response.put("smartMeterId", payload.getSmartMeterId());
            response.put("electricityReadings", readings.stream()
                    .map(r -> {
                        Map<String, Object> reading = new HashMap<>();
                        reading.put("time", r.getTime());
                        reading.put("reading", r.getReading());
                        return reading;
                    })
                    .collect(Collectors.toList()));
            
            return response;
        } catch (IllegalArgumentException e) {
            throw new org.springframework.web.server.ResponseStatusException(
                    HttpStatus.UNPROCESSABLE_ENTITY, e.getMessage());
        }
    }

    @GetMapping("/read/{smartMeterId}")
    public ResponseEntity<?> readReadings(@PathVariable String smartMeterId) {
        List<ElectricityReading> readings = electricityReadingService.retrieveReadingsFor(smartMeterId);
        
        if (readings.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("detail", "No readings found for this smart meter."));
        }

        // Return format matching Python: List of {time: ..., reading: ...}
        List<Map<String, Object>> readingsList = readings.stream()
                .map(r -> {
                    Map<String, Object> reading = new HashMap<>();
                    reading.put("time", r.getTime());
                    reading.put("reading", r.getReading());
                    return reading;
                })
                .collect(Collectors.toList());

        return ResponseEntity.ok(readingsList);
    }
}

