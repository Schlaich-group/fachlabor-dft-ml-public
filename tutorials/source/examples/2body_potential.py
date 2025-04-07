#!/usr/bin/python

""".. _2_body_potential:

Calculating the 2 body potential of Argon using ASE and CP2K
============================================================

In this tutorial you will learn how to calculate the 2 body potential between two Argon atoms with DFT. 
We will use ASE (Atomic Simulation Environment) to setup our simulation. 
To do our energy calculation, ASE will call CP2K, which implements DFT.

First, we import our Python modules
"""

import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.calculators.cp2k import CP2K
import matplotlib
import scipy.constants as c

matplotlib.use("agg")

# %%
# We also import pint, which will help us to keep track of units

import pint

ureg = pint.UnitRegistry()

# %%
# Next, we create an Atoms object with two argon atoms placed a distance apart.

distance = 3.3 * ureg.angstrom
two_argon_atoms = Atoms("Ar2", [[0, 0, 0], [0, 0, distance.magnitude]])

# %%
# We set the cubic simulation box size to something much larger than Ar-Ar distance
# and apply periodic boundary conditions in all directions

two_argon_atoms.center(vacuum=3)
two_argon_atoms.pbc = [1, 1, 1]

# %%
# We will use CP2K as a calculator for our Atoms object.
# First, we specify calculation settings, you will not have to worry about these

inp = """
# Parameters for force calculation.
&FORCE_EVAL
    # Define the DFT parameters

    &DFT
        &SCF
            &OT
                MINIMIZER DIIS
                PRECONDITIONER FULL_SINGLE_INVERSE
            &END OT
            &OUTER_SCF
                MAX_SCF 100
                EPS_SCF 1.0E-6
            &END OUTER_SCF
        &END SCF

    &END DFT
&END FORCE_EVAL
"""

# %%
# Next, we specify our basis set, pseudo potential and exchange correlation functional

two_argon_atoms.calc = CP2K(inp=inp,
                            basis_set="DZVP-MOLOPT-SR-GTH",
                            pseudo_potential="GTH-PBE-q8",
                            potential_file="GTH_POTENTIALS",
                            xc="PBE",
                            command="cp2k.psmp -s",
                            )


# %%
# We can now run our first DFT calculation with

E = two_argon_atoms.get_potential_energy()
print(E)

# %% 
# This will return us a single potential energy for the specified interatomic distance
# Next, we want to sample a region between 1 and 10 angstrom and get the potential energy for each distance

distances = np.linspace(3.3, 6.0, 20)
energies = np.zeros(distances.shape)

for i in range(len(distances)):
    two_argon_atoms.set_positions([[0, 0, 0], [0, 0, distances[i]]])
    two_argon_atoms.center(vacuum=3)
    print(distances[i])
    print(two_argon_atoms.get_positions())

    E = two_argon_atoms.get_potential_energy()
    print(E)
    energies[i] = E

# %%
# Finally, we plot the energy as a function of the interatomic distance. 

plt.plot(distances, energies, "x", label="DFT")
plt.xlabel("$R$ in Angstrom")
plt.ylabel("$E$ in eV")

plt.savefig("2body_potential.png", dpi=300)
