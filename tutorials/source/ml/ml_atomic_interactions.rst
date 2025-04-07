Getting started
***************

.. container:: abstract

    In the following we will use GAP (Gaussian Approximation Potential) implemented in QUIP (**Q**\uantum Mechanics and **I**\nteratomic **P**\otentials)
    to learn the energies and forces of liquid argon. 


.. admonition:: Requirements

     - an xyz file with the energies and forces of liquid argon
     - for example generated with CP2K (:ref: `liquid_argon_cp2k`)

Setting up our work environment
================================

.. container:: justify
    
    Create the following folder structure
    
.. code-block::
    :dedent: 0 

    |   your-project
    |   |---dft
    |   |   |---Argon_Simulation-pos.xyz
    |   |   |---Argon_Simulation-frc.xyz
    |   |---gap
    
.. container:: justify

    In the following we will work with a Jupyter notebook. To do so, go into your folder ``gap`` and type 

.. code-block:: bash
    :dedent: 0

    jupyter notebook

.. container:: justify
    
    Now, the jupyter notebook editor opens in your browser. This is where we will work. 
    Continue now with :ref:`preprocess_dft`.



