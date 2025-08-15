'''
This is not really performant or well written code, but it works.

Code to calculate the mass loss of SLRs in the wind of an AGB star throughout the AGB phase.

Method assumes that the isotopic ratio of 60Fe and 26Al to their stable counterparts are constant throughout the AGB phase, as are the elemental mass fractions in the wind. Whilst these are two fairly big assumptions this should be fine for the N-body work we are performing.

Derived from the following research:
Karakas, A. I., & Lugaro, M. (2016). Stellar Yields From Metal-Rich Asymptotic Giant Branch Models. The Astrophysical Journal, 825(1), 26. https://doi.org/10.3847/0004-637X/825/1/26
'''

# 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from amuse.units import units
from amuse.lab import SeBa,Particle,Particles
from tqdm import tqdm
import seaborn as sns
import matplotlib as mpl

nsteps=1024

# Star properties, derived from Karakas & Lugaro (2016), see above
star_masses = [3.,5.,6.,7.] | units.MSun
al26_mix    = [2.28E-03,9.47E-03,4.24E-02,7.29E-02,8.85E-02]
fe60_mix    = [6.74E-06,9.55E-04,1.14E-03,7.11E-04,7.45E-04]
al_yield    = [2.68906E-04,5.05140E-04,6.25450E-04,7.34474E-04,8.41198E-04]
fe_yield    = [6.35719E-03,1.14482E-02,1.41060E-02,1.67203E-02,1.92280E-02]
mass_loss   = [4.1330,5.0930,6.0370,6.9470] | units.MSun

# Set Nord dark theme for plots
nord_colors = [
  "#2E3440", "#3B4252", "#434C5E", "#4C566A",  # Polar Night
  "#D8DEE9", "#E5E9F0", "#ECEFF4",             # Snow Storm
  "#8FBCBB", "#88C0D0", "#81A1C1", "#5E81AC",  # Frost
  "#BF616A", "#D08770", "#EBCB8B", "#A3BE8C", "#B48EAD"  # Aurora
]

nord_bg = "#4C566A"
nord_fg = "#ECEFF4"
nord_grid = "#E5E9F0"
nord_axes = "#E5E9F0"
nord_cmap = sns.color_palette("mako", as_cmap=True)  # closest to Nord, inferno is not nordic

plt.style.use("dark_background")
mpl.rcParams.update({
  "axes.facecolor": nord_bg,
  "figure.facecolor": nord_bg,
  "axes.edgecolor": nord_axes,
  "axes.labelcolor": nord_fg,
  "xtick.color": nord_fg,
  "ytick.color": nord_fg,
  "text.color": nord_fg,
  "axes.grid": True,
  "grid.color": nord_grid,
  "axes.titlecolor": nord_fg,
  "savefig.facecolor": nord_bg,
  "savefig.edgecolor": nord_bg,
  "legend.edgecolor": nord_axes,
  "legend.facecolor": nord_bg,
  # "axes.prop_cycle": plt.cycler(color=sns.color_palette("nord", 8))
})

# Use Nord Aurora colors for lines
aurora_colors = nord_colors[12:17]
color_palette = aurora_colors

# sns.set_style("darkgrid", {"axes.facecolor": nord_colors[1], "grid.color": nord_colors[3]})
# sns.set_style("darkgrid", {"axes.facecolor": nord_colors[0], "grid.color": nord_colors[3]})

