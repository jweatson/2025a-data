# 2025a-data
Post-processed data, simulation and processing code, and bootstrap scripts for my first submitted paper of 2025, _Short-Lived Radioisotopic enrichment from AGB interlopers in low-mass star-forming regions_.

# Repo contents

- `al26_nbody`
  - A copy of the `al26_nbody` programme used in the paper.
  - In particular, the stripped down version, `al26_nbody_agb_cyl.py`, which was used to run the simulations in the paper.
  - The plotting code is also included, in the subdirectory `plotting`.
    - This handles general plotting instructions and stuff for several plotting scripts in the other directories.
  - Also contained are a few older scripts and methods for determining mass loss rates that didn't make the cuts, checking the `al26_nbody_agb` scripts should make it clear what is and isn't used.
  - I've done my best to document most of it, but there are a few things that are either poorly documented or poorly made ("if it works, it works") functions, if you have any suggestions or want me to better document a section, please submit a pull request!
- `set_a` through `set_d`.
  - The yields data and post-processed data for simulation set A-D in the paper.
  - PDF versions of all plots in the paper.
  - Python scripts to generate these plots using the post-processed and yields data sets.
  - Bash scripts to run `al26_nbody_agb_cyl` in such a way that recreates the parameter space search performed in the paper.
    - Note this will not be exactly alike, as clusters are generated randomly. 
    - This will also take several days to run, depending on the power of the workstation, the bash scripts may also have issues when run on a different workstation to the one used in this paper.
- `linspace.py` and `logspace.py` are just wrappers to get bash to use these functions, I was running low on time and wanted to use them for the simulation set initialisation bash scripts.
- `README.md` is this document, hello!

# Other Notes and Observations

- A large amount of this code is kind of bodged together from better code I wrote for a previous paper, as such code is presented as-is, which means that there is a bunch of horrible "if it works, it works" plotting code, no real attempt to make the code work on every device, and a lot of bash scripts. I'm sorry for not doing much better than that, I always say I'll do better, but here we are.
- I am also sorry for constantly shifting between _ and - in filenames, I know that pains some people, I swear I am not doing it on purpose, I just forget which one I'm sticking with (it's _, for now).