import sys
import os

script_dir = "../al26_nbody/"
sys.path.append(script_dir)
sys.path.append(script_dir+"/plotting/")

import matplotlib
from al26_plot import read_state,use_tex
from al26_nbody import Yields,State,Metadata
from glob import glob
from scipy.stats import norm
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
from amuse.units import units
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import seaborn as sns



use_tex()

sims = sorted(glob("pt-0.3/run-*"))
nsims = len(sims)
print(nsims)


# velocities = np.logspace(-2,1,)
norm = matplotlib.colors.LogNorm(vmin=0.1,vmax=100.)

# Create a colormap that uses distinct base colors for each order of magnitude,
# and increases brightness within each order.

# Define base colors for each order of magnitude (0.1, 1, 10, 100)
base_colors = sns.color_palette("colorblind", 3)

# Create a custom colormap
def get_custom_colormap():
  colors = []
  n_steps_per_decade = 32
  for i, base in enumerate(base_colors):
    for j in range(n_steps_per_decade):
      # Increase brightness within the decade
      factor = 0.4 + 0.6 * (j / (n_steps_per_decade - 1))
      color = tuple(np.clip(factor * np.array(base), 0, 1))
      colors.append(color)
  return ListedColormap(colors, name='custom_log')

c_m = get_custom_colormap()

s_m = matplotlib.cm.ScalarMappable(cmap=c_m, norm=norm)
s_m.set_array([])


plt.figure(figsize=(5,3))

i = 0
for nsim in range(1,nsims+1):
  # print(nsim)
  simname = "pt-0.3/run-{}".format(nsim)
  # print(simname)
  statenames = sorted(glob(simname+"/*state*.pkl.zst"))
  print(simname)
  first_state = read_state(statenames[0])
  offset = first_state.metadata.args.interloper_offset_time.value_in(units.myr)
  velocity = first_state.metadata.args.interloper_velocity.value_in(units.kms)
  if offset == 0.01:
    xx = []
    yy = []
    for j,statename in enumerate(statenames):
      state = read_state(statename)
      time = state.metadata.time.value_in(units.myr)

      # print(simname,offset,sim_num,time)
      x = state.cluster.x[-1]
      y = state.cluster.y[-1]
      z = state.cluster.z[-1]

      d2a = state.cluster[:-1].distances_squared(state.cluster[-1])
      d2 = sorted(d2a)[0]
      d = d2**0.5
      dist_si = d.value_in(units.pc)

      xx.append(time)
      yy.append(dist_si)

    plt.plot(xx,yy,color=s_m.to_rgba(velocity),alpha=1.)
    i += 1
    print("finished {}".format(nsim))

plt.xlim(0,10)
plt.ylim(0,2)
plt.grid(ls=":")
plt.xlabel("Simulation time, $t$ (Myr)")
plt.ylabel("Nearest star distance, $d_{i,n}$ (pc)")
cbar = plt.colorbar(s_m,ax=plt.gca(),label="Interloper velocity, $v_i$ (km$\\,$s$^{-1}$)")
plt.savefig("distance_from_nearest.pdf",bbox_inches="tight")