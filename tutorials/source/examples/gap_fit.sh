# Fitting GAP 
# ===========
#
# In this tutorial, you will learn to write a bash-script that fits GAP on your DFT data.
# GAP learns the energies and forces as a function of the atomic positions. 
# It is implemented as a command line tool ``gap_fit``
# which takes many parameters. 
# The parameters are specified in the following, and then passed to ``gap_fit``

# %%
# First, we define our parameters which we want to vary later
# In this case, that's the Cut-off of the atomic neighborhood,
# the output file and the input file.

CUT_OFF=4.0
GAP_FILE=cut_off_4A/SOAP.xml
INPUT_FILE=train.xyz

# %% 
# Next, we have the parameters for GAP. 
GAP_PARAMS=(
# %% 
# First, we have the parameters for the 2 body distance descriptor
distance_2b
cutoff=$CUT_OFF
covariance_type=ard_se
delta=1
theta_uniform=1.0
sparse_method=uniform
n_sparse=300
Z1=18
Z2=18 :
# %% 
# Then we have the parameters for the SOAP descriptor
soap 
# %% 
# ``n_max`` and ``l_max`` is the order of expansion in spherical harmonics
l_max=6
n_max=6
# %%
# ``atom_sigma`` is the smearing of the atomic position
atom_sigma=0.5
zeta=4
# %% 
# Then we specify the cut-off for the neighborhood around the centered atom
cutoff=$CUT_OFF
cutoff_transition_width=0.5
# %%
# and some magic settings
covariance_type=dot_product
n_sparse=300
sparse_method=random
delta=1.0
# %% 
# Finally, we specify the number of different species and the atomic charge number of the species
n_Z=1 Z={18}

)

# %% 
# Next, we have some general parameters
GEN_PARAMS=(
e0_method=average 
gap={"${GAP_PARAMS[@]}"}
# %% 
# Here we specify the input file (the atomic coordinates and forces) and the output file (the machine learned potential)
at_file=$INPUT_FILE
gp_file=$GAP_FILE 
default_sigma={0.003 0.15 0 0}
sparse_jitter=1.0e-10
# %% 
# and then we have some parsing options for the input file
force_parameter_name=forces
energy_parameter_name=energy
)

# %% 
# Finally, we print our parameters and then run the gap_fit command
echo ${GEN_PARAMS[@]}

gap_fit "${GEN_PARAMS[@]}"

# %%
# To run this script open the terminal, navigate to the folder ``your_project/gap`` 
# and execute the command ``bash gap_fit.sh``. 
