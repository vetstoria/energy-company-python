package com.energycompany.dto;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Price plan comparison response")
public class PricePlanComparisonsDto {
    @Schema(description = "The price plan ID with the minimum cost", example = "price-plan-2")
    private String pricePlanId;
    
    @Schema(description = "List of price plan comparisons, each containing a price plan ID and its cost. Each item is a map with one key-value pair.",
            example = "[{\"price-plan-2\": 1.8573933524727018e-06}, {\"price-plan-1\": 3.7147867049454036e-06}, {\"price-plan-0\": 1.8573933524727016e-05}]",
            type = "array",
            implementation = Map.class)
    private List<Map<String, Double>> pricePlanComparisons;
}

