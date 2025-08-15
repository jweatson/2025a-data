import sys
script_dir = "../al26_nbody/"
sys.path.append(script_dir)
sys.path.append(script_dir+"/plotting/")
from al26_plot import use_tex
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read in data file
d = pd.read_pickle("all-sims-ratios.pkl.zst")

# Filter out low and high mass stars, and apply additional filters
d = d[d.mass >= 0.1]
d = d[d.mass <= 3.0]
d = d[d.has_interloper == True]
d = d[d.is_interloper == False]
d = d[d.rc == 0.3]
d = d[d.interloper_bubble_radius == 0.1]

interloper_masses = [7.0]
interloper_velocities = [1.0,3.0, 10.0, 30.0]
markers = ["o", "s", "^", "P"]
colours = sns.color_palette("colorblind", n_colors=len(interloper_velocities))

pop_sizes = [100, 300, 500, 1000]

use_tex()

fig, axs = plt.subplots(2, 2, figsize=(10, 6), dpi=600, sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.15, wspace=0.15)
axs = axs.flatten()


for idx, pop in enumerate(pop_sizes):
  ax = axs[idx]
  d_pop = d[d.nstars == pop]
  for i_m, interloper_mass in enumerate(interloper_masses):
    for i_v, interloper_velocity in enumerate(interloper_velocities):
      dd = d_pop
      dd = dd[dd.interloper_mass == interloper_mass]
      dd = dd[dd.interloper_velocity == interloper_velocity]
      dd = dd[dd.model == "agb"]

      ddm = dd[dd.initial_mass >= 0.5]
      ddm = ddm[ddm.initial_mass <= 1.5]

      ddx = dd[dd.isotope == "60fe"].yield_ratio_decay
      ddy = dd[dd.isotope == "26al"].yield_ratio_decay
      ddmx = ddm[ddm.isotope == "60fe"].yield_ratio_decay
      ddmy = ddm[ddm.isotope == "26al"].yield_ratio_decay

      print(max(ddmx), max(ddmy), min(ddmx), min(ddmy))

      label = "$v_i$={:.1f}$\\,$km/s".format(interloper_velocity)
      ax.scatter(ddx, ddy, c=colours[i_v], marker=markers[i_m], s=1, linewidths=0, alpha=0.3)
      ax.scatter(ddmx, ddmy, c=colours[i_v], marker=markers[i_m], s=6, linewidths=0, label=label,alpha=1.0, zorder=2)

  ax.set_xlim(1e-9, 1e-2)
  ax.set_ylim(1e-9, 1e0)
  ax.set_xscale("log")
  ax.set_yscale("log")
  ax.set_title(f"$N_\\star$ = {pop}")
  ax.axvline(1.15e-8, color="red",zorder=2, ls="--")
  ax.axvline(1.00e-6, color="red",zorder=2, ls="--")
  ax.axhline(5.85e-5, color="red",zorder=2, ls="--")
  ax.tick_params(axis="both", which="both", direction="in")
  # Set y-label only for plots on the left
  if idx % 2 == 0:
    ax.set_ylabel("$^{26}$Al/$^{27}$Al")
  # Set x-label only for plots on the bottom
  if idx >= 2:
    ax.set_xlabel("$^{60}$Fe/$^{56}$Fe")
    
  if idx == len(pop_sizes) - 1:
    ax.legend(loc="upper left", ncol=1)
  ax.grid(which="both", alpha=0.1, color="k", ls=":")


# plt.tight_layout()
plt.savefig("isotope_comparison_nstars_subfigs.pdf", bbox_inches="tight")
plt.close()
