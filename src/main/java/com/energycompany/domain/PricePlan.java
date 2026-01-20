package com.energycompany.domain;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "price_plans")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PricePlan {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "plan_id", nullable = false, unique = true, length = 64)
    private String planId;

    @Column(nullable = false, length = 128)
    private String supplier;

    @Column(name = "unit_rate", nullable = false)
    private Double unitRate;

    public PricePlan(String planId, String supplier, Double unitRate) {
        this.planId = planId;
        this.supplier = supplier;
        this.unitRate = unitRate;
    }

    public Double getPrice(java.time.LocalDateTime dateTime) {
        // For now, return unit_rate (peak_time_multipliers not implemented in original)
        return unitRate;
    }
}

