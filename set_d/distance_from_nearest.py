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
import seaborn as sns



use_tex()

sims = sorted(glob("pt-0.3/run-*"))
nsims = len(sims)







# # velocities = np.logspace(-2,1,)
# norm = matplotlib.colors.LogNorm(vmin=0.01,vmax=10.)

# custom_colors = ["#073b4c","#118ab2","#06d6a0","#ffd166","#f78c6b","#ef476f"]
# c_m = ListedColormap(custom_colors)

# s_m = matplotlib.cm.ScalarMappable(cmap=c_m, norm=norm)
# s_m.set_array([])


vels = [1.0,3.0,10.0,30.0]
nstars = [100, 300, 500, 1000]

fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)
plt.subplots_adjust(hspace=0.15, wspace=0.15)
axes = axes.flatten()

for i,vel in enumerate(vels):
  for j,nstar in enumerate(nstars):
    simsetname = "pt-0.3/pt-rc-0.3-inm-7-inv-{}-rb-0.1-ns-{}".format(vel,nstar)
    print(simsetname)
    sims = sorted(glob(simsetname+"/*"))
    nsims = len(sims)
    for n,simname in enumerate(sims):
      # print(simname)
      # print(simname)
      statenames = sorted(glob(simname+"/*state*.pkl.zst"))
      # print(statenames)
      first_state = read_state(statenames[0])
      offset = first_state.metadata.args.interloper_offset_time.value_in(units.myr)
      velocity = first_state.metadata.args.interloper_velocity.value_in(units.kms)
      if offset == 0.00:
        xx = []
        yy = []
        for m,statename in enumerate(statenames):
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
        palette = sns.color_palette("deep", n_colors=4)
        color = palette[i]
        axes[j].plot(xx, yy, color=color, alpha=0.8)
        print("finished {}".format(simname))



for ax in axes:
  ax.set_xlim(0, 10)
  ax.set_ylim(0, 2)
  ax.grid(ls=":")

# Label each subplot with the number of stars
for j, nstar in enumerate(nstars):
  axes[j].set_title(f"$N_\\star = {nstar}$")

# Add legend for velocities
import matplotlib.patches as mpatches

custom_labels = [f"$v_i = {v}$ km s$^{{-1}}$" for v in vels]
palette = sns.color_palette("deep", n_colors=4)
handles = [mpatches.Patch(color=palette[i], label=custom_labels[i], linewidth=plt.rcParams['lines.linewidth']) for i in range(len(vels))]
axes[1].legend(handles=handles, title="Interloper velocity", loc="upper right", frameon=True)

# Only set x/y labels on outer axes for shared axes
for ax in axes[2:]:
  ax.set_xlabel("Simulation time, $t$ (Myr)")
for ax in axes[::2]:
  ax.set_ylabel("Nearest star distance, $d_{i,n}$ (pc)")
plt.savefig("distance_from_nearest.pdf",bbox_inches="tight")




# plt.figure(figsize=(5,3))

# i = 0
# for nsim in range(nsims):
#   # print(nsim)
#   simname = "pt-0.3/run-{}".format(nsim)
#   # print(simname)
#   statenames = sorted(glob(simname+"/*state*.pkl.zst"))

#   print(simname)

#   first_state = read_state(statenames[0])
#   offset = first_state.metadata.args.interloper_offset_time.value_in(units.myr)
#   velocity = first_state.metadata.args.interloper_velocity.value_in(units.kms)
#   if offset == 0.01:
#     xx = []
#     yy = []
#     for j,statename in enumerate(statenames):
#       state = read_state(statename)
#       time = state.metadata.time.value_in(units.myr)

#       # print(simname,offset,sim_num,time)
#       x = state.cluster.x[-1]
#       y = state.cluster.y[-1]
#       z = state.cluster.z[-1]
      
#       cm = state.cluster[:-1].center_of_mass()
#       dist = ((x - cm[0])**2 + (y - cm[1])**2 + (z - cm[2])**2)**0.5
#       dist_si = dist.value_in(units.pc)
      
#       xx.append(time)
#       yy.append(dist_si)

#     plt.plot(xx,yy,color=s_m.to_rgba(velocity),alpha=0.8)
#     i += 1
#     print("finished {}".format(nsim))

# plt.xlim(0,10)
# plt.ylim(0,2)
# plt.grid(ls=":")
# plt.xlabel("Simulation time, $t$ (Myr)")
# plt.ylabel("Interloper distance to CoM, $d_i$ (pc)")
# cbar = plt.colorbar(s_m,ax=plt.gca(),label="Interloper velocity, $v_i$ (km$\\,$s$^{-1}$)")
# plt.savefig("distance_from_centre.pdf",bbox_inches="tight")