Machine learning atomic interactions with GAP
*********************************************

.. container:: abstract

    In the following we will use GAP (Gaussian Approximation Potential) implemented in QUIP (QUantum mechanics and Interatomic Potentials)
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

    In the following we will work with a Jupyter notebook. To do so, go into your folder `gap` and type 

.. code-block:: bash
    :dedent: 0

    jupyter notebook

.. container:: justify
    
    Now, the jupyter notebook editor opens in your browser. This is where we will work. 
    Continue now with preprocessing DFT data. :ref:`preprocess_dft`


    
Preprocessing DFT data
======================

.. container:: justify

    First, we need to convert our simulation data to be

Fitting a potential with GAP
============================

.. container:: justify

    Once we have generated train, test and validation data sets, we can start training our model
    To do so, we first import quip and ase as

.. code-block::
   :dedent: 0

   import quip
   import ase


Evaluating the fit
==================


