import os
import numpy as np
import pandas as pd

def generate_true_latent_benchmark(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    DATA GENERATING PROCESS (DGP) MURNI VARIABEL LATEN:
    Target Y dibangkitkan 100% dari variabel laten tak teramati (unobserved state)
    S_audit = 0.40 * delta_cash + 0.35 * delta_inv + 0.25 * delta_log + epsilon
    Fitur masukan X (GMV, SPT, PayRatio, Logistics) hanyalah noisy proxy di lapangan.
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
    provinsi = rng.choice(provinsi_list, size=n_samples)
    bps_macro_map = {
        "DKI Jakarta": (62.4, 94.2), "Jawa Barat": (41.5, 78.6),
        "Jawa Tengah": (33.2, 72.1), "Jawa Timur": (36.8, 75.4),
        "Banten": (44.1, 79.8), "Sumatera Utara": (28.4, 68.2),
        "Riau": (26.1, 65.4), "Sumatera Selatan": (24.3, 63.1),
        "Bali": (48.7, 84.5), "Sulawesi Selatan": (27.9, 67.8)
    }
    ecom_penetration = np.array([bps_macro_map[p][0] + rng.normal(0, 1.5) for p in provinsi])
    infra_index = np.array([bps_macro_map[p][1] + rng.normal(0, 1.2) for p in provinsi])
    
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
    underreporting_fraction = np.clip(0.4 * delta_cash + 0.3 * (delta_inv / (1.0 + delta_inv)) + rng.normal(0.1, 0.1, size=n_samples), 0.0, 0.85)
    reported_turnover_spt = true_gmv * (1.0 - underreporting_fraction)
    tax_paid_final = reported_turnover_spt * 0.005
    
    df = pd.DataFrame({
        "provinsi": provinsi,
        "gmv_transaksi_juta": np.round(true_gmv, 2),
        "annual_order_volume": order_vol,
        "avg_ticket_size_ribu": np.round(ticket_size, 2),
        "digital_payment_ratio": np.round(digital_payment_ratio, 4),
        "logistics_tracking_ratio": np.round(logistics_tracking_ratio, 4),
        "customer_return_rate": np.round(customer_return_rate, 4),
        "bps_ecom_penetration_pct": np.round(ecom_penetration, 2),
        "bps_infra_index": np.round(infra_index, 2),
        "reported_turnover_spt_juta": np.round(reported_turnover_spt, 2),
        "tax_paid_final_juta": np.round(tax_paid_final, 2),
        "target_non_compliance": target_non_compliance
    })
    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "bps_e_commerce_tax_compliance.csv")
    df = generate_true_latent_benchmark()
    df.to_csv(out_path, index=False)
    print(f"Generated 100% latent-independent benchmark: {df.shape} -> {out_path}")
