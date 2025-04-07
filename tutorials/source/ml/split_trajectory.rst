Splitting the trajectory
========================

.. container:: abstract
        
    Next, we split ``trajectory.xyz`` into a ``train.xyz``, ``validate.xyz`` and ``test.xyz`` data set.


.. container:: justify
    
    Think of a way to split your DFT trajectory into a training, validation and test data set. 
    We recommend a trajectory length of 500 frames for each data set.
    Furthermore, the first 100 frames of the trajectory should not be used. These frames are outliers,
    as the simulated system is not well equilibrated yet (it has physically unlikely configurations).
    
.. admonition:: Do it yourself

    Split the trajectory into a ``train.xyz``, ``validate.xyz`` and ``test.xyz`` data set.
