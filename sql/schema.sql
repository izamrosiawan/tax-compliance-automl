-- DDL Schema for Tax Compliance & BPS E-Commerce Analytics Database

CREATE TABLE IF NOT EXISTS bps_regional_indicators (
    provinsi VARCHAR(50) PRIMARY KEY,
    proporsi_e_commerce_pct NUMERIC(5,2),
    infrastruktur_digital_score NUMERIC(5,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS taxpayer_digital_transactions (
    taxpayer_id SERIAL PRIMARY KEY,
    provinsi VARCHAR(50) REFERENCES bps_regional_indicators(provinsi),
    gmv_transaksi_juta NUMERIC(12,2) NOT NULL,
    volume_transaksi_tahunan INTEGER NOT NULL,
    rasio_pembayaran_digital NUMERIC(5,3) NOT NULL,
    frekuensi_pengiriman_logistik INTEGER NOT NULL,
    omset_dilaporkan_spt_juta NUMERIC(12,2) NOT NULL,
    pajak_disetor_juta NUMERIC(12,2) NOT NULL,
    target_compliance_risk INTEGER NOT NULL CHECK (target_compliance_risk IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_taxpayer_risk ON taxpayer_digital_transactions(target_compliance_risk);
CREATE INDEX IF NOT EXISTS idx_taxpayer_provinsi ON taxpayer_digital_transactions(provinsi);
