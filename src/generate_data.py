import os
import numpy as np
import pandas as pd

def generate_true_latent_benchmark(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    DATA GENERATING PROCESS (DGP) MURNI VARIABEL LATEN:
    Target Y dibangkitkan 100% dari variabel laten tak teramati (unobserved state)
    S_audit = 0.40 * delta_cash + 0.35 * delta_inv + 0.25 * delta_log + epsilon
    Fitur masukan X (GMV, SPT, PayRatio, Logistics, BPS Macro) hanyalah noisy proxy di lapangan.
    Tidak ada satu pun fitur X yang masuk ke dalam formula pembentukan target Y.
    """
    rng = np.random.default_rng(seed)
    
    provinsi_list = [
        "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Banten",
        "Sumatera Utara", "Riau", "Sumatera Selatan", "Bali", "Sulawesi Selatan"
    ]
    
    # 1. State Kepatuhan Laten Sejati (Ground Truth Laten Wajib Pajak - TIDAK DIBERIKAN KE X)
    delta_cash = rng.beta(a=2.0, b=4.0, size=n_samples)        # Kecenderungan transaksi off-the-books tunai
    delta_inv = rng.exponential(scale=0.25, size=n_samples)     # Distorsi arus barang & stok gudang
    delta_log = rng.beta(a=1.5, b=4.5, size=n_samples)         # Pengiriman tanpa resi sistem
    noise_audit = rng.normal(0, 0.08, size=n_samples)
    
    latent_audit_risk = (
        0.40 * delta_cash +
        0.35 * (delta_inv / (1.0 + delta_inv)) +
        0.25 * delta_log +
        noise_audit
    )
    audit_threshold = np.percentile(latent_audit_risk, 75.0)
    target_non_compliance = (latent_audit_risk > audit_threshold).astype(int)
    
    # 2. Indikator Kontekstual Wilayah BPS (Macro Covariates)
    # Sumber Resmi:
    # 1. BPS (2024), Statistik E-Commerce 2024, Tabel 3.1: Persentase Usaha Melakukan E-Commerce (%)
    # 2. BPS (2024), Indeks Pembangunan Teknologi Informasi dan Komunikasi (IP-TIK) 2023, Tabel 4: Skala 0-10
    provinsi = rng.choice(provinsi_list, size=n_samples)
    bps_macro_map = {
        "DKI Jakarta": (63.54, 7.73),
        "Jawa Barat": (43.38, 6.15),
        "Banten": (44.12, 6.38),
        "Jawa Timur": (36.85, 5.96),
        "Jawa Tengah": (33.20, 5.86),
        "Bali": (48.74, 6.60),
        "Sumatera Utara": (28.41, 6.04),
        "Sulawesi Selatan": (27.90, 6.01),
        "Riau": (26.15, 6.07),
        "Sumatera Selatan": (24.32, 5.88)
    }
    # Skala noise terkalibrasi: e-commerce (persentase) sigma=1.5, IP-TIK (skala 0-10) sigma=0.12
    ecom_penetration = np.array([bps_macro_map[p][0] + rng.normal(0, 1.5) for p in provinsi])
    infra_index = np.array([bps_macro_map[p][1] + rng.normal(0, 0.12) for p in provinsi])
    
    # 3. Fitur Teramati (Observable Noisy Proxies - FITUR INPUT X)
    # Fitur-fitur ini terpapar pengaruh variabel laten secara tidak langsung
    order_vol = rng.poisson(lam=140, size=n_samples) + 20
    ticket_size = rng.lognormal(mean=4.8, sigma=0.6, size=n_samples) + 25.0
    true_gmv = (order_vol * ticket_size) / 1000.0
    
    # PayRatio berkurang jika delta_cash tinggi (noisy proxy)
    digital_payment_ratio = np.clip(1.0 - (0.6 * delta_cash + rng.normal(0.2, 0.1, size=n_samples)), 0.05, 0.99)
    
    # Logistics tracking berkurang jika delta_log tinggi (noisy proxy)
    logistics_tracking_ratio = np.clip(1.0 - (0.5 * delta_log + rng.normal(0.15, 0.08, size=n_samples)), 0.10, 1.00)
    customer_return_rate = np.clip(rng.normal(loc=0.04, scale=0.02, size=n_samples), 0.001, 0.20)
    
    # Pelaporan SPT tertekan oleh delta_cash & delta_inv (noisy proxy)
    underreport_frac = np.clip(
        0.40 * delta_cash + 
        0.30 * (delta_inv / (1.0 + delta_inv)) + 
        rng.normal(0.10, 0.10, size=n_samples), 
        0.0, 0.85
    )
    reported_spt = true_gmv * (1.0 - underreport_frac)
    tax_paid_final = reported_spt * 0.005 # PPh Final PP 55/2022 (Deterministik administratif)
    
    df = pd.DataFrame({
        "provinsi": provinsi,
        "gmv_transaksi_juta": np.round(true_gmv, 2),
        "reported_turnover_spt_juta": np.round(reported_spt, 2),
        "tax_paid_final_juta": np.round(tax_paid_final, 2),
        "annual_order_volume": order_vol,
        "avg_ticket_size_ribu": np.round(ticket_size, 2),
        "digital_payment_ratio": np.round(digital_payment_ratio, 4),
        "logistics_tracking_ratio": np.round(logistics_tracking_ratio, 4),
        "customer_return_rate": np.round(customer_return_rate, 4),
        "bps_ecom_penetration_pct": np.round(ecom_penetration, 2),
        "bps_infrastructure_index": np.round(infra_index, 2),
        "target_non_compliance": target_non_compliance
    })
    
    return df

if __name__ == "__main__":
    df = generate_true_latent_benchmark()
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/tax_compliance_synthetic_data.csv", index=False)
    print(f"Dataset non-sirkular berhasil dibangkitkan: {df.shape}")
    print(f"Distribusi Target: {df['target_non_compliance'].value_counts(normalize=True).to_dict()}")
