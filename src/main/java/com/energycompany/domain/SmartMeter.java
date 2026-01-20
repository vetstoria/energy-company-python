package com.energycompany.domain;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "smart_meters")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SmartMeter {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "smart_meter_id", nullable = false, unique = true, length = 64)
    private String smartMeterId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "price_plan_id", nullable = false)
    private PricePlan pricePlan;
}

