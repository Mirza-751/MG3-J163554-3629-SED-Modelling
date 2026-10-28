# Settings and data for the MG3 J163554+3629 analysis.
# Every notebook starts with:  %run mg3_setup.py
# All saved files (models, chains, tables, figures) are read from and written to ../results

import os
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import jetset
from jetset.data_loader import Data, ObsData
from jetset.sed_shaper import SEDShape
from jetset.obs_constrain import ObsConstrain
from jetset.model_manager import FitModel
from jetset.minimizer import ModelMinimizer
from jetset.mcmc import McmcSampler
from jetset.template_2Dmodel import EBLAbsorptionTemplate

warnings.filterwarnings('ignore')
print('JetSeT version:', jetset.__version__)      # the thesis used 1.3.0

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(HERE, '..', 'results'))
os.chdir(RESULTS_DIR)

# source and data
SED_FILE   = os.path.join(HERE, '..', 'data', 'SED.txt')   # nu [Hz], nuFnu [erg cm^-2 s^-1], error
Z_SOURCE   = 3.647763
OBJ_NAME   = 'J163547+362930'

SYSTEMATICS = 0.15                # 15% systematics on all points (the SED is not simultaneous)

# upper limits (observed frequency in Hz):
#   1.318e13, 2.417e13 : WISE W4, W3
#   1.709e22           : lowest-energy Fermi-LAT bin
#   4.188e24, 1.324e25, 7.646e25 : highest-energy Fermi-LAT bins
UL_FREQS = [1.318e13, 2.417e13, 1.709e22, 4.188e24, 1.324e25, 7.646e25]

# radio below 1e10 Hz is left out: the extended radio emission can't come from one compact zone
NU_FIT_MIN = 1e10
NU_FIT_MAX = 1e29

# model choices
EXT_FIELD_FRAME = 'blob'          # external fields in the blob frame, as in Sanchez Zaballa et al. (2025)
ETA_BASE        = 1/12            # for this value the JetSeT L_Disk equals the radiated disc luminosity
NH_COLD_TO_REL_E = 0.1            # cold protons per relativistic electron (only matters for energetics)

eta_grid = [0.057, 0.070, 1/12, 0.100, 0.150, 0.200, 0.300]

def eta_tag(eta):
    # 0.057 -> 'eta_0p057', 1/12 -> 'eta_0p083'
    return f"eta_{eta:.3f}".replace('.', 'p')

TEMPLATE_FILE = 'Template_ObsConstrain.pkl'
FIG_DIR = 'figures'
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 13, 'legend.fontsize': 10,
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': True, 'ytick.right': True,
    'figure.dpi': 110, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})

# load the SED (not rebinned, so every point, including each NuSTAR bin, enters the fit)
d = np.genfromtxt(SED_FILE)

data = Data(n_rows=d.shape[0])
data.set_field('x',  d[:, 0])
data.set_field('y',  d[:, 1])
data.set_field('dy', d[:, 2])

data.set_meta_data('z', Z_SOURCE)
data.set_meta_data('UL_CL', 0.95)
data.set_meta_data('restframe', 'obs')
data.set_meta_data('data_scale', 'lin-lin')
data.set_meta_data('obj_name', OBJ_NAME)

sed_data = ObsData(data_table=data)
sed_data.filter_data_set('-1', exclude=True)
sed_data.add_systematics(SYSTEMATICS, [10.**6, 10.**29])

# flag the upper limits (tight tolerance, so e.g. 4.188e22 and 4.188e24 don't get mixed up)
nu_all = np.array(sed_data.table['nu_data'])
for freq in UL_FREQS:
    mask = np.isclose(nu_all, freq, rtol=1e-3)
    if mask.sum() != 1:
        raise ValueError(f"UL frequency {freq:.3e} Hz matched {mask.sum()} points")
    sed_data.table['UL'][mask] = True

ul_mask = np.array(sed_data.table['UL'], dtype=bool)
in_fit  = (nu_all >= NU_FIT_MIN) & (nu_all <= NU_FIT_MAX)
nustar  = (nu_all > 3 * 2.418e17) & (nu_all < 79 * 2.418e17)
print(f"points: {len(nu_all)}  (detections {(~ul_mask).sum()}, UL {ul_mask.sum()}),"
      f" in fit range {in_fit.sum()}, in 3-79 keV {nustar.sum()}")
