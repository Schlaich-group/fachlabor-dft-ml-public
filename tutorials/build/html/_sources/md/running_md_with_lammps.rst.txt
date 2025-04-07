.. _lammps_with_gap:

Molecular Dynamics with LAMMPS interfaced to QUIP
*************************************************

.. container:: abstract

    In the following we will use LAMMPS (**L**\arge-scale **A**\tomic/**M**\olecular **M**\assively **P**\arallel **S**\imulator)
    interfaced with QUIP, which you know from the previous tutorial, to run a molecular dynamics simulation.

.. admonition:: Requirements

    - Trained GAP model (from last tutorial)
    - QUIP (preinstalled)
    - LAMMPS binary (preinstalled)


Brief introduction into LAMMPS
==============================

.. container:: justify

   LAMMPS is a powerful, open-source molecular dynamics (MD) software package used to simulate atomic,
   molecular, and solid-state systems. It is highly scalable, running efficiently on single workstations
   as well as on supercomputers with hundreds of processors. Due to its modular design, LAMMPS can be
   easily extended with new features and capabilities, making it suitable for a wide range of
   applications in materials science, chemistry, and biology.

Input preparation
=================

.. container:: justify

   Even though LAMMPS only requires one input file, it is common to split the input into several files
   for better organization and readability. 

   These three main types of files used in LAMMPS are:

   - **input script**: Actual input file, which is a text file containing LAMMPS commands that define the
     simulation parameters and protocols, such as the time step, thermostat, simulation time and other settings.
   - **data file**: Contains the initial configuration of the system, including atomic positions, types,
     and other properties.
   - **potential file**: Specifies the interatomic potential to be used in the simulation, which can be
     a pre-defined potential or a custom one.

   The latter two are then imported into the input script.
   In this tutorial, we will use a GAP model as the interatomic potential, which we trained in the
   previous tutorial, so no potential file is needed.
   We also do not need a data file, as the setup is rather simple and we will therefore generate the initial
   configuration directly in the input script.
   So the only file we need to prepare is the input script.
   In the "md" directory, you will find an almost finished version of it as "Ar.in":

.. code-block::
    :dedent: 0 

    |   your-project
    |   |---dft
    |   |---gap
    |   |---md
    |   |   |---Ar.in
   
.. container:: justify 
   
   It is designed to guide users who are new to LAMMPS through their first simulation.
   Next to the commands, you will find some information which either briefly explain what is done at this point or 
   give some hints.  It is a good praxis to also check out the official LAMMPS documentation, which provides more
   in-depth information and examples of each command. It can be found here
   `here <https://docs.lammps.org/Manual.html>`_. The best entry is probably the section about the
   `LAMMPS input script language <https://docs.lammps.org/Commands_input.html>`_.

.. container:: justify 
   
   First, we want to set some general parameters as the unit system being used throughout
   the input script and output files.
   We will use the "metal" unit system, which is mostly used for metallic systems. It defines e.g. the
   following units:
   - energy in eV
   - mass in grams/mole
   - distance in Angstroms
   - time in picoseconds
   - temperature in Kelvin
   
   Periodic boundary conditions (PBCs) are applied in x-, y-, and z-direction. An atom style is set,
   which defines which attributes are associated with every atoms. In this case, we use the "atomic" style,
   meaning that every atom has a tag, type, x, v, f, image, mask.

.. code-block:: lammps
    :dedent: 0 

    units           metal 
    boundary        p p p
    atom_style      atomic


.. container:: justify

   Next, we build our simulation box. We will use a cubic box with a size of 17.0742 Angstroms in each direction.
   Therefore we define a region called "myRegion" and then create a box by setting the number of atom types
   to 1 (in this case, we only have one type of atom, which is Argon) and assigning it to the region we just created.

.. code-block:: lammps
    :dedent: 0 

    region          myRegion block 0 17.0742 0 17.0742 0 17.0742
    create_box      1 myRegion


.. container:: justify

    Now we can start populating our simulation box with atoms.
    We will read in the file "argon.xyz" that contains the coordinates of the atoms, and assign types, masses, a group ("Ar") and velocities to them.
    LAMMPS does not know about elements as defined in the periodic table, so we need to define all relevant attributes of our atoms by ourselves.

.. code-block:: lammps
    :dedent: 0 

    read_dump       argon.xyz 0      x    y      z box no add yes format xyz
    set		        atom      1*108  type 1
    mass            1         39.948
    group           Ar        type   1
    velocity        all       create 900  132465

.. container:: justify

    In this section, we will define the potential that will be used in the simulation.
    Without a potential, LAMMPS wouldn't not know how to calculate the forces acting on the atoms.
    We will use the pair_style quip command, which interaces to our machine learned potential (MLP) model that was trained on DFT data.
    We also need to tell LAMMPS that the potentials should be used for all possible atom pairs. This is done using the asterisk (*) twice, which means
    that we consider the interaction of all atom types with each other followed bt the path to the MLP file.

.. code-block:: lammps
    :dedent: 0 

    pair_style      quip
    pair_coeff      * * ../gap/SOAP_500.xml "Potential xml_label=GAP_2025_2_21_60_23_19_51_451" 18


.. container:: justify

    Next, we set the time step for the simulation. The time step is the interval at which the positions and velocities of the atoms are updated by 
    integration Newton's equation of motion. It is important to choose a timestep that is small enough to accurately capture the dynamics of the system
    (especially the fast hydrogen vibrations!), but not so small that it slows down the simulation unnecessarily.
    We will use a time step of 0.001 picoseconds (ps) = 1 femtoseconds (fs), which is a common choice for MD simulations.

.. admonition:: Caution

    Watch out which unit system your are using!


.. code-block:: lammps
    :dedent: 0 

    timestep        0.001

.. container:: justify

    To correctly sample the NVT (= number of particles, volume and temperature are constant), we need to apply a thermostat
    to the system's particles, which is achieved by a "fix".

.. admonition:: Info

    In LAMMPs' language a "fix" does not literally mean that e.g. an atom is fixed in space, it's rather an operation that is applied during the
    simulation.


.. code-block:: lammps
    :dedent: 0

    fix             myThermostat all nvt temp 85.0 85.0 $(50*dt)


.. container:: justify

    If we want to retrieve an observable that changes during the simulation, e.g. the temperature of the system, we need to
    define a compute command.


.. code-block:: lammps
    :dedent: 0 

    compute         myTemp all temp



.. container:: justify

    The dump command is used to output data from the simulation.
    The data can be written to a file in different formats, such as xyz, custom, or atom.

.. code-block:: lammps
    :dedent: 0 

    dump            myDump1 all     custom  100 Ar_full.lammpstraj id                  type element x y z vx vy vz fx fy fz
    dump_modify     myDump1 element Ar
    dump_modify     myDump1 sort    id
    # dump_modify     myDump1 append  yes
 
    dump            myDump2         all     xyz 10                 Ar_Trajectories.xyz
    dump_modify     myDump2         element Ar
    # dump_modify     myDump2         append  yes
 
    log             log.argon       append



.. container:: justify

    It considered good practice to write restart files during the simulation.
    Restart files are used to save the current state of the simulation, allowing you to pause and resume the simulation later.
    This is especially useful for long simulations, where you might want to save the state periodically in case of a crash or other issues.
    They can also be used to analyze the simulation at different points in time or to continue the simulation from a specific point.
    In this case, we will write restart files every 1000 steps.
    LAMMPS will toggle between the two files defined and overwrite each every other time.

.. code-block:: lammps
    :dedent: 0 

    restart		1000 Ar_1.restart A_2.restart


.. container:: justify

    Finally, we need to define the output frequency of the simulation.
    The thermo command specifies how often LAMMPS will print thermodynamic information to the screen or log file.
    In this case, we set it to 1, meaning that LAMMPS will print the information every time step.
    The thermo_style command specifies the format of the output. In this case, we want to see the step number, time, temperature, density and pressure.
    The run command specifies the number of time steps to run the simulation. In this case, we set it to 100000, which corresponds to 100 ps.

.. code-block:: lammps
    :dedent: 0 

    thermo          1
    thermo_style    custom step time temp density press
    run             100000

Running the simulation
======================

.. container:: justify

    Now its time to run the simulation. To exploit the full power of out notebook, we will run LAMMPS in parallel 
    on all available cores of our machine. This is done using the mpirun command, which is a part of the MPI
    (Message Passing Interface) library. The -np flag specifies the number of processes to run in parallel.
    In this case, we set it to 32, meaning that LAMMPS will use 32 processes.

.. code-block:: bash
    :dedent: 0 

    mpirun -np 32 lmp_mpi -in Ar.in


    include:: ../auto_examples/plot_rdf.rst
