import sys
import os

script_dir = "../al26_nbody/"
sys.path.append(script_dir)
sys.path.append(script_dir+"/plotting/")

import matplotlib.colors as mcolors
import matplotlib
from al26_plot import read_yields,read_state,calc_cdf,use_tex
from al26_nbody import Yields,State,Metadata
from glob import glob
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker
import matplotlib.cm as cm
from tqdm import tqdm
import seaborn as sns
import pandas as pd
from amuse.units import units
import colorsys
from seaborn import color_palette

al26ss = 5.85e-5
alinf  = al26ss * 0.1

data = pd.read_pickle("all-sims-ratios.pkl.zst")

# Filter out low and high mass stars
data = data[data.mass >= 0.1]
data = data[data.mass <= 3.0]
data = data[data.has_interloper == True]
data = data[data.is_interloper == False]
data = data[data.model == "agb"]
data = data[data.isotope == "26al"]

interloper_velocities = [1.0,3.0,10.0,30.0]

use_tex()
palette = sns.color_palette("colorblind", len(interloper_velocities))
fig, ax = plt.subplots(dpi=300, figsize=(5, 3))
for idx, velocity in enumerate(interloper_velocities):
  d = data.copy()
  d = d[d.interloper_velocity == velocity]

  distances = sorted(d.interloper_distance.unique())
  frac_enriched = []

  for distance in distances:
    dd = d[d.interloper_distance == distance]
    al26_yield = dd.yield_ratio_decay
    al26_sub = al26_yield[al26_yield >= alinf]
    nstars = len(al26_yield)
    nal26s = len(al26_sub)
    print(f"vel={velocity:<7.2f} x={distance:<7.2f} ndisk={nstars:<4d} nal0.1={nal26s:<4d} zal0.1={nal26s/nstars:.3f} max_enrich={al26_yield.max():.3e}")
    frac_enriched.append(nal26s / nstars if nstars > 0 else 0)

  ax.plot(distances, frac_enriched, color=palette[idx], label=f"$v_i$={int(velocity)} km/s")

ax.set_xlim(-25, 0)
ax.set_ylim(0, 0.5)
ax.set_xlabel("$x_i$ (pc)")
ax.set_ylabel("Enriched disk fraction, $Z_\\mathrm{26Al,0.1SS}$")
# Add a single colorbar for all subplots
fig.subplots_adjust(right=0.88, hspace=0.25, wspace=0.25)
ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax.yaxis.set_major_locator(mticker.MultipleLocator(0.1))
ax.yaxis.set_minor_locator(mticker.MultipleLocator(0.025))
ax.grid(True, which='both', linestyle=':', alpha=0.1)
ax.legend(loc="upper left", frameon=True, ncol=2)

# cbar_ax = fig.add_axes([0.91, 0.08, 0.02, 0.84])

# cbar = fig.colorbar(pc, cax=cbar_ax, extend="max")

# cbar.set_label("Enriched disk fraction, $Z_\\mathrm{26Al,0.1SS}$")

# fig.tight_layout(rect=[0, 0, 0.9, 1])
plt.savefig("set-c-2-x-vs-vel.pdf", bbox_inches="tight")
