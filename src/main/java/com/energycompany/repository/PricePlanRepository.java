package com.energycompany.repository;

import com.energycompany.domain.PricePlan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PricePlanRepository extends JpaRepository<PricePlan, Long> {
    Optional<PricePlan> findByPlanId(String planId);
}

