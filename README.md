# SED Modelling of High-Redshift Blazar MG3 J163554+3629

This repository contains the full analysis pipeline for **Spectral Energy Distribution (SED) modelling** of the high-redshift FSRQ blazar **MG3 J163554+3629** (z = 3.648). The work extends the published one-zone leptonic model of Sánchez Zaballa et al. (2025) by applying multiple statistical fitting methods (Minuit, MCMC, UltraNest nested sampling) and a novel two-zone model, and by deriving Bayesian posterior distributions for the key physical parameters.

---

## Repository Structure

```
blazar-sed-modelling/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── SED.txt                              # Multi-wavelength SED (radio → gamma-ray)
│                                            # Radio (1.4 GHz) to Fermi-LAT (gamma-ray)
│                                            # Instruments: VLA, WISE, GAIA, Swift-UVOT,
│                                            #              XMM-Newton, Fermi-LAT, NuSTAR
│
├── pipelines/
│   └── 00_basic_pipeline.ipynb              # Data loading, systematics, binning
│                                            # SEDShape characterisation (sync + IC peaks)
│                                            # ObsConstrain prefit: SSC + EC (BLR, Disk, DT)
│                                            # Opening angle geometry + EBL (Franceschini 2008)
│   └── Fit_Pipeline_10 june.ipynb           # Earlier working version of the pipeline
│
├── analysis/
│   ├── one_zone/
│   │   ├── 01_interactive_model.ipynb       # Parameter exploration — tweak and plot instantly
│   │   └── 02_minuit_mcmc_ultranest.ipynb   # Full statistical analysis:
│   │                                        #   Minuit → MCMC (emcee) → UltraNest
│   │                                        #   Free params: B, M_BH, accr_eff (+ others)
│   │                                        #   Outputs: corner plots, posterior SED, log Z
│   └── two_zone/
│       ├── 03_two_zone_model.ipynb          # Two-zone prefit + Minuit fit
│       │                                    #   Zone 1 (compact): SSC + EC (BLR, Disk, DT)
│       │                                    #   Zone 2 (extended): SSC only, outside R_DT
│       └── 04_two_zone_ultranest.ipynb      # UltraNest on two-zone model
│                                            #   12 free params (Zone1 + Zone2)
│                                            #   log Z for Bayesian model comparison
│       └── 2 zone model with ultranest(12 June).ipynb   # Earlier working version
│
├── results/
│   ├── plots/                               # SED plots, corner plots, posterior envelopes
│   ├── tables/                              # Best-fit parameter tables
│   ├── models/                              # Saved pkl and npy outputs
│   ├── ultranest_output_NuSTAR/             # UltraNest run (one zone): chains, posterior summary
│   └── ultranest_output_2zone/              # UltraNest run (two zones): log
│
└── comparison/
    └── 05_comparison_jose.ipynb             # Comparison with Sánchez Zaballa et al. (2025):
                                             # M_BH, L_Disk, λ_Edd posteriors vs published
                                             # Seed black hole mass constraint (z=20 → z=3.65)
                                             # M_BH posteriors across BH spin grid (η = 0.057–0.300)
```

---

## Object

| Property | Value |
|----------|-------|
| Name | MG3 J163554+3629 |
| 4FGL designation | 4FGL J1635.6+3628 |
| Redshift | z = 3.648 |
| Classification | High-redshift FSRQ blazar |
| Position | R.A. = 248.947°, Dec = +36.492° |
| SED coverage | Radio (1.4 GHz) → Gamma-ray (10²⁵ Hz) |
| Variability timescale | 7 days |

---

## Methods Overview

### Physical Model

All fits use **JetSeT** (Tramacere et al. 2009, 2011, 2020) to build leptonic jet models with a broken power-law electron distribution:

n(γ) = K × γ^{−p} for γ < γ_break, K × γ^{−p₁} for γ ≥ γ_break

The emission model includes:
- **Synchrotron** radiation (self-absorbed)
- **SSC** (Synchrotron Self-Compton)
- **EC** (External Compton) from: Broad Line Region, Accretion Disk (MultiBB), Dust Torus
- **EBL absorption** via Franceschini et al. (2008)

The emitting region is located outside the BLR but within R_DT — consistent with EC_DT dominating the IC peak.

**Two-zone extension:** Zone 1 is a compact near-zone (R_H = 1.5×10¹⁸ cm); Zone 2 is an extended zone at 5×R_DT contributing SSC and synchrotron to the radio/sub-mm.

### Fitting Pipeline

| Step | Notebook | Tool | Notes |
|------|----------|------|-------|
| Prefit | `00_basic_pipeline` | JetSeT `ObsConstrain` | Physical initial guess from SED shape |
| Interactive | `01_interactive_model` | Manual | Parameter sensitivity exploration |
| One-zone fit | `02_minuit_mcmc_ultranest` | Minuit → MCMC → UltraNest | Full statistical analysis |
| Two-zone fit | `03_two_zone_model` | Minuit | Prefit + best-fit of composite model |
| Two-zone Bayes | `04_two_zone_ultranest` | UltraNest | Nested sampling, log Z for model comparison |
| Comparison | `05_comparison_jose` | — | Posteriors vs Sánchez Zaballa et al. (2025) |

