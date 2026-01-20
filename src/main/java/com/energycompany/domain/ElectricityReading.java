package com.energycompany.domain;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "electricity_readings")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ElectricityReading {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "smart_meter_id", nullable = false)
    private SmartMeter smartMeter;

    @Column(nullable = false)
    private Long time;

    @Column(nullable = false)
    private Double reading;

    public ElectricityReading(Long time, Double reading) {
        this.time = time;
        this.reading = reading;
    }
}

