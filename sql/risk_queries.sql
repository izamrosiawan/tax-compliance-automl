-- Analytical SQL Queries for Digital Tax Compliance Risk Analytics

-- 1. Underreporting Variance & Risk Ratio per Province
SELECT 
    t.provinsi,
    COUNT(t.taxpayer_id) AS total_merchants,
    ROUND(AVG(t.gmv_transaksi_juta), 2) AS avg_gmv_juta,
    ROUND(AVG(t.omset_dilaporkan_spt_juta), 2) AS avg_reported_spt_juta,
    ROUND(AVG((t.gmv_transaksi_juta - t.omset_dilaporkan_spt_juta) / (t.gmv_transaksi_juta + 0.0001) * 100), 2) AS avg_underreporting_pct,
    ROUND(SUM(CASE WHEN t.target_compliance_risk = 1 THEN 1 ELSE 0 END)::NUMERIC / COUNT(t.taxpayer_id) * 100, 2) AS high_risk_incidence_pct
FROM taxpayer_digital_transactions t
GROUP BY t.provinsi
ORDER BY high_risk_incidence_pct DESC;

-- 2. Audit Decile Segmentation Using Window Functions (NTILE)
WITH scored_merchants AS (
    SELECT 
        taxpayer_id,
        provinsi,
        gmv_transaksi_juta,
        omset_dilaporkan_spt_juta,
        (gmv_transaksi_juta - omset_dilaporkan_spt_juta) AS underreported_gap_juta,
        target_compliance_risk,
        NTILE(10) OVER (ORDER BY (gmv_transaksi_juta - omset_dilaporkan_spt_juta) DESC) AS risk_decile
    FROM taxpayer_digital_transactions
)
SELECT 
    risk_decile,
    COUNT(taxpayer_id) AS total_taxpayers,
    SUM(target_compliance_risk) AS actual_non_compliant_count,
    ROUND(SUM(target_compliance_risk)::NUMERIC / COUNT(taxpayer_id) * 100, 2) AS decile_hit_rate_pct,
    ROUND(SUM(underreported_gap_juta), 2) AS total_underreported_gap_juta
FROM scored_merchants
GROUP BY risk_decile
ORDER BY risk_decile ASC;
