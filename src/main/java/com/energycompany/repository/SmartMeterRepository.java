package com.energycompany.repository;

import com.energycompany.domain.SmartMeter;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SmartMeterRepository extends JpaRepository<SmartMeter, Long> {
    Optional<SmartMeter> findBySmartMeterId(String smartMeterId);
}

