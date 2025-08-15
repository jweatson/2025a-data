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
fig, axes = plt.subplots(4, 1, dpi=300, figsize=(7, 5), sharex=True, sharey=True)
axes = axes.flatten()

for idx, velocity in enumerate(interloper_velocities):
  d = data.copy()
  d = d[d.interloper_velocity == velocity]

  sims = d.sim_number.unique()
  distances = sorted(d.interloper_distance.unique())
  radius_offsets = sorted(d.interloper_radius_offset.unique())

  xxx, yyy, zzz = [], [], []

  for distance in distances:
    dd = d[d.interloper_distance == distance]
    for radius_offset in radius_offsets:
      ddd = dd[dd.interloper_radius_offset == radius_offset]
      al26_yield = ddd.yield_ratio_decay
      al26_sub = al26_yield[al26_yield >= alinf]
      nstars = len(al26_yield)
      nal26s = len(al26_sub)
      print(f"vel={velocity:<7.2f} x={distance:<6.2f} y={radius_offset:<6.2f} ndisk={nstars:<4d} nal0.1={nal26s:<4d} zal0.1={nal26s/nstars:.3f}")
      xxx.append(distance)
      yyy.append(radius_offset)
      zzz.append(nal26s/nstars)

  nx = len(distances)
  ny = len(radius_offsets)

  minx = distances[0]
  maxx = distances[-1]
  miny = radius_offsets[0]
  maxy = radius_offsets[-1]

  x = np.linspace(minx, maxx, nx + 1)
  y = np.linspace(miny, maxy, ny + 1)

  z = np.asarray(zzz)
  z = np.reshape(z, (nx, ny))
  z = z.transpose()

  ax = axes[idx]
  pc = ax.pcolormesh(x, y, z, rasterized=True, cmap=color_palette("inferno", as_cmap=True))
  pc.set_clim(0, 0.3)
  ax.set_xlim(-8, 0)
  ax.set_ylim(0, 1)
  ax.set_aspect('equal')
  if idx == 3:
    ax.set_xlabel("$x_i$ (pc)")
  ax.set_ylabel("$y_i$ (pc)")
  ax.set_title(f"$v_{{\\mathrm{{int}}}}$ = {velocity} km/s")

# Add a single colorbar for all subplots
fig.subplots_adjust(right=0.88, hspace=0.25, wspace=0.25)
cbar_ax = fig.add_axes([0.91, 0.08, 0.02, 0.84])

cbar = fig.colorbar(pc, cax=cbar_ax, extend="max")

cbar.set_label("Enriched disk fraction, $Z_\\mathrm{26Al,0.1SS}$")

fig.tight_layout(rect=[0, 0, 0.9, 1])
plt.savefig("set-c-interloper-run-posxy-pix-plot-multipanel.pdf", bbox_inches="tight")
