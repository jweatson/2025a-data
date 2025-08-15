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

rc = float(sys.argv[1])

d = pd.read_pickle("all-sims-ratios.pkl.zst")
# Filter out low and high mass stars
d = d[d.mass >= 0.1]
d = d[d.mass <= 3.0]
d = d[d.has_interloper == True]
d = d[d.is_interloper == False]
d = d[d.rc == rc]

interloper_masses = [3.0,7.0]
interloper_velocities = [0.0,0.1,0.3,1.0,3.0,10.0]

markers = ["o","s","^","P"]
colours = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:gray"]


use_tex()
plt.figure(figsize=(10,4),dpi=600)

for i_m,interloper_mass in enumerate(interloper_masses):
  for i_v,interloper_velocity in enumerate(interloper_velocities):
    dd = d
    dd = dd[dd.interloper_mass == interloper_mass]
    dd = dd[dd.interloper_velocity == interloper_velocity]
    dd = dd[dd.model == "agb"]

    ddm = dd[dd.initial_mass >= 0.5]
    ddm = ddm[ddm.initial_mass <= 1.5]


    # ddx = dd[dd.isotope == "60fe"].yield_ratio_raw
    # ddy = dd[dd.isotope == "26al"].yield_ratio_raw
    # ddmx = ddm[ddm.isotope == "60fe"].yield_ratio_raw
    # ddmy = ddm[ddm.isotope == "26al"].yield_ratio_raw

    ddx = dd[dd.isotope == "60fe"].yield_ratio_decay
    ddy = dd[dd.isotope == "26al"].yield_ratio_decay
    ddmx = ddm[ddm.isotope == "60fe"].yield_ratio_decay
    ddmy = ddm[ddm.isotope == "26al"].yield_ratio_decay

    label = "$M_i$={:.0f}$\\,\\mathrm M_\\odot$, $v_i$={:.1f}$\\,$km/s".format(interloper_mass,interloper_velocity)
    plt.scatter(ddx,ddy,c=colours[i_v],marker=markers[i_m],s=1,linewidths=0,alpha=0.8)
    plt.scatter(ddmx,ddmy,c=colours[i_v],marker=markers[i_m],s=4,linewidths=0,label=label)

plt.xlim(1e-10,1e-4)
plt.ylim(1e-9,1e-1)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("$^{60}$Fe/$^{56}$Fe")
plt.ylabel("$^{26}$Al/$^{27}$Al")

plt.axvline(1.15e-8,color="red",ls=":")
plt.axvline(1.00e-6,color="red",ls=":")
plt.axhline(5.85e-5,color="red",ls=":")

print(len(d))
print(len(ddmx))

legend = plt.legend(loc="upper left",ncol=3,numpoints=4,prop={'size': 8})
# legend.get_frame().set_alpha(0)
# legend.get_frame().set_facecolor((0, 0, 1, 0.1))

# plt.grid(which="both",alpha=0.1,color="k",ls=":")
plt.tick_params(axis="both",which="both",direction="in")

plt.savefig("isotope_comparison_rc{}.pdf".format(rc),bbox_inches="tight")