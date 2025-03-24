#!/usr/bin/python

"""
Learn forces and energies with GAP
==================================

In this tutorial you will learn how to learn energies and forces using GAP.

We will need quip and ase
"""

import numpy as np
import subprocess
from pathlib import Path
import ase
import ase.io 
import matplotlib.pyplot as plt
import matplotlib
import os
from quippy.potential import Potential

PROJECT_PATH=Path("/work/amam/ckf7015/fachlabor-dft-ml/solutions")
os.chdir(PROJECT_PATH)
# %%
# Next, we write a little bash script to run the gap_fit program. 

gap_fit_cmd = """
gap_fit e0_method=average \
        at_file=gap/train_500.xyz \
	    gap={distance_2b \
                cutoff=6.0 \
                covariance_type=ard_se \
                delta=1 \
                theta_uniform=1.0 \
                sparse_method=uniform \
                n_sparse=300 \
                Z1=18 Z2=18 :\
            soap \
                l_max=6 \
                n_max=6 \
                atom_sigma=0.5 \
                zeta=4 \
                cutoff=6.0 \
                cutoff_transition_width=0.5 \
                covariance_type=dot_product \
                n_sparse=300 \
                sparse_method=random \
                delta=1.0 \
                n_Z=1 Z={18}} \
	    gp_file=gap/SOAP_500.xml \
        default_sigma={0.003 0.15 0 0} \
        sparse_jitter=1.0e-10 \
        force_parameter_name=forces \
        energy_parameter_name=energy

"""

RERUN_GAP = False

# %% 
# Let's walk through the different options...( long long walkthrough )
# We execute our script with 

if RERUN_GAP:
    subprocess.run(gap_fit_cmd, cwd=str(PROJECT_PATH))

# %% 
# Next, we want to use the generated GAP potential to calculate the energies and forces. 


soap = Potential(param_filename=PROJECT_PATH/"gap"/"SOAP_500.xml")

def rms_dict(x_ref, x_pred):
    """ Takes two datasets of the same shape and returns a dictionary containing RMS error data"""

    x_ref = np.array(x_ref)
    x_pred = np.array(x_pred)

    if np.shape(x_pred) != np.shape(x_ref):
        raise ValueError('WARNING: not matching shapes in rms')

    error_2 = (x_ref - x_pred) ** 2

    average = np.sqrt(np.average(error_2))
    print(average)
    std_ = np.sqrt(np.var(error_2))

    return {'rmse': average, 'std': std_}

def energy_plot(in_file, ax, title='Plot of energy'):
    """ Plots the distribution of energy per atom on the output vs the input"""
    # read files
    in_frames = ase.io.read(in_file, ':')

    print(in_frames[0])
    print(f"number of frames {len(in_frames)}")
    print(f"position array has shape {in_frames[0].positions.shape}")
    print(f"{len(in_frames[0].get_chemical_symbols())}")
    # list energies
    ener_in = [frame.get_potential_energy() / len(frame.get_chemical_symbols()) for frame in in_frames]
    ener_out = []
    for frame in  in_frames:
        frame.set_calculator(soap)
        ener_out+=[frame.get_potential_energy() / len(frame.get_chemical_symbols())]
    #ener_out = [frame.get_potential_energy() / len(frame.get_chemical_symbols()) for frame in out_frames]
    # scatter plot of the data
    ax.scatter(ener_in, ener_out)
    # get the appropriate limits for the plot
    for_limits = np.array(ener_in +ener_out)
    elim = (for_limits.min() - 0.005, for_limits.max() + 0.005)
    ax.set_xlim(elim)
    ax.set_ylim(elim)
    # add line of slope 1 for refrence
    ax.plot(elim, elim, c='k')
    # set labels
    ax.set_ylabel('energy by GAP / eV')
    ax.set_xlabel('energy by CP2K / eV')
    #set title
    ax.set_title(title)
    # add text about RMSE
    _rms = rms_dict(ener_in, ener_out)
    rmse_text = 'RMSE:\n' + str(np.round(_rms['rmse'], 5)) + ' +- ' + str(np.round(_rms['std'], 5)) + 'eV/atom'
    rmse_text = f"RMSE: {_rms['rmse']:2e} +- {_rms['std']:2e} eV/atom"
    ax.text(0.9, 0.1, rmse_text, transform=ax.transAxes, fontsize='small', horizontalalignment='right',
            verticalalignment='bottom')

def force_plot(in_file, ax, symbol='HO', title='Plot of force'):
    """ Plots the distribution of firce components per atom on the output vs the input
        only plots for the given atom type(s)"""

    in_atoms = ase.io.read(in_file, ':')

    symbol=["Ar"]
    # extract data for only one species
    in_force, out_force = [], []
    for at_in in in_atoms:
        # get the symbols
        sym_all = at_in.get_chemical_symbols()
        # add force for each atom
        for j, sym in enumerate(sym_all):
            if sym in symbol:
                in_force.append(at_in.get_forces()[j]) 
        at_in.set_calculator(soap)
        for j, sym in enumerate(sym_all):
            if sym in symbol:
                out_force.append(at_in.get_forces()[j]) 
    print(len(in_force))
    print(in_force[0].shape)
    # convert to np arrays, much easier to work with
    in_force = np.array(in_force)
    out_force = np.array(out_force)
    in_force = np.sqrt(np.sum(in_force**2, axis=1))
    out_force = np.sqrt(np.sum(out_force**2, axis=1))
    print(in_force.shape)
    # scatter plot of the data
    ax.scatter(in_force, out_force)
    # get the appropriate limits for the plot
    #for_limits = np.array(in_force + out_force)
    #flim = (for_limits.min() - 1, for_limits.max() + 1)
    #ax.set_xlim(flim)
    #ax.set_ylim(flim)
    # add line of
    #ax.plot(flim, flim, c='k')
    # set labels
    ax.set_ylabel('force by GAP / (eV/Å)')
    ax.set_xlabel('force by CP2K / (eV/Å)')
    #set title
    ax.set_title(title)
    # add text about RMSE
    _rms = rms_dict(in_force, out_force)
    #rmse_text = 'RMSE:\n' + str(np.round(_rms['rmse'], 5)) + ' +- ' + str(np.round(_rms['std'], 5)) + 'eV/Å'
    rmse_text = f"RMSE: {_rms['rmse']:2e} +- {_rms['std']:2e} eV/A"
    ax.text(0.9, 0.1, rmse_text, transform=ax.transAxes, fontsize='small', horizontalalignment='right',
            verticalalignment='bottom')

fig, ax = plt.subplots(1, 1)
energy_plot("gap/test.xyz", ax, "Energy on training data")
fig.savefig("plots/energy_plot_500.png")


fig, ax = plt.subplots(1, 1)
force_plot("gap/test.xyz", ax, "Force on training data")
fig.savefig("plots/force_plot_500.png")

fig, ax = plt.subplots(1, 1)
energy_plot("gap/validate.xyz", ax, "Energy on validation data")
fig.savefig("plots/energy_plot_validate_500.png")


fig, ax = plt.subplots(1, 1)
force_plot("gap/validate.xyz", ax, "Force on validation data")
fig.savefig("plots/force_plot_validate_500.png")

