package com.energycompany.controller;

import com.energycompany.dto.PricePlanComparisonsDto;
import com.energycompany.service.PricePlanService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/price-plans")
@Tag(name = "price-plans", description = "Price plan comparison endpoints")
public class PricePlanComparatorController {
    private final PricePlanService pricePlanService;

    public PricePlanComparatorController(PricePlanService pricePlanService) {
        this.pricePlanService = pricePlanService;
    }

    @GetMapping("/compare-all/{smartMeterId}")
    @Operation(summary = "Compare usage cost against all price plans", 
               description = "Returns the current price plan and compares usage cost against all available price plans")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successful comparison",
                    content = @Content(mediaType = "application/json",
                    schema = @Schema(implementation = PricePlanComparisonsDto.class),
                    examples = @ExampleObject(value = "{\"pricePlanId\":\"price-plan-2\",\"pricePlanComparisons\":[{\"price-plan-2\":1.8573933524727018e-06},{\"price-plan-1\":3.7147867049454036e-06},{\"price-plan-0\":1.8573933524727016e-05}]}")))
    })
    public ResponseEntity<PricePlanComparisonsDto> compareAll(
            @Parameter(description = "Smart meter ID", example = "smart-meter-0", required = true)
            @PathVariable String smartMeterId) {
        List<Map<String, Double>> comparisons = pricePlanService.getListOfSpendAgainstEachPricePlanFor(smartMeterId, null);
        
        if (comparisons.isEmpty()) {
            return ResponseEntity.ok(new PricePlanComparisonsDto(null, List.of()));
        }

        // Extract plan name with the minimum cost
        Map<String, Double> cheapestPlan = comparisons.stream()
                .min((a, b) -> {
                    Double valueA = a.values().iterator().next();
                    Double valueB = b.values().iterator().next();
                    return valueA.compareTo(valueB);
                })
                .orElseThrow();

        String pricePlanId = cheapestPlan.keySet().iterator().next();

        return ResponseEntity.ok(new PricePlanComparisonsDto(pricePlanId, comparisons));
    }

    @GetMapping("/recommend/{smartMeterId}")
    @Operation(summary = "Get recommended price plans", 
               description = "Returns recommended price plans sorted by cost, optionally limited by the limit parameter")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "List of recommended price plans",
                    content = @Content(mediaType = "application/json",
                    examples = @ExampleObject(value = "[{\"price-plan-2\":1.8573933524727018e-06},{\"price-plan-1\":3.7147867049454036e-06}]")))
    })
    public List<Map<String, Double>> recommendPricePlans(
            @Parameter(description = "Smart meter ID", example = "smart-meter-0", required = true)
            @PathVariable String smartMeterId,
            @Parameter(description = "Optional limit on the number of plans to return", example = "2")
            @RequestParam(required = false) Integer limit) {
        return pricePlanService.getListOfSpendAgainstEachPricePlanFor(smartMeterId, limit);
    }
}

