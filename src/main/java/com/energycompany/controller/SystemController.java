package com.energycompany.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class SystemController {
    @GetMapping("/")
    public Map<String, String> root() {
        return Map.of("message", "Welcome to the EnergyCompany ");
    }

    @GetMapping("/health")
    public boolean health() {
        return true;
    }
}

