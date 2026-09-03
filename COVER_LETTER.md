# COVER LETTER FOR MANUSCRIPT SUBMISSION

**Date:** September 3, 2026  
**To:** Editor-in-Chief / Editorial Board  
**Target Journal:** Jurnal Ilmiah Terakreditasi Nasional (SINTA 2) / International Peer-Reviewed Journal in Data Science & Computational Economics  

**Subject:** Submission of Original Research Article titled *"Kerangka Benchmark Simulasi Non-Sirkular untuk Pemeringkatan Risiko Kepatuhan Pajak Pedagang Daring melalui Integrasi Data Transaksi Gerbang Pembayaran, Logistik, dan Indikator Regional Berbasis Data BPS"*

Dear Editor-in-Chief and Esteemed Members of the Editorial Board,

We are pleased to submit our original research manuscript entitled:

> **"Kerangka Benchmark Simulasi Non-Sirkular untuk Pemeringkatan Risiko Kepatuhan Pajak Pedagang Daring melalui Integrasi Data Transaksi Gerbang Pembayaran, Logistik, dan Indikator Regional Berbasis Data BPS"**  
> *(English title: "A Non-Circular Synthetic Simulation Benchmark for E-Commerce Merchant Tax Compliance Risk Ranking Integrating Digital Payment Gateway, Logistics, and BPS Regional Indicators")*

by **Izam Rosiawan** (Corresponding Author, Telkom University Kampus Surabaya) and **Sulthan** (Telkom University Kampus Surabaya) for consideration of publication as a regular research article in your reputable journal.

---

### 1. Research Context and Background
The rapid expansion of the digital economy in Indonesia (with gross merchandise value projected to reach US\$99 billion by 2025) poses unprecedented monitoring challenges for the Directorate General of Taxes (DGT). Verifying the plausibility of self-reported turnover under the *self-assessment* system is increasingly constrained by information asymmetry, cross-border multi-channel platforms, and the absence of physical commercial presence. 

While statutory taxpayer confidentiality (Article 34 of Law KUP) legally restricts access to individual tax records for broad computational research, existing synthetic simulation benchmarks frequently suffer from **target circularity**—where ground-truth labels are inadvertently computed directly from observable features.

---

### 2. Core Contributions and Novelty
This study addresses this fundamental methodological challenge by formulating a strictly non-circular synthetic simulation framework as a proof-of-concept for tax compliance risk ranking:
1. **Independent Latent DGP Architecture:** Ground-truth audit outcomes ($Y$) are generated exclusively from unobserved latent behavioral states (cash skimming propensity, inventory distortion, and logistics tracking deviation), while observable features ($X$) serve as noisy empirical proxies bounded by realistic bivariate correlations ($\text{Corr}(Y, X) < 0.50$).
2. **Stepwise Feature Ablation with 95% Bootstrap CI:** Benchmarking across 5,000 simulated observations under 5-Fold Stratified Cross-Validation proves that self-reported tax returns alone exhibit negligible discriminatory power (ROC-AUC $0.5641$, PR-AUC $0.3192$). Progressively integrating payment gateway transactions and physical logistics tracking significantly elevates ranking quality to ROC-AUC $0.7667$ and PR-AUC $0.5455$ ($2.18\times$ above base rate). Incorporating BPS regional macro indicators yields a stable Top-20% Risk Yield of $45.2\%$ ($95\%$ CI $[40.8\%, 49.6\%]$, $2.26\times$ cumulative lift).
3. **Cross-Province Holdout Validation:** Repeated holdout testing across unseen provinces ($R=5$ province pairs) demonstrates consistent spatial interpolation within the simulation environment ($0.7643 \pm 0.0321$).
4. **Policy, Governance, and Algorithmic Accountability:** In compliance with Law No. 27 of 2022 on Personal Data Protection (UU PDP), we detail technical pseudonymization mechanisms (salted cryptographic hashing on NIK/NPWP) and evaluate operational audit threshold trade-offs between false-positive social costs and false-negative fiscal gap costs.

---

### 3. Verification, Ethics, and Open Science Commitments
* **Originality:** This manuscript represents original work and is not under consideration for publication elsewhere in any language.
* **No Conflicts of Interest:** The authors declare no competing financial or personal interests.
* **Open Science & Reproducibility:** In accordance with open data standards (Nowok et al., 2016; Snoke et al., 2018), all simulation generation code, automated ML training scripts, publication-grade figures, and the master Jupyter Notebook are made publicly accessible at:  
  👉 **`https://github.com/izamrosiawan/tax-compliance-automl`**

We believe this paper will be of high interest to your readership, bridging computational data science, machine learning, and fiscal policy administration.

Thank you very much for your time, consideration, and editorial stewardship.

Sincerely yours,

**Izam Rosiawan**  
Corresponding Author  
Program Studi Sains Data, Fakultas Informatika  
Telkom University, Kampus Surabaya  
Jl. Ketintang No. 156, Surabaya 60231, Jawa Timur, Indonesia  
Email: `izamrosiawan@student.telkomuniversity.ac.id`  

**Sulthan**  
Co-Author  
Direktorat Kampus Surabaya  
Telkom University, Kampus Surabaya, Indonesia  
