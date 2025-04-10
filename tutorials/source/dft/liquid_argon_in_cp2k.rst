.. _liquid_argon_in_cp2k:

Liquid argon with CP2K 
*********************************

.. container:: abstract

    In this tutorial, we learn how to simulate liquid argon with CP2K and using Born-Oppenheimer ab-initio MD.
   

Getting started
===============

.. container:: justify 

    To run a simulation in CP2K, one needs to provide CP2K with an input script and a starting configuration :download:`system.xyz <./system.xyz>`.

.. container:: justify

    Go into your folder ``dft/liquid_argon_85K``, and place :download:`system.xyz <./system.xyz>` in it. 
    Then create a blank text file in your folder called ``Argon_Simulation.inp``. 
    Copy the following lines in the ``Argon_Simulation.inp``, where a line starting with 
    a hash symbol (#) is a comment ignored by CP2K:

.. code-block:: cp2k
   :dedent: 0

    # Name of the project
    @SET PROJ_NAME Argon_Simulation

    # Set global properties
    &GLOBAL
        PROJECT ${PROJ_NAME}
        
        # Fast Fourier transform settings
        PREFERRED_FFT_LIBRARY FFTW
        FFTW_PLAN_TYPE MEASURE

        # Set type of the run.
        RUN_TYPE MD

        PRINT_LEVEL LOW
        WALLTIME 172000
    &END GLOBAL

.. container:: justify

    Here we set the global properties. 
    First we set the project name. 
    Then FFT specifies our settings for performing fast fourier transformations.
    Finally, we set the run type to molecular dynamics. 

    
Force Calculation with DFT
==========================

.. container:: justify

    Next, we specify our settings for the force and energy calculation using DFT.
    Start with the following two lines

.. code-block:: cp2k
   :dedent: 0

    # Parameters for force calculation.
    &FORCE_EVAL
        # Define the DFT parameters
        &DFT

.. container:: justify

    Next, we need to specify a basis set and a potential. First, place the files in :download:`BASIS_MOLOPT` and :download:`GTH_POTENTIALS` to your directory ``dft/liquid_argon_85K``. Then we import our files by specifying the following in ``Argon_Simulation.inp``

.. code-block:: cp2k
    :dedent: 0
            
            BASIS_SET_FILE_NAME BASIS_MOLOPT
            POTENTIAL_FILE_NAME GTH_POTENTIALS

.. admonition:: About basis sets
    :class: info

    A basis set is a set of functions that is used to represent the electronic wave function.

.. admonition:: About pseudopotentials
    :class: info 

    The pseudopotential is used as an approximation of the nucleus-valence electron and core electron-valence electron interaction.


.. container:: justify

    Next, we have a whole bunch of parameters for our calculation

.. code-block:: cp2k
    :dedent: 0

            # Multi-grid information
            &MGRID
                CUTOFF 600
                NGRIDS 5
            &END MGRID
            &SCF
                # Use a restart to guess wave-function.
                SCF_GUESS RESTART
                MAX_SCF 30
                EPS_SCF 1.0E-6
                # Orbital transformation scheme
                &OT
                    MINIMIZER DIIS
                    PRECONDITIONER FULL_SINGLE_INVERSE
                &END OT
                &OUTER_SCF
                    MAX_SCF 100
                    EPS_SCF 1.0E-6
                &END OUTER_SCF
                # Print options for SCF information -- need for restart files
                &PRINT
                    # Dump restart files
                    &RESTART
                        ADD_LAST NUMERIC
                        &EACH
                            QS_SCF 0
                        &END EACH
                    &END RESTART
                &END PRINT
            &END SCF

.. container:: justify

   Then, we specify our exchange-correlation functional, and set it to the Perdew-Burke-Ernzerhof functional (PBE)

.. code-block:: cp2k
    :dedent: 0

            # Define XC functional parameters
            &XC
              &XC_FUNCTIONAL PBE
              &END XC_FUNCTIONAL
            &END XC

.. admonition:: About exchange correlation functionals
   :class: info

   The exchange correlation functional approximates the electronic exchange and correlation energy from the electron density. 


.. container:: justify

   Finally, we close our section of the DFT settings using

.. code-block:: cp2k
    :dedent: 0
    
        &END DFT

System definition
------------------

.. container:: justify

    Next, we need to tell CP2K what kind of system we are simulating. 
    Start your system section with 

.. code-block:: cp2k
    :dedent: 0

        &SUBSYS

.. container:: justify 

   Then we add our topology information, like coordinates and system size.

   First, we need to provide CP2K with a starting configuration. Todo so copy ``resources/argon.xyz`` to your directory ``dft/liquid_argon_85K``. 
   Take a look into the file. The first line in the xyz format specifies the number of atoms. The following lines set the name and coordinates for each atom. You can also visualize ``argon.xyz`` with *vmd*. This is our starting configuration. 

   We now tell CP2K to use this file

.. code-block:: cp2k
    :dedent: 0

            &TOPOLOGY
                # Starting configuration.
                COORD_FILE_NAME argon.xyz
                COORD_FILE_FORMAT XYZ
                &GENERATE
                &END GENERATE
            &END TOPOLOGY

.. container:: justify

    Next, we set the size of the simulation box using

.. code-block:: cp2k
    :dedent: 0

            &CELL
                # Cubic box.
                ABC [angstrom] 17.0742 17.0742 17.0742
            &END CELL

.. container:: justify

    Finally, we tell CP2K which basis set and potential to use for our Argon atoms (Ar)


.. code-block:: cp2k
    :dedent: 0

            &KIND Ar
                # Basis set -- discuss this.
                BASIS_SET DZVP-MOLOPT-SR-GTH
                # Pseudo-potential --  discuss this.
                POTENTIAL GTH-PBE-q8
            &END KIND


.. container:: justify

    Last but not least, we close our system definition and the force calculation sections with

.. code-block:: cp2k
    :dedent: 0

        &END SUBSYS
    &END FORCE_EVAL


Molecular dynamics
==================

.. container:: justify
    
    Now, we want to move our nuclei according to the forces obtained from DFT.

    We start our motion and md section with

.. code-block:: cp2k
    :dedent: 0 

    &MOTION
        &MD

.. container:: justify
    
    Then we set our ensemble to NVT (constant number of particles N, constant volume V and constant temperature T)

.. code-block:: cp2k
    :dedent: 0

            ENSEMBLE NVT

.. container:: justify

    Next, we set our number of timesteps and the timestep

.. code-block:: cp2k
    :dedent: 0 
            
            STEPS 5000
            TIMESTEP 10.0   #femtoseconds

.. container:: justify

    And specify our temperature

.. code-block:: cp2k
    :dedent: 0 

            TEMPERATURE 85  #Kelvin

.. container:: justify
    
    In order to run a simulation at a constant temperature, we need a thermostat. A thermostat changes the particle velocities during the simulation to keep the temperature constant. Here, we use the Nose-Hoover thermostat

.. code-block:: cp2k
    :dedent: 0 
    
            # Nose-Hoover thermostat
            &THERMOSTAT
                TYPE NOSE
                REGION MASSIVE
                &NOSE
                    TIMECON [fs] 100
                &END NOSE
            &END THERMOSTAT

.. container:: justify

    Next, we tell CP2K to print the output and restart file if walltime is reached or the command gets an external EXIT command.

.. code-block:: cp2k
    :dedent: 0

            &PRINT
                FORCE_LAST
            &END PRINT

.. container:: justify
    
    and finally, we close the MD section with

.. code-block:: cp2k
    :dedent: 0

    &END MD

Writing coordinates and forces
------------------------------

.. container:: justify

    Now, we tell CP2K which information to write to an output file using &PRINT. We tell CP2K to write out the coordinates, velocities and forces. We also tell CP2K to write a restart file every step. 

.. code-block:: cp2k
    :dedent: 0

            # Define print statements
        &PRINT
            &TRAJECTORY
            &END TRAJECTORY
            &VELOCITIES
            &END VELOCITIES
            &FORCES
            &END FORCES
            # Dump a restart file every step.
            &RESTART
                ADD_LAST NUMERIC
                &EACH
                    MD 1
                &END EACH
            &END RESTART
        &END PRINT

.. container:: justify

    Finally, we close our motion section with 

.. code-block:: cp2k
    :dedent: 0

    &END MOTION


Running your simulation 
=======================

.. container:: justify

    You've made it! Your input file ``Argon_Simulation.inp`` is now complete!

    You can run the simulation using

.. code-block:: bash
    :dedent: 0

    cp2k.sopt -i Argon_Simulation.inp


.. container:: justify

    Here ``-i`` specifies the input file. You will get 4 files

    * ``Argon_Simulation-pos.xyz`` with the atomic coordinates
    * ``Argon_Simulation-frc.xyz`` with the force on each atom
    * ``Argon_Simulation-vel.xyz`` with the velocity on each atom
    * ``Argon_Simulation-n.restart`` which is a restart file for the simulation
