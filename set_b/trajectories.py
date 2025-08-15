import sys
import os

script_dir = "../al26_nbody/"
sys.path.append(script_dir)
sys.path.append(script_dir+"/plotting/")

import matplotlib.colors as mcolors
import matplotlib
from al26_plot import read_yields,read_state,calc_cdf,use_tex,sphere_wireframe
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
from scipy import interpolate
from seaborn import color_palette
from matplotlib.colors import LogNorm

use_tex()

sims = glob("pt-0.3/run-*")
nsims = len(sims)
# print(len(sims))

offsets = []
velocities = []


z_arr = np.zeros(nsims)


for i,simname in enumerate(tqdm(sims)):
  statenames = sorted(glob(simname+"/*state*.pkl.zst"))
  xx,yy,zz = [],[],[]
  sim_num = int(simname.split("-")[-1])
  for j,statename in enumerate(statenames):
    state = read_state(statename)
    
    offset = state.metadata.args.interloper_offset_time.value_in(units.myr)
    velocity = state.metadata.args.interloper_velocity.value_in(units.kms)
    time = state.metadata.time.value_in(units.myr)
    
    offsets.append(offset)
    velocities.append(velocity)

    if offset <= time:
      # print(simname,offset,sim_num,time)
      x = state.cluster.x[-1]
      y = state.cluster.y[-1]
      z = state.cluster.z[-1]
      cm = state.cluster[:-1].center_of_mass()
      dist = ((x - cm[0])**2 + (y - cm[1])**2 + (z - cm[2])**2)**0.5
      dist_si = dist.value_in(units.pc)
      # print(type(sim_num),type(dist_si))
      z_arr[sim_num-1] = dist_si
      # z_arr[sim_num-1] = velocity
      # print(dist.value_in(units.pc))
      break

    # yy.append(dist.value_in(units.pc))    
    # xx.append(time)
  plt.plot(xx,yy)

x = sorted(set(velocities))
y = sorted(set(offsets))
nx = len(x)
ny = len(y)

z_arr = z_arr.reshape((nx,ny))
z_arr = z_arr.transpose()

use_tex()
fig,ax = plt.subplots(dpi=300,figsize=(5, 4))
pc = ax.pcolormesh(x,y,z_arr,rasterized=True,cmap=color_palette("rocket",as_cmap=True),norm=LogNorm())

# levs = np.linspace(0,0.15,100)
# plt.pcolormesh(xxx,yyy,zzz,vmin=0,vmax=0.15)
ax.set_xscale("log")
ax.set_yscale("log")
# plt.colorbar()
ax.set_xlabel("Interloper velocity, $v_i$ (km$\\,$s$^{-1}$)")
ax.set_ylabel("Interloper time offset, $\\tau_i$ (Myr)")
ax.set_box_aspect(1)
ax.set_xlim(1e-2,1e1)
ax.set_ylim(1e-2,1e1)


cbar = fig.colorbar(pc)
cbar.set_label("AGB phase distance, $d_\\mathrm{AGB}$")
# plt.scatter(xxx,yyy,marker="o",s=(72./fig.dpi)**2)
fig.tight_layout()
plt.savefig("interloper-agb-distance.pdf",bbox_inches="tight")



print(nx,ny)

plt.savefig("test.png")



# nplot = 0
# for i,radius in enumerate(radii):
#   for j,vel in enumerate(vels):
#     nplot += 1
#     # ax = fig.add_subplot(len(radii),len(vels),nplot,projection="3d")
#     ax = fig.add_subplot(len(radii),len(vels),nplot)

#     simsetname = "pt-{}/pt-rc-{}-inm-{}-inv-{}/*".format(radius,radius,mass,vel)
#     simnames   = glob(simsetname)
#     for k,simname in enumerate(simnames[:nsamples]):
#       print(i,j,k)
#       statenames = sorted(glob(simname+"/*state*.pkl.zst"))
#       xx,yy,zz = [],[],[]
#       xxx,yyy,zzz = [],[],[]
#       for z,statename in enumerate(statenames):
#         state = read_state(statename)
#         xx.append(state.cluster.x[-1].value_in(units.pc))
#         yy.append(state.cluster.y[-1].value_in(units.pc))
#         zz.append(state.cluster.z[-1].value_in(units.pc))
#         if z == 0:
#           for s in range(len(state.cluster)-1):
#             xxx.append(state.cluster.x[s].value_in(units.pc))
#             yyy.append(state.cluster.y[s].value_in(units.pc))
#             zzz.append(state.cluster.z[s].value_in(units.pc))

#       # ax.plot(xx,yy,zz[:100],color=cols[k])

#       ax.plot(xx,yy,color=cols[k],rasterized=True)
#       # ax.scatter(xxx,yyy,color="tab:grey",alpha=0.2,marker=".",linewidths=0,rasterized=True)
#     ax.set_title("$v_i$={:.1f}$\\,$km/s, $r_c$={:.1f}$\\,$pc".format(vel,radius))

#     # xxw,yyw,zzw = sphere_wireframe(0,0,0,radius)
#     # ax.plot_wireframe(xxw,yyw,zzw,color="r",linewidth=0.25,linestyle="dotted")
#     ax.set_xlim(-2,6)
#     ax.set_ylim(-4,4)
#     ax.grid(linestyle=":")
#     # ax.set_zlim(-5*radius,5*radius)
#     ax.set_aspect("equal")

# fig.add_subplot(111, frameon=False)
# plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
# plt.xlabel("X (pc)")
# plt.ylabel("Y (pc)")

# plt.savefig("trajectories.pdf",bbox_inches="tight")