package com.energycompany.dto;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ReadingsDto {
    @NotNull(message = "time is required")
    private Long time;
    
    @NotNull(message = "reading is required")
    private Double reading;
}

