#!/usr/bin/python

""".. _rdf

Calculating the radial distribution function
********************************************

In this tutorial we will learn how to analyse (ab-initio) molecular dynamics trajectories.
We will use the tool MDAnalysis to read our simulation data files and calculate the radial distribution 
function.

`Wikipedia page on RDF: <https://en.wikipedia.org/wiki/Radial_distribution_function>`_
`MDAnalysis documentation on RDF: <https://docs.mdanalysis.org/stable/documentation_pages/analysis/rdf.html>`_

We first import our python modules
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import MDAnalysis as mda
from MDAnalysis.analysis.rdf import InterRDF

# %%
# Then we define our project path. Replace the path with your own project path

PROJECT_PATH=Path("/home/kira/Git/fachlabor-dft-ml/solutions/")

# %%
# Next, we load our simulation output.

#universe = mda.Universe(PROJECT_PATH / "dft"/ "Argon_Simulation-pos-1.xyz")
universe = mda.Universe(PROJECT_PATH /"lammps"/"Ar_Trajectories.xyz")

# %%
## The Universe object contains the atomic positions for each timestep. 
## Note that the xyz file does not contain any information on the dimensions

print(f"dimensions from xyz file {universe.dimensions}")

# %%
# So we must set the dimensions ourself to 

box_l = 17.0742
universe.dimensions = [box_l, box_l, box_l, 90, 90, 90]

# %%
# Let's also check how many frames we've loaded with

print(f"loaded {len(universe.trajectory)} frames")

# %%
# We now want to run an radial distribution analysis using InterRDF

rdf = InterRDF(universe.atoms, universe.atoms, 
               n_bins = 100,
               range = (1.0, box_l / 2)
               )

# %%
# We then run the analysis with

rdf.run()

# %% 
# Next, we plot our results

plt.plot(rdf.results.bins, rdf.results.rdf)
plt.xlabel("$r$ in A")
plt.ylabel("g(r)")

# %%
# and save our figure

plt.savefig(PROJECT_PATH / "lammps" / "rdf.png", dpi=300)

