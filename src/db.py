# -*- coding: utf-8 -*-

instant_reads = """CREATE TABLE instant_reads (
    dt INT NOT NULL PRIMARY KEY,
    kWh_1 DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    kWh_2 DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    kWh_3 DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    kWh_total DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    kVARh_total DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    V_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    V_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    V_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    I_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    I_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    I_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    P_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    P_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    P_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    P DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    PF_1 DECIMAL(3,0) NOT NULL DEFAULT 200,
    PF_2 DECIMAL(3,0) NOT NULL DEFAULT 200,
    PF_3 DECIMAL(3,0) NOT NULL DEFAULT 200,
    VAR_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    VAR_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    VAR_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    VAR DECIMAL(8,2) NOT NULL DEFAULT 0.0
)"""

by_hour = """CREATE TABLE by_hour (
    dt_slot CHARACTER(11) STRING NOT NULL PRIMARY KEY,
    kWh_1 DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    kWh_2 DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    kWh_3 DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    kWh_totalDECIMAL(5,2) NOT NULL DEFAULT 0.0,
    kVARh_total DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    MIN_V_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_V_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_V_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_V_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_V_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_V_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_V_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_V_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_V_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_I_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_I_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_I_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_I_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_I_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_I_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_I_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_I_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_I_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_P_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_P_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_P_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_P_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_P_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_P_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_P_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_P_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_P_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_P DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_P DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_P DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_VAR_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_VAR_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_VAR_1 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_VAR_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_VAR_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_VAR_2 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_VAR_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_VAR_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_VAR_3 DECIMAL(8,2) NOT NULL DEFAULT 0.0,
    MIN_VAR DECIMAL(8,2) NOT NULL DEFAULT 0.0, MAX_VAR DECIMAL(8,2) NOT NULL DEFAULT 0.0, AVG_VAR DECIMAL(8,2) NOT NULL DEFAULT 0.0
)
"""

instant_reads_insert = """INSERT INTO instant_reads (
    dt,
    kWh_1, kWh_2, kWh_3, kWh_total, kVARh_total,
    V_1, V_2, V_3,
    I_1, I_2, I_3,
    P_1, P_2, P_3, P,
    PF_1, PF_2, PF_3,
    VAR_1, VAR_2, VAR_3, VAR
) VALUES (
    ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?,
    ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?, ?,
    ?, ?, ?, ?
)"""

instant_reads_by_hour = """SELECT
    strftime('%Y%m%d-%H', dt) AS dt_slot,
    MAX(kWh_1) - MIN(kWh_1) AS kWh_1,
    MAX(kWh_2) - MIN(kWh_2) AS kWh_2,
    MAX(kWh_3) - MIN(kWh_3) AS kWh_3,
    MAX(kWh_total) - MIN(kWh_total) AS kWh_total,
    MAX(kVARh_total) - MIN(kVARh_total) AS kVARh_total,
    MIN(V_1) AS MIN_V_1, MAX(V_1) AS MAX_V_1, AVG(V_1) AS AVG_V_1,
    MIN(V_2) AS MIN_V_2, MAX(V_2) AS MAX_V_2, AVG(V_2) AS AVG_V_2,
    MIN(V_3) AS MIN_V_3, MAX(V_3) AS MAX_V_3, AVG(V_3) AS AVG_V_3,
    MIN(I_1) AS MIN_I_1, MAX(I_1) AS MAX_I_1, AVG(I_1) AS AVG_I_1,
    MIN(I_2) AS MIN_I_2, MAX(I_2) AS MAX_I_2, AVG(I_2) AS AVG_I_2,
    MIN(I_3) AS MIN_I_3, MAX(I_3) AS MAX_I_3, AVG(I_3) AS AVG_I_3,
    MIN(P_1) AS MIN_P_1, MAX(P_1) AS MAX_P_1, AVG(P_1) AS AVG_P_1,
    MIN(P_2) AS MIN_P_2, MAX(P_2) AS MAX_P_2, AVG(P_2) AS AVG_P_2,
    MIN(P_3) AS MIN_P_3, MAX(P_3) AS MAX_P_3, AVG(P_3) AS AVG_P_3,
    MIN(P) AS MIN_P, MAX(P) AS MAX_P, AVG(P) AS AVG_P,
    MIN(VAR_1) AS MIN_VAR_1, MAX(VAR_1) AS MAX_VAR_1, AVG(VAR_1) AS AVG_VAR_1,
    MIN(VAR_2) AS MIN_VAR_2, MAX(VAR_2) AS MAX_VAR_2, AVG(VAR_2) AS AVG_VAR_2,
    MIN(VAR_3) AS MIN_VAR_3, MAX(VAR_3) AS MAX_VAR_3, AVG(VAR_3) AS AVG_VAR_3,
    MIN(VAR) AS MIN_VAR, MAX(VAR) AS MAX_VAR, AVG(VAR) AS AVG_VAR
FROM instant_reads
WHERE dt < ?
GROUP BY dt_slot"""
