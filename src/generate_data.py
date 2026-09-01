import os
import numpy as np
import pandas as pd

def generate_bps_digital_tax_dataset(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    
    provinsi_choices = [
        "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Banten",
        "Sumatera Utara", "Riau", "Sumatera Selatan", "Bali", "Sulawesi Selatan"
    ]
    provinsi = rng.choice(provinsi_choices, size=n_samples)
    
    gmv_transaksi_juta = rng.exponential(scale=150.0, size=n_samples) + 10.0
    volume_transaksi_tahunan = rng.poisson(lam=120, size=n_samples) + 12
    proporsi_e_commerce_pct = np.clip(rng.normal(loc=35.0, scale=12.0, size=n_samples), 5.0, 95.0)
    infrastruktur_digital_score = rng.uniform(50.0, 99.0, size=n_samples)
    
    rasio_pembayaran_digital = np.clip(rng.beta(a=5.0, b=2.0, size=n_samples), 0.1, 1.0)
    frekuensi_pengiriman_logistik = (volume_transaksi_tahunan * rng.uniform(0.8, 1.1, size=n_samples)).astype(int)
    
    omset_dilaporkan_spt_juta = gmv_transaksi_juta * rng.uniform(0.4, 1.05, size=n_samples)
    pajak_disetor_juta = omset_dilaporkan_spt_juta * 0.005
    
    underreporting_ratio = (gmv_transaksi_juta - omset_dilaporkan_spt_juta) / (gmv_transaksi_juta + 1e-5)
    latent_risk = (
        0.45 * underreporting_ratio +
        0.30 * (1.0 - rasio_pembayaran_digital) +
        0.15 * (gmv_transaksi_juta / 500.0) +
        rng.normal(0.0, 0.08, size=n_samples)
    )
    risk_threshold = np.percentile(latent_risk, 75.0)
    target_risk = (latent_risk > risk_threshold).astype(int)
    
    return pd.DataFrame({
        "provinsi": provinsi,
        "gmv_transaksi_juta": np.round(gmv_transaksi_juta, 2),
        "volume_transaksi_tahunan": volume_transaksi_tahunan,
        "proporsi_e_commerce_pct": np.round(proporsi_e_commerce_pct, 2),
        "infrastruktur_digital_score": np.round(infrastruktur_digital_score, 2),
        "rasio_pembayaran_digital": np.round(rasio_pembayaran_digital, 3),
        "frekuensi_pengiriman_logistik": frekuensi_pengiriman_logistik,
        "omset_dilaporkan_spt_juta": np.round(omset_dilaporkan_spt_juta, 2),
        "pajak_disetor_juta": np.round(pajak_disetor_juta, 2),
        "target_compliance_risk": target_risk
    })

if __name__ == "__main__":
    target_path = os.path.join(os.path.dirname(__file__), "..", "data", "bps_e_commerce_tax_compliance.csv")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    df = generate_bps_digital_tax_dataset()
    df.to_csv(target_path, index=False)
    print(f"Generated {len(df)} records -> {target_path}")
