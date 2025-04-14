Getting started
***************

.. container:: abstract

    In the following we will use GAP (Gaussian Approximation Potential) implemented in QUIP (**Q**\uantum Mechanics and **I**\nteratomic **P**\otentials)
    to learn the energies and forces of liquid argon. 


.. admonition:: Requirements

     - an xyz file with the energies and forces of liquid argon
     - for example generated with CP2K (:ref:`liquid_argon_in_cp2k`)

Setting up our work environment
================================

.. container:: justify
    
    Open VSCode (or any other editor of your choice) and
    create the following folder structure
    
.. code-block::
    :dedent: 0 

    |   your-project
    |   |---dft
    |   |   |---2_body_potential
    |   |   |---liquid_argon_85K
    |   |   |   |---Argon_Simulation-pos-1.xyz
    |   |   |   |---Argon_Simulation-frc-1.xyz
    |   |---gap
    |   |   |---cut_off_4A
    
.. container:: justify
    
    In the following we will work with a Jupyter notebook. Todo so, go to the next page :ref:`preprocess_dft` and download the ipynb notebook from the end of the page.
    Place the notebook into your folder ``gap/``, then continue with doing the tutorial :ref:`preprocess_dft`.




