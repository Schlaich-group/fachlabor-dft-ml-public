# Simulation of Argon 
# ===================
#
# This is a description 

#############################
### Configure system type ###
#############################

# use mass in grams/mole, distance in Angstroms, time in picoseconds, energy in eV and so on
units           metal
# apply periodic boundary conditions (PBCs) in x-, y-, and z-direction
boundary        p p p
# define the per-atom attributes tag, type, x, v, f, image, mask
atom_style      atomic

# %% Sphinx code block 
#
#
################################
### Define system parameters ###
################################

region          myRegion block 0 17.0742 0 17.0742 0 17.0742
create_box      1        myRegion

##############################################################
### Read input file and assign types and elementary groups ###
##############################################################

labelmap		atom      1      Ar
read_dump       argon.xyz 0      x    y      z box no add yes format xyz
set		        atom      1*108  type 1
mass            1         39.948
group           Ar        type   1
velocity        all       create 900  132465

#######################################
### Read a restart file if required ###
#######################################

# read_restart    Ar_1.restart

########################################
### Define forcefield for simulation ###
########################################

pair_style      quip
pair_coeff      * * ../gap/SOAP_500.xml "Potential xml_label=GAP_2025_2_21_60_23_19_51_451" 18

####################
### Set Timestep ###
####################

timestep        0.001

###########################################
### Define thermostat or other ensemble ###
###########################################
# minimize 1.0e-4 1.0e-6 100 1000 <-- geometry optimization

fix             myThermostat all nvt temp 85.0 85.0 $(50*dt)

#################################
### Compute system parameters ###
#################################

compute         myTemp all temp

##########################
#### Define dump files ###
##########################

dump            myDump1 all     custom  100 Ar_full.lammpstraj id                  type element x y z vx vy vz fx fy fz
dump_modify     myDump1 element Ar
dump_modify     myDump1 sort    id
# dump_modify     myDump1 append  yes

dump            myDump2         all     xyz 10                 Ar_Trajectories.xyz
dump_modify     myDump2         element Ar
# dump_modify     myDump2         append  yes

log             log.argon       append

################################
### Define restart file dump ###
################################

restart		1000 Ar_1.restart A_2.restart

#################################################################
### Define thermo output for log dump and run the simulations ###
#################################################################

thermo          1
thermo_style    custom step time temp density press
run             100000
