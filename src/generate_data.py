import os
import numpy as np
import pandas as pd

def generate_bps_digital_tax_dataset(n_samples=5000, seed=42):
    """
    Simulasi sintetik data BPS Statistik E-Commerce & Ekonomi Digital Provinsi/Kabupaten
    yang digabungkan dengan fitur transaksi digital & kepatuhan pajak (CRM DJP).
    Fixed seed=42 untuk reprodusibilitas penuh (Anti-Leakage Standard).
    """
    np.random.seed(seed)
    
    provinsi_list = [
        'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Banten',
        'Sumatera Utara', 'Riau', 'Sumatera Selatan', 'Bali', 'Sulawesi Selatan'
    ]
    
    provinsi = np.random.choice(provinsi_list, size=n_samples)
    
    # 1. Indikator Ekonomi Digital BPS
    gmv_transaksi_juta = np.random.exponential(scale=150, size=n_samples) + 10
    volume_transaksi_tahunan = np.random.poisson(lam=120, size=n_samples) + 12
    proporsi_e_commerce_pct = np.clip(np.random.normal(loc=35, scale=12, size=n_samples), 5, 95)
    infrastruktur_digital_score = np.random.uniform(50, 99, size=n_samples)
    
    # 2. Fitur Transaksi & Finansial (Payment Gateway & Logistik)
    rasio_pembayaran_digital = np.clip(np.random.beta(a=5, b=2, size=n_samples), 0.1, 1.0)
    frekuensi_pengiriman_logistik = (volume_transaksi_tahunan * np.random.uniform(0.8, 1.1, size=n_samples)).astype(int)
    
    # 3. Fitur Pajak & Pelaporan SPT (Fiskal)
    omset_dilaporkan_spt_juta = gmv_transaksi_juta * np.random.uniform(0.4, 1.05, size=n_samples)
    pajak_disetor_juta = omset_dilaporkan_spt_juta * 0.005 # PPN/PPh Final 0.5% UMKM
    
    # 4. Konstruksi Target: Indicator Compliance Risk / Anomaly Flag (0: Patuh/Rendah, 1: Berisiko Tinggi)
    # Target tidak direkonstruksi langsung dari fitur tunggal (Anti-Leakage)
    rasio_underreporting = (gmv_transaksi_juta - omset_dilaporkan_spt_juta) / (gmv_transaksi_juta + 1e-5)
    risk_score_true = (
        0.5 * rasio_underreporting +
        0.3 * (1 - rasio_pembayaran_digital) +
        0.2 * (gmv_transaksi_juta / 500.0) +
        np.random.normal(0, 0.1, size=n_samples)
    )
    
    target_risk_flag = (risk_score_true > np.percentile(risk_score_true, 75)).astype(int)
    
    df = pd.DataFrame({
        'provinsi': provinsi,
        'gmv_transaksi_juta': np.round(gmv_transaksi_juta, 2),
        'volume_transaksi_tahunan': volume_transaksi_tahunan,
        'proporsi_e_commerce_pct': np.round(proporsi_e_commerce_pct, 2),
        'infrastruktur_digital_score': np.round(infrastruktur_digital_score, 2),
        'rasio_pembayaran_digital': np.round(rasio_pembayaran_digital, 3),
        'frekuensi_pengiriman_logistik': frekuensi_pengiriman_logistik,
        'omset_dilaporkan_spt_juta': np.round(omset_dilaporkan_spt_juta, 2),
        'pajak_disetor_juta': np.round(pajak_disetor_juta, 2),
        'target_compliance_risk': target_risk_flag
    })
    
    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "bps_e_commerce_tax_compliance.csv")
    df = generate_bps_digital_tax_dataset()
    df.to_csv(out_file, index=False)
    print(f"Dataset BPS E-Commerce Tax Compliance berhasil dibuat di: {out_file}")
    print(f"Bentuk Dataset: {df.shape}")
    print(f"Distribusi Target Risk Flag:\n{df['target_compliance_risk'].value_counts(normalize=True)}")