def agb_borders(masses):
  '''
  AGB borders: Find the start and end point for the AGB phase of stars of a given mass.
  Assumes that all stars will undergo this phase, relies on the SEBA stellar evolution code in AMUSE
  Also relies on adaptiv etimestep of SEBA, which has been reduced to improve accuracy, but could be
  off by a few thousand years.
  
  Inputs:
    masses: A list of masses in amuse units, used to fill the particles dataset for SEBA
  Outputs:
    start_times: AGB phase start time list in Myr
    finish_times: AGB phase finish time list in Myr
  '''
  # Initialise variables and outputs
  t = 0.0 | units.yr
  start_times = np.zeros(len(masses))
  finish_times = np.zeros(len(masses))
  # Setup seba
  stellar = SeBa(number_of_workers=4) # Use multicore for a bit more speed
  stellar.parameters.metallicity = 0.02 # Approximately solar metallicity
  stellar.particles.add_particles(Particles(mass = star_masses)) # Add masses as particles to SeBa
  while t <= 1e9 | units.yr: # Set a maximum time, just to prevent a total runaway
    step = 0.2*stellar.particles.time_step.min() # Calculate susbtep based on SeBa adaptive
    stellar.evolve_model(t+step) # Evolve model
    # Check each star to see if 
    for i,star in enumerate(stellar.particles):
      if star.stellar_type >= 5 | units.stellar_type:
        if start_times[i] == 0.0: # Initialising zeroes used to find if operation done before
          start_times[i] = t.value_in(units.Myr)
      if star.stellar_type >= 7 | units.stellar_type:
        if finish_times[i] == 0.0:
          finish_times[i] = t.value_in(units.Myr)
    if min(stellar.particles.stellar_type.value_in(units.stellar_type) >= 7):
      break # Finish up if all stars have exited the AGB phase
    t = t+step # Increment simulation time
  stellar.stop()
  return start_times,finish_times
    
# Execution:

# First, calculate start and finish times
start_times,finish_times = agb_borders(star_masses)

# # Initialise plot
# plt.rcParams.update({
#   "text.usetex": True,
#   "font.family": "serif",
#   "font.serif": ["Computer Modern Roman"],
# })




fig,ax = plt.subplots(2,1,figsize=(7,5),sharex=True)
fig.subplots_adjust(hspace=0)
# color_palette = sns.color_palette("colorblind", len(star_masses))


