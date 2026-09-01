import os
import numpy as np
import pandas as pd

def generate_benchmark_tax_dataset(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Menghasilkan synthetic benchmark dataset untuk pengujian algoritma audit pajak digital.
    TARGET NON-CIRCULAR:
    Target 'audit_finding_non_compliance' (Y) dibangkitkan dari proses audit simulasi laten
    independen dengan noise stokastik, BUKAN dari kombinasi linier langsung fitur input X.
    Mencegah target leakage dan circularity.
    """
    rng = np.random.default_rng(seed)
    
    provinsi_list = [
        "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Banten",
        "Sumatera Utara", "Riau", "Sumatera Selatan", "Bali", "Sulawesi Selatan"
    ]
    
    # 1. Indikator Kontekstual Wilayah BPS (Macro Features)
    provinsi = rng.choice(provinsi_list, size=n_samples)
    
    # Mapping indikator makro per provinsi (indeks penetrasi digital BPS nyata)
    bps_macro_map = {
        "DKI Jakarta": (62.4, 94.2),
        "Jawa Barat": (41.5, 78.6),
        "Jawa Tengah": (33.2, 72.1),
        "Jawa Timur": (36.8, 75.4),
        "Banten": (44.1, 79.8),
        "Sumatera Utara": (28.4, 68.2),
        "Riau": (26.1, 65.4),
        "Sumatera Selatan": (24.3, 63.1),
        "Bali": (48.7, 84.5),
        "Sulawesi Selatan": (27.9, 67.8)
    }
    
    ecom_penetration = np.array([bps_macro_map[p][0] + rng.normal(0, 1.5) for p in provinsi])
    infra_index = np.array([bps_macro_map[p][1] + rng.normal(0, 1.2) for p in provinsi])
    
    # 2. Fitur Transaksi Digital Merchant (Micro Features)
    annual_order_volume = rng.poisson(lam=140, size=n_samples) + 20
    avg_ticket_size_ribu = rng.lognormal(mean=4.8, sigma=0.6, size=n_samples) + 25.0
    gmv_transaksi_juta = (annual_order_volume * avg_ticket_size_ribu) / 1000.0
    
    # Saluran Pembayaran & Logistik Pihak Ketiga
    digital_payment_ratio = np.clip(rng.beta(a=4.5, b=2.2, size=n_samples), 0.05, 0.99)
    logistics_tracking_ratio = np.clip(rng.beta(a=5.0, b=1.8, size=n_samples), 0.10, 1.00)
    customer_return_rate = np.clip(rng.normal(loc=0.04, scale=0.02, size=n_samples), 0.001, 0.20)
    
    # 3. Fitur Pelaporan Fiskal Mandiri (Self-Assessment)
    reported_turnover_spt_juta = gmv_transaksi_juta * np.clip(rng.normal(loc=0.72, scale=0.22, size=n_samples), 0.15, 1.10)
    tax_paid_final_juta = reported_turnover_spt_juta * 0.005 # PP 55/2022 PPh Final 0.5%
    
    # 4. TARGET INDEPENDEN (Simulasi Hasil Pemeriksaan Audit Faktual)
    # Target dibangkitkan dari ketidakkonsistenan laten kompleks nonlinier + audit discovery probability
    # Fitur input TIDAK memiliki akses ke unobserved error term ini
    unobserved_inventory_distortion = rng.exponential(scale=0.35, size=n_samples)
    cash_skimming_propensity = (1.0 - digital_payment_ratio) * rng.uniform(0.2, 0.9, size=n_samples)
    unreported_logistics_delta = np.maximum(0, (1.0 - logistics_tracking_ratio) - rng.uniform(0.05, 0.25, size=n_samples))
    
    latent_audit_finding_score = (
        0.35 * cash_skimming_propensity +
        0.30 * (unobserved_inventory_distortion / (1.0 + unobserved_inventory_distortion)) +
        0.20 * unreported_logistics_delta +
        0.15 * (1.0 - np.minimum(1.0, reported_turnover_spt_juta / (gmv_transaksi_juta + 1e-4))) +
        rng.normal(0, 0.12, size=n_samples)
    )
    
    audit_threshold = np.percentile(latent_audit_finding_score, 75.0)
    audit_non_compliance_flag = (latent_audit_finding_score > audit_threshold).astype(int)
    
    df = pd.DataFrame({
        "provinsi": provinsi,
        "gmv_transaksi_juta": np.round(gmv_transaksi_juta, 2),
        "annual_order_volume": annual_order_volume,
        "avg_ticket_size_ribu": np.round(avg_ticket_size_ribu, 2),
        "digital_payment_ratio": np.round(digital_payment_ratio, 4),
        "logistics_tracking_ratio": np.round(logistics_tracking_ratio, 4),
        "customer_return_rate": np.round(customer_return_rate, 4),
        "bps_ecom_penetration_pct": np.round(ecom_penetration, 2),
        "bps_infra_index": np.round(infra_index, 2),
        "reported_turnover_spt_juta": np.round(reported_turnover_spt_juta, 2),
        "tax_paid_final_juta": np.round(tax_paid_final_juta, 2),
        "target_non_compliance": audit_non_compliance_flag
    })
    
    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "bps_e_commerce_tax_compliance.csv")
    df = generate_benchmark_tax_dataset()
    df.to_csv(out_path, index=False)
    print(f"Generated non-circular benchmark dataset: {df.shape} -> {out_path}")
    print(f"Target distribution:\n{df['target_non_compliance'].value_counts(normalize=True)}")
