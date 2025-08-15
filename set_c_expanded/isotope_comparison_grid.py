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

rc_values = [0.3]
interloper_masses = [7.0]
interloper_velocities = [30.0]
markers = ["o", "s", "^", "P"]
colours = sns.color_palette("colorblind", n_colors=len(interloper_velocities))

use_tex()
fig, ax = plt.subplots(figsize=(5, 3), dpi=600)
axes = [ax]

d = pd.read_pickle("all-sims-ratios.pkl.zst")
# Filter out low and high mass stars
d = d[d.mass >= 0.1]
d = d[d.mass <= 3.0]
d = d[d.has_interloper == True]
d = d[d.is_interloper == False]

for ax, rc in zip(axes, rc_values):
  dd_rc = d[d.rc == rc]
  for i_m, interloper_mass in enumerate(interloper_masses):
    for i_v, interloper_velocity in enumerate(interloper_velocities):
      dd = dd_rc
      dd = dd[dd.interloper_mass == interloper_mass]
      dd = dd[dd.interloper_velocity == interloper_velocity]
      dd = dd[dd.model == "agb"]

      ddm = dd[dd.initial_mass >= 0.5]
      ddm = ddm[ddm.initial_mass <= 1.5]

      ddx = dd[dd.isotope == "60fe"].yield_ratio_decay
      ddy = dd[dd.isotope == "26al"].yield_ratio_decay
      ddmx = ddm[ddm.isotope == "60fe"].yield_ratio_decay
      ddmy = ddm[ddm.isotope == "26al"].yield_ratio_decay

      ddc = -dd[dd.isotope == "60fe"].interloper_distance
      ddmc = -ddm[ddm.isotope == "60fe"].interloper_distance

      label = "$v_i$={:.0f}$\\,$km/s".format(interloper_velocity)
      sc = ax.scatter(ddmx, ddmy, c=ddmc, cmap=sns.color_palette("flare", as_cmap=True), marker=markers[i_m], s=6, linewidths=0, label=label, zorder=2)
      # sc = ax.scatter(ddx, ddy, c=ddc, cmap=sns.color_palette("flare", as_cmap=True), marker=markers[i_m], s=1, linewidths=0)

  ax.set_xlim(1e-9, 1e-3)
  ax.set_ylim(1e-9, 1e0)
  ax.set_xscale("log")
  ax.set_yscale("log")
  ax.set_xlabel("Fe SLR yield ratio ($^{60}$Fe/$^{56}$Fe)")
  if ax is axes[0]:
    ax.set_ylabel("Al SLR yield ratio ($^{26}$Al/$^{27}$Al)")
  ax.axvline(1.15e-8, color="red", ls="--", zorder=2)
  ax.axvline(1.00e-6, color="red", ls="--", zorder=2)
  ax.axhline(5.85e-5, color="red", ls="--", zorder=2)
  # ax.set_title(f"$r_c$ = {rc}")
  cbar = plt.colorbar(sc, ax=ax, pad=0.01)
  cbar.set_label("Interloper initial distance, $x_i$ (pc)")

  ax.grid(which="both", alpha=0.1, color="k", ls=":")
  ax.tick_params(axis="both", which="both", direction="in")

# handles, labels = axes[0].get_legend_handles_labels()
# axes[-1].legend(handles, labels, loc="upper left", ncol=1)
# plt.tight_layout(rect=[0, 0, 1, 0.93])

plt.savefig("set-c-expanded-isotope-comparison.pdf".format(rc),bbox_inches="tight")