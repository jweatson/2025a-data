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
from uncertainties import ufloat 

def getstats(li,sci=False):
  mean = np.mean(li)
  err = np.std(li) / np.sqrt(len(li))
  uf = ufloat(mean, err)

  if sci == True:
    return "${:L}$".format(uf)
  if mean == 0.0:
    return "$0.0$"
  else:
    return "${:.1uL}$".format(uf)

  

d = pd.read_pickle("all-sims-ratios.pkl.zst")
d = d[d.is_interloper == False]
d = d[d.initial_mass >= 0.1]
d = d[d.initial_mass <= 3.0]
d = d[d.model == "agb"]


nstars = [100, 300, 500, 1000]
vels   = [1.0,3.0,10.0,30.0]

# print(d)

print("name, nstars, vel, ndiskstot, Zany, ZAlsig, ZAlsol, ZFelow, ZFehi, ZtotalAl, ZtotalFe")

for nstar in nstars:
  for vel in vels:
    name = "set-d-v-{}-ns-{}".format(vel,nstar)

    dd = d

    dd = dd[dd.rc == 0.3]
    dd = dd[dd.nstars == nstar]
    dd = dd[dd.interloper_velocity == vel]

    sims = dd.sim_number.unique()

    nstarstot   = []
    dddany      = []
    dddalsig    = []
    dddalsol    = []
    dddfelow    = []
    dddfehi     = []
    dddsolany   = []
    dddsolalsig = []
    dddsolalsol = []
    dddsolfelow = []
    dddsolfehi  = []
    dddtotalal  = []
    dddtotalfe  = []

    for sim in sims:
      ddd = dd
      ddd = ddd[ddd.sim_number == sim]

      dddal = ddd[ddd.isotope == "26al"]
      dddfe = ddd[ddd.isotope == "60fe"]

      nstarstot.append(len(dddal))
      dddany.append(len(dddal[dddal.yield_ratio_decay > 0.0]) / len(dddal))
      dddalsig.append(len(dddal[dddal.yield_ratio_decay >= 5.85e-6]) / len(dddal))
      dddalsol.append(len(dddal[dddal.yield_ratio_decay >= 5.85e-5]) / len(dddal))
      dddfelow.append(len(dddfe[dddfe.yield_ratio_decay >= 1.15e-8]) / len(dddal))
      dddfehi.append(len(dddfe[dddfe.yield_ratio_decay >= 1.00e-6]) / len(dddal))

      dddsol = ddd[ddd.initial_mass >= 0.5]
      dddsol = dddsol[dddsol.initial_mass <= 1.5]
      dddsolal = dddsol[dddsol.isotope == "26al"]
      dddsolfe = dddsol[dddsol.isotope == "60fe"]

      dddsolany.append(len(dddsolal[dddsolal.yield_ratio_decay > 0.0]))
      dddsolalsig.append(len(dddsolal[dddsolal.yield_ratio_decay >= 5.85e-6]) / len(dddsolal))
      dddsolalsol.append(len(dddsolal[dddsolal.yield_ratio_decay >= 5.85e-5]) / len(dddsolal))
      dddsolfelow.append(len(dddsolfe[dddsolfe.yield_ratio_decay >= 1.15e-8]) / len(dddsolal))
      dddsolfehi.append(len(dddsolfe[dddsolfe.yield_ratio_decay >= 1.00e-6]) / len(dddsolal))

      dddtotalal.append(dddal.yield_raw.sum())
      dddtotalfe.append(dddfe.yield_raw.sum())


    print("\\texttt{"+name+"}, ", end="")
    print(str(nstar)+", ", end="")
    print(str(vel)+", ", end="")
    print(str(sum(nstarstot))+", ", end="")
    print(getstats(dddany)+", ", end="")
    print(getstats(dddalsig)+", ", end="")
    print(getstats(dddalsol)+", ", end="")
    print(getstats(dddfelow)+", ", end="")
    print(getstats(dddfehi)+", ", end="")
    # print(getstats(dddsolany)+", ", end="")
    # print(getstats(dddsolalsig)+", ", end="")
    # print(getstats(dddsolalsol)+", ", end="")
    # print(getstats(dddsolfelow)+", ", end="")
    # print(getstats(dddsolfehi)+", ", end="")
    print(getstats(dddtotalal,sci=True)+", ", end="")
    print(getstats(dddtotalfe,sci=True), end="")
    print("")
      