### UltraNest Details
- Reactive nested sampler (`ultranest.ReactiveNestedSampler`) with slice stepping
- 200–400 live points depending on dimensionality
- Uniform priors within physically motivated ranges
- Bayesian evidence log Z enables model comparison (1-zone vs 2-zone, different η values)
- Seed mass constraint: Shapiro (2005) exponential growth from z = 20 to z = 3.65 (t = 1.72 Gyr)

---

## Key Physical Parameters

| Parameter | Symbol | Sánchez Zaballa et al. (2025) | Description |
|-----------|--------|-------------------|-------------|
| Magnetic field | B | 6.56×10⁻² G | Jet co-moving frame field strength |
| Bulk Lorentz factor | Γ | 19.0 | Jet bulk motion |
| Electron normalisation | N | 9.21×10² cm⁻³ | Number density of emitting electrons |
| Spectral index (low) | p | 1.45 | Below break |
| Spectral index (high) | p₁ | 3.58 | Above break |
| Break Lorentz factor | γ_break | 940 | Transition energy |
| Black hole mass | M_BH | 1.1×10⁹ M☉ | Central engine mass |
| Disk luminosity | L_Disk | 1.41×10⁴⁶ erg/s | Accretion disk power |
| Accretion efficiency | η | 0.083 | L_Disk = η Ṁ c² |
| Eddington ratio | λ_Edd | ~0.109 | L_Disk / L_Edd |
| Dust torus temperature | T_DT | 927 K | Peak of DT seed photon field |
| Dissipation distance | R_diss | 1.5×10¹⁸ cm | Outside BLR, inside R_DT |

---

## Comparison with Published Work

Results are compared against:

> **Sánchez Zaballa, J.M., Bottacini, E., & Tramacere, A. (2025)**
> *The High-redshift Blazar MG3 J163554+3629: Physical Properties and the Enigma of Its Unexpected Supermassive Black Hole Growth*
> Accepted ApJ — [arXiv:2505.13593](https://arxiv.org/abs/2505.13593)

Key published results:
- M_BH = 1.1 (+0.2/−0.1) × 10⁹ M☉
- L_Disk = 1.41 × 10⁴⁶ erg/s
- η = 0.083 (best-fit), explored from η = 0.057 (a=0) to η = 0.300 (a~0.998)
- Eddington-limited growth from z~30 cannot account for the observed M_BH — super-Eddington accretion or jet-enhanced growth required

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Mirza-751/MG3-J163554-3629-SED-Modelling.git
cd MG3-J163554-3629-SED-Modelling
```

### 2. Set up the environment
```bash
conda create -n jetset_env python=3.9
conda activate jetset_env
pip install -r requirements.txt
```

The analysis was developed and run with **JetSeT 1.3.0** on Python 3.9. `requirements.txt` does not pin versions, so a
newer JetSeT (1.4 is in preparation) may give slightly different fitted values.

### 3. Run in order
```
00_basic_pipeline.ipynb        ← start here (pipelines/)
01_interactive_model.ipynb     ← explore parameters (analysis/one_zone/)
02_minuit_mcmc_ultranest.ipynb ← full statistical fit (analysis/one_zone/)
03_two_zone_model.ipynb        ← two-zone Minuit (analysis/two_zone/)
04_two_zone_ultranest.ipynb    ← two-zone nested sampling (analysis/two_zone/)
05_comparison_jose.ipynb       ← comparison with paper (comparison/)
```

> **Note:** UltraNest runs are computationally expensive (hours). The outputs of the runs used here (saved models
> `*.pkl`, samples `*.npy`, and the `ultranest_output_*/` folders) are included in `results/`, so the plots and
> comparisons can be checked without re-running the samplers. Re-running the notebooks regenerates them.

> **Important:** All notebooks build the JetSeT model from scratch rather than loading from `.pkl` files. This avoids an issue seen with JetSeT 1.3.0, where the dependent parameter `R = R_H × tan(θ_open)` became corrupted after serialisation with `dill`.

---

## Requirements

See `requirements.txt`. Core packages:

- `jetset` — leptonic jet SED modelling (Tramacere et al. 2020)
- `astropy` — units, coordinates, data handling
- `emcee` — MCMC ensemble sampler
- `ultranest` — nested sampling and Bayesian evidence
- `iminuit` — Minuit gradient minimiser
- `corner` — posterior triangle plots
- `dill` — model serialisation
- `matplotlib`, `numpy`, `scipy` — scientific computing

---

## Author

**Mirza Laraib Mustafa**
*MSc student, University of Padova*
Supervisor: Prof. Eugenio Bottacini
Co-supervisor: Dr. Andrea Tramacere

---

## Reference

> Sánchez Zaballa, J.M., Bottacini, E., & Tramacere, A. (2025). *The High-redshift Blazar MG3 J163554+3629: Physical Properties and the Enigma of Its Unexpected Supermassive Black Hole Growth.* Accepted ApJ. [arXiv:2505.13593](https://arxiv.org/abs/2505.13593)

---

## License

Shared for academic review. Please contact the author before reusing any analysis code or results.
