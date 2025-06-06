
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "auto_examples/Ar.in.sh"
.. LINE NUMBERS ARE GIVEN BELOW.

.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        :ref:`Go to the end <sphx_glr_download_auto_examples_Ar.in.sh>`
        to download the full example code.

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_Ar.in.sh:

Simulation of Argon 
===================

This is a description 

.. GENERATED FROM PYTHON SOURCE LINES 6-7

## Configure system type ###

.. GENERATED FROM PYTHON SOURCE LINES 9-15

.. code-block:: Bash

    # use mass in grams/mole, distance in Angstroms, time in picoseconds, energy in eV and so on
    units           metal
    # apply periodic boundary conditions (PBCs) in x-, y-, and z-direction
    boundary        p p p
    # define the per-atom attributes tag, type, x, v, f, image, mask
    atom_style      atomic

.. GENERATED FROM PYTHON SOURCE LINES 15-21

Sphinx code block
-----------------



## Define system parameters ###

.. GENERATED FROM PYTHON SOURCE LINES 23-25

.. code-block:: Bash

    region          myRegion block 0 17.0742 0 17.0742 0 17.0742
    create_box      1        myRegion

.. GENERATED FROM PYTHON SOURCE LINES 27-28

## Read input file and assign types and elementary groups ###

.. GENERATED FROM PYTHON SOURCE LINES 30-36

.. code-block:: Bash

    labelmap		atom      1      Ar
    read_dump       argon.xyz 0      x    y      z box no add yes format xyz
    set		        atom      1*108  type 1
    mass            1         39.948
    group           Ar        type   1
    velocity        all       create 900  132465

.. GENERATED FROM PYTHON SOURCE LINES 38-39

## Read a restart file if required ###

.. GENERATED FROM PYTHON SOURCE LINES 41-42

.. code-block:: Bash

    # read_restart    Ar_1.restart

.. GENERATED FROM PYTHON SOURCE LINES 44-45

## Define forcefield for simulation ###

.. GENERATED FROM PYTHON SOURCE LINES 47-49

.. code-block:: Bash

    pair_style      quip
    pair_coeff      * * ../gap/SOAP_500.xml "Potential xml_label=GAP_2025_2_21_60_23_19_51_451" 18

.. GENERATED FROM PYTHON SOURCE LINES 51-52

## Set Timestep ###

.. GENERATED FROM PYTHON SOURCE LINES 54-55

.. code-block:: Bash

    timestep        0.001

.. GENERATED FROM PYTHON SOURCE LINES 57-59

## Define thermostat or other ensemble ###
minimize 1.0e-4 1.0e-6 100 1000 <-- geometry optimization

.. GENERATED FROM PYTHON SOURCE LINES 61-62

.. code-block:: Bash

    fix             myThermostat all nvt temp 85.0 85.0 $(50*dt)

.. GENERATED FROM PYTHON SOURCE LINES 64-65

## Compute system parameters ###

.. GENERATED FROM PYTHON SOURCE LINES 67-68

.. code-block:: Bash

    compute         myTemp all temp

.. GENERATED FROM PYTHON SOURCE LINES 70-71

### Define dump files ###

.. GENERATED FROM PYTHON SOURCE LINES 73-83

.. code-block:: Bash

    dump            myDump1 all     custom  100 Ar_full.lammpstraj id                  type element x y z vx vy vz fx fy fz
    dump_modify     myDump1 element Ar
    dump_modify     myDump1 sort    id
    # dump_modify     myDump1 append  yes

    dump            myDump2         all     xyz 10                 Ar_Trajectories.xyz
    dump_modify     myDump2         element Ar
    # dump_modify     myDump2         append  yes

    log             log.argon       append

.. GENERATED FROM PYTHON SOURCE LINES 85-86

## Define restart file dump ###

.. GENERATED FROM PYTHON SOURCE LINES 88-89

.. code-block:: Bash

    restart		1000 Ar_1.restart A_2.restart

.. GENERATED FROM PYTHON SOURCE LINES 91-92

## Define thermo output for log dump and run the simulations ###

.. GENERATED FROM PYTHON SOURCE LINES 93-95

.. code-block:: Bash

    thermo          1
    thermo_style    custom step time temp density press
    run             100000

.. _sphx_glr_download_auto_examples_Ar.in.sh:

.. only:: html

  .. container:: sphx-glr-footer sphx-glr-footer-example

    .. container:: sphx-glr-download sphx-glr-download-python

      :download:`Download Bash source code: Ar.in.sh <Ar.in.sh>`

    .. container:: sphx-glr-download sphx-glr-download-zip

      :download:`Download zipped: Ar.in.zip <Ar.in.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