# Loop through list of stellar masses
for i,mass in enumerate(star_masses):
  times = np.linspace(start_times[i],finish_times[i],nsteps) | units.myr
  # Initialise new instance of seba per star, not efficient but reliable
  stellar = SeBa()
  stellar.parameters.metallicity = 0.02
  stellar.particles.add_particles(Particles(mass = mass))
  # Use a series of lists, again, not a particularly pythonic way of doing this, but its fine for this
  elapsed = []
  star_mass_arr = []
  al26_mass_loss_rate_arr = []
  fe60_mass_loss_rate_arr = []
  star_mass_loss_rate_arr = []
  al26_total_mass_loss_arr = []
  fe60_total_mass_loss_arr = []
  star_total_mass_loss_arr = []
  # Evolve simulation and calculate yields for specific points in time
  for time in tqdm(times):
    stellar.evolve_model(time)
    elapsed.append(time.value_in(units.myr) - start_times[i])
    # Determine mass loss rates and total losses
    mass_loss_rate  = -stellar.particles.wind_mass_loss_rate[0].value_in(units.MSun/units.yr)
    current_mass = stellar.particles.mass[0]
    total_mass_loss = (mass-current_mass).value_in(units.MSun)
    al26_frac = al_yield[i]*al26_mix[i]
    fe60_frac = fe_yield[i]*fe60_mix[i]
    # Caclulate mass loss rates and total mass losses for SLRS
    al26_mass_loss_rate = mass_loss_rate * al26_frac
    fe60_mass_loss_rate = mass_loss_rate * fe60_frac
    al26_total_mass_loss = total_mass_loss * al26_frac
    fe60_total_mass_loss = total_mass_loss * fe60_frac
    # Append to list, faster in general
    star_mass_arr.append(current_mass.value_in(units.MSun))
    al26_mass_loss_rate_arr.append(al26_mass_loss_rate)
    fe60_mass_loss_rate_arr.append(fe60_mass_loss_rate)
    star_mass_loss_rate_arr.append(mass_loss_rate)
    al26_total_mass_loss_arr.append(al26_total_mass_loss)
    fe60_total_mass_loss_arr.append(fe60_total_mass_loss)
    star_total_mass_loss_arr.append(total_mass_loss)    
  
  # Write file for each star mass using pandas
  df = pd.DataFrame(list(zip(elapsed,
                             star_mass_arr,
                             al26_mass_loss_rate_arr,
                             fe60_mass_loss_rate_arr,
                             star_mass_loss_rate_arr,
                             al26_total_mass_loss_arr,
                             fe60_total_mass_loss_arr,
                             star_total_mass_loss_arr)),
                    columns=["t",
                             "star_mass",
                             "26al_mass_loss_rate",
                             "60fe_mass_loss_rate",
                             "star_mass_loss_rate",
                             "26al_total_mass_loss",
                             "60fe_total_mass_loss",
                             "star_total_mass_loss"])
  df.to_csv("agb_slr_{}_msol.csv".format(int(mass.value_in(units.MSun))),index=False)
  # Plot lines
  ax[0].plot(elapsed,al26_mass_loss_rate_arr,"C{}".format(i),c=color_palette[i],label="{}$\\,$M$_\\odot$".format(int(mass.value_in(units.MSun))))
  ax[0].plot(elapsed,fe60_mass_loss_rate_arr,"C{}".format(i),c=color_palette[i],linestyle="--")
  ax[1].plot(elapsed,al26_total_mass_loss_arr,"C{}".format(i),c=color_palette[i],label="{}$\\,$M$_\\odot$".format(int(mass.value_in(units.MSun))))
  ax[1].plot(elapsed,fe60_total_mass_loss_arr,"C{}".format(i),c=color_palette[i],linestyle="--")

  
  # Annotate the lines at the start with isotope labels
  if len(elapsed) > 0:
    # Annotate 26Al line (only for the first line, not the first plot)
    if i == 0:
      # Annotate 26Al and 60Fe lines on both subplots
      # Mass loss rate subplot
      ax[0].annotate(
        "26Al",
        xy=(elapsed[0], al26_mass_loss_rate_arr[0]),
        xytext=(5, 0),
        textcoords="offset points",
        color=color_palette[i],
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.05", fc=nord_bg, ec=color_palette[i], lw=0.0, alpha=1.0)  # Smaller pad
      )
      ax[0].annotate(
        "60Fe",
        xy=(elapsed[0], fe60_mass_loss_rate_arr[0]),
        xytext=(5, 0),
        textcoords="offset points",
        color=color_palette[i],
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.05", fc=nord_bg, ec=color_palette[i], lw=0.0, alpha=1.0)  # Smaller pad
      )
      # Total mass loss subplot
      ax[1].annotate(
        "26Al",
        xy=(elapsed[0], al26_total_mass_loss_arr[0]),
        xytext=(5, 0),
        textcoords="offset points",
        color=color_palette[i],
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.05", fc=nord_bg, ec=color_palette[i], lw=0.0, alpha=1.0)  # Smaller pad
      )
      ax[1].annotate(
        "60Fe",
        xy=(elapsed[0], fe60_total_mass_loss_arr[0]),
        xytext=(2, 0),  # Reduced offset for tighter box
        textcoords="offset points",
        color=color_palette[i],
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.05", fc=nord_bg, ec=color_palette[i], lw=0.0, alpha=1.0)  # Smaller pad
      )
  stellar.stop() # Finish up SeBa

# Plotting
ax[0].set_yscale("log")
ax[1].set_yscale("log")
# ax[0].set_xlabel("AGB elapsed time (Myr)")
ax[1].set_xlabel("AGB elapsed time (Myr)")
ax[0].set_ylabel("SLR yield rate (M$_\\odot\\,$yr$^{-1}$)")
ax[1].set_ylabel("Total SLR yield (M$_\\odot$)")
ax[0].legend(loc="upper right")
# ax[1].legend()

ax[0].set_xlim(0,4.2)
ax[1].set_xlim(0,4.2)

ax[0].grid(which='major', linestyle=":")
ax[1].grid(which='major', linestyle=":")
plt.savefig("agb-yields-poster.pdf",bbox_inches="tight")