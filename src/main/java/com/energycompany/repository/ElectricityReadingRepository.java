package com.energycompany.repository;

import com.energycompany.domain.ElectricityReading;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ElectricityReadingRepository extends JpaRepository<ElectricityReading, Long> {
    @Query("SELECT er FROM ElectricityReading er WHERE er.smartMeter.smartMeterId = :smartMeterId ORDER BY er.time")
    List<ElectricityReading> findBySmartMeterId(@Param("smartMeterId") String smartMeterId);
}

