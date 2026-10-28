# MG3 J163554+3629: jet physics and black-hole growth at z = 3.65

This is the analysis of my master's thesis, *Jet Physics of MG3 J163554+3629 and Its Impact on Supermassive Black
Hole Evolution in the Early Universe* (M.Sc. Astrophysics and Cosmology, University of Padova, 2026; supervisor
Prof. Eugenio Bottacini, co-supervisor Dr. Andrea Tramacere). The full thesis is in [`thesis/`](thesis/).

MG3 J163554+3629 is one of the most distant blazars detected by Fermi-LAT. I model its broadband SED, including new
NuSTAR hard X-ray data, with a one-zone leptonic model in [JetSeT](https://github.com/andreatramacere/jetset), and
then use the fitted disc and jet to ask how a black hole of almost 2×10⁹ M☉ could have grown in the 1.7 Gyr since
z = 30.

![SED with the MCMC credible bands](results/figures/SED_MCMC_band_eta_0p083_7p.png)

## What I found

- **The emission region.** The SED is well fitted (χ² = 26.3 for 27 dof) with the emission region at
  R_H ≃ 1.2×10¹⁸ cm, outside the broad-line region and well inside the dusty torus, with B ≃ 0.06 G and Γ ≃ 18.
- **SSC vs external Compton.** NuSTAR separates the two: SSC gives 60–74 % of the emission at 10 keV and 37–56 % at
  40 keV, and the rest is external Compton, which also makes all of the γ-rays. This split is the same for every
  accretion efficiency.
- **The central engine.** The disc radiates L_disc ≃ 1.9×10⁴⁶ erg/s and the black hole mass is
  M_BH = (1.8 +0.5/−0.4)×10⁹ M☉ (for an inner disc radius of ~8 R_S), with an Eddington ratio λ ≃ 0.08.
- **The accretion efficiency can't be measured from the SED.** Seven efficiencies, η = 0.057 to 0.300 (spin
  a = 0 to ≃ 0.996), fit equally well (Δχ² = 0.76 across the grid): in this model η only changes the geometry of
  the BLR and torus.
- **Spin, jets and growth.** The jet carries several times the disc luminosity. Combining the jet power, the growth
  history and the proton content, the most consistent picture for one cold proton per ten electrons is a black hole
  spinning fast but not maximally (a ≈ 0.6–0.7) with a standard disc (η ≈ 0.09–0.10), grown from a heavy seed at an
  average Eddington ratio of 0.33–0.47. This is a consistent picture under the stated assumptions, not a measurement.

![Black-hole growth from z = 30](results/figures/bh_mass_evolution.png)

## The repository

```
thesis/        the thesis (PDF)
data/          SED.txt: the multiwavelength SED (radio to Fermi-LAT, incl. NuSTAR)
analysis/      the thesis analysis, six notebooks run in order + mg3_setup.py
results/       fitted models, MCMC chains, tables and figures saved by the notebooks
extensions/    two further analyses: nested sampling (UltraNest) and a two-zone model
```

### Thesis analysis (`analysis/`)

| notebook | |
|---|---|
| `01_data_and_template` | the SED, its shape (`SEDShape`) and the starting model (`ObsConstrain`) |
| `02_base_model` | Minuit fit and MCMC for η = 1/12 |
| `03_eta_grid` | Minuit and MCMC for each η = 0.057 … 0.300; which process makes the X-rays, MeV and GeV emission |
| `04_bh_growth` | seed mass and growth history from z = 30 for each η |
| `05_jet_energetics` | jet powers from the posteriors, proton content, jet power vs disc luminosity |
| `06_figures_tables_and_slides` | tables and figures for the thesis and the defence |

The fitted models and chains are in `results/`, so the notebooks open with all their figures and rerun in minutes
without refitting. Notebook 02 has `RUN_FIT` / `RUN_MCMC` switches, and notebook 03 skips any η whose fit or chain
already exists; delete those files to redo a fit (~15 min per fit, the same for each MCMC).

### Extensions (`extensions/`)

Before settling on the thesis set-up I also tried two things that are worth keeping. They use an earlier version of
the data handling (slightly different upper limits; the two-zone model also rebins the SED and drops the lowest-energy
Fermi-LAT point), so their numbers are not directly comparable with the thesis.

| notebook | |
|---|---|
| `01_one_zone_ultranest` | the one-zone model sampled with UltraNest, which also gives the Bayesian evidence |
| `02_two_zone_model` | a compact zone plus an extended zone outside the torus, so that the radio data can be fitted too |
| `03_two_zone_ultranest` | nested sampling of the two-zone model, and Minuit vs MCMC vs UltraNest on the same 7 parameters |
| `04_comparison_sanchez_zaballa` | the two-zone results next to the published one-zone model |

The UltraNest runs take hours; the notebooks show the outputs of my runs and the chains are in
`extensions/results/`.

## Running it

```bash
conda create -n jetset_env python=3.9
conda activate jetset_env
pip install -r requirements.txt
```

Everything was run with JetSeT 1.3.0; newer versions can move the fitted values slightly.

## References

The model set-up follows Sánchez Zaballa, Bottacini & Tramacere (2025), *The high-redshift blazar MG3 J163554+3629:
physical properties and the enigma of its unexpected supermassive black hole growth*, ApJ,
[arXiv:2505.13593](https://arxiv.org/abs/2505.13593). JetSeT: Tramacere (2020), Tramacere et al. (2011, 2009).

## Contact

Mirza Laraib Mustafa. Please get in touch before reusing the analysis or results.
