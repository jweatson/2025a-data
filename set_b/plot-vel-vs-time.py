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

d = pd.read_pickle("all-sims-ratios.pkl.zst")
# Filter out low and high mass stars
d = d[d.mass >= 0.1]
d = d[d.mass <= 3.0]
d = d[d.has_interloper == True]
d = d[d.is_interloper == False]
d = d[d.model == "agb"]
d = d[d.isotope == "26al"]
d = d[d.rc == 0.3]

sims = d.sim_number.unique()

velocities = sorted(d.interloper_velocity.unique())
time_offsets = sorted(d.interloper_time_offset.unique())

xxx,yyy,zzz = [],[],[]

for velocity in velocities:
  dd = d[d.interloper_velocity == velocity]
  for time_offset in time_offsets:
    ddd = dd[dd.interloper_time_offset == time_offset]
    al26_yield = ddd.yield_ratio_decay
    al26_sub   = al26_yield[al26_yield >= alinf]
    nstars = len(al26_yield)
    nal26s = len(al26_sub)
    print(f"vel={velocity:<7.2f} t={time_offset:<6.2f} ndisk={nstars:<4d} nal0.1={nal26s:<4d} zal0.1={nal26s/nstars:.3f}")
    xxx.append(velocity)
    yyy.append(time_offset)
    zzz.append(nal26s/nstars)

nx = len(velocities)
ny = len(time_offsets)

minx = velocities[0]
maxx = velocities[-1]
miny = time_offsets[0]
maxy = time_offsets[-1]

x = np.logspace(minx,maxx,nx+1)
y = np.logspace(miny,maxy,ny+1)

z = np.asarray(zzz)
z = np.reshape(z,(nx,ny))
z = z.transpose()

use_tex()
fig,ax = plt.subplots(dpi=300,figsize=(5, 4))
pc = ax.pcolormesh(velocities,time_offsets,z,rasterized=True,cmap=color_palette("inferno",as_cmap=True))

# levs = np.linspace(0,0.15,100)
# plt.pcolormesh(xxx,yyy,zzz,vmin=0,vmax=0.15)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1e-1,1e2)
ax.set_ylim(1e-2,1e1)
# plt.colorbar()
ax.set_xlabel("Interloper velocity, $v_i$ (km$\\,$s$^{-1}$)")
ax.set_ylabel("AGB time offset, $\\tau_i$ (Myr)")
ax.set_box_aspect(1)
cbar = fig.colorbar(pc,extend="max")
pc.set_clim(0, 0.3)
cbar.set_label("Enriched disk fraction, $Z_\\mathrm{26Al,0.1SS}$")
# plt.scatter(xxx,yyy,marker="o",s=(72./fig.dpi)**2)
fig.tight_layout()
plt.savefig("interloper-run-vel-time-pix-plot.pdf",bbox_inches="tight")
