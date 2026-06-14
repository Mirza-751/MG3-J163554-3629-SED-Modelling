# SED Modelling of High-Redshift Blazar MG3 J163554+3629

This repository contains the full analysis pipeline for **Spectral Energy Distribution (SED) modelling** of the high-redshift blazar **MG3 J163554+3629** (z = 3.648). The work spans one-zone and two-zone leptonic models, multiple statistical fitting methods (Minuit, MCMC, UltraNest nested sampling), and a comparison of derived physical parameters against the published results of Sánchez Zaballa (2025).

---

## Repository Structure

```
blazar-sed-modelling/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── data/
│   └── SED.txt                          # Multi-wavelength SED (radio → gamma-ray)
│
├── pipelines/
│   └── 00_basic_pipeline.ipynb          # Data loading, rebinning, SED shape characterisation
│                                        # ObsConstrain prefit (SSC + EC: BLR, Disk, DT)
│
├── analysis/
│   ├── one_zone/
│   │   ├── 01_minuit_binned.ipynb       # Minuit fit on rebinned (grouped) data
│   │   ├── 02_minuit_unbinned.ipynb     # Minuit fit on unbinned data
│   │   ├── 03_mcmc_binned.ipynb         # MCMC (emcee) fit on rebinned data
│   │   ├── 04_mcmc_unbinned.ipynb       # MCMC (emcee) fit on unbinned data
│   │   ├── 05_ultranest_binned.ipynb    # UltraNest nested sampling on rebinned data
│   │   └── 06_ultranest_unbinned.ipynb  # UltraNest nested sampling on unbinned data
│   │                                    # (NuSTAR-focused; Gaussian + uniform prior tests)
│   └── two_zone/
│       └── 07_two_zone_ultranest.ipynb  # 2-zone model (compact + extended) with UltraNest
│                                        # Zone 1: EC (BLR + Disk + DT), Zone 2: SSC
│
├── results/
│   ├── plots/                           # SED plots, corner plots, posterior envelopes
│   └── tables/                          # Best-fit parameter tables
│
└── comparison/
    └── 08_sanchez_zaballa_comparison.ipynb  # Comparison with Sánchez Zaballa (2025):
                                             # M_BH, L_Disk, λ_Edd, seed mass constraints
```

---

## Object

| Property | Value |
|----------|-------|
| Name | MG3 J163554+3629 |
| Redshift | z = 3.648 |
| Classification | High-redshift FSRQ blazar |
| SED coverage | Radio (1.4 GHz) → Gamma-ray (10²⁵ Hz) |
| Variability timescale | 7 days |

---

## Methods Overview

### Physical Model

All fits use **JetSeT** to build leptonic jet models with a broken power-law electron distribution. The emission model includes:

- **Synchrotron** radiation
- **SSC** (Synchrotron Self-Compton)
- **EC** (External Compton) from Broad Line Region, Accretion Disk (MultiBB), and Dust Torus

**Two-zone extension**: Zone 1 is a compact near-zone (between BLR and DT); Zone 2 is an extended zone contributing additional SSC flux.

### Fitting Pipeline

| Step | Notebook | Tool | Notes |
|------|----------|------|-------|
| Prefit | `00_basic_pipeline` | JetSeT `ObsConstrain` | Physical initial guess from SED shape |
| Binned fit | `01`, `03`, `05` | Minuit / emcee / UltraNest | Data grouped with bin_width = 0.15 |
| Unbinned fit | `02`, `04`, `06` | Minuit / emcee / UltraNest | Individual data points; NuSTAR-focused |
| 2-zone | `07` | UltraNest | Nested sampling over both zone parameters |
| Comparison | `08` | — | λ_Edd, M_BH, L_Disk vs Sánchez Zaballa (2025) |

### UltraNest Details
- Reactive nested sampler with slice stepping
- 400 live points
- Prior sensitivity tests: uniform vs. Gaussian prior on T_DT
- Bayesian model comparison (log Z) across BH spin values (η = 0.06 → 0.42)
- Seed mass constraint: growth from z = 20 to z = 3.65 (t = 1.72 Gyr)

---

## Key Physical Parameters

These are the primary free parameters constrained across analyses:

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| Electron normalisation | N | Number density of emitting electrons |
| Spectral indices | p, p₁ | Below/above break in broken power law |
| Break Lorentz factor | γ_break | Transition energy in electron distribution |
| Magnetic field | B | Jet co-moving frame field strength |
| Bulk Lorentz factor | Γ | Jet bulk motion |
| Black hole mass | M_BH | Central engine mass |
| Disk luminosity | L_Disk | Accretion disk radiative power |
| Eddington ratio | λ_Edd | L_Disk / L_Edd |
| Dust torus temp. | T_DT | Blackbody temperature of dust torus |

---

## Comparison with Published Work

Results are cross-checked against:

> Sánchez Zaballa, J.M. (2025) — SED modelling of MG3 J163554+3629
> M_BH = 1.1 × 10⁹ M☉ | L_Disk = 1.38 × 10⁴⁶ erg/s | λ_Edd ≈ 0.109

Key comparisons include posterior distributions of M_BH and λ_Edd, and the implied seed black hole mass required for growth to the observed mass by z = 3.65.

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/blazar-sed-modelling.git
cd blazar-sed-modelling
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run in order
Start with `pipelines/00_basic_pipeline.ipynb` to build the prefit model, then proceed through the numbered notebooks in `analysis/`.

> **Note**: UltraNest runs are computationally expensive. Saved chain outputs (`ultranest_output_*/`, `*.pkl`, `*.npy`) are excluded from version control via `.gitignore` but can be regenerated by re-running the relevant notebooks.

---

## Requirements

See `requirements.txt`. Core packages:

- `jetset` — leptonic jet SED modelling
- `astropy` — units, data handling
- `sherpa` — fitting framework and Minuit interface
- `emcee` — MCMC ensemble sampler
- `ultranest` — nested sampling (Bayesian evidence)
- `iminuit` — Minuit minimiser
- `corner` — posterior triangle plots
- `dill` — serialisation of fit model objects
- `matplotlib`, `numpy`, `scipy` — scientific computing

---

## Author

**[Your Name]**
*[MSc/PhD student, University Name]*
Supervisor: [Supervisor Name]

---

## Reference

> Sánchez Zaballa, J.M. (2025) — *(add full journal citation)*

---

## License

Shared for academic review. Please contact the author before reusing code or results.
