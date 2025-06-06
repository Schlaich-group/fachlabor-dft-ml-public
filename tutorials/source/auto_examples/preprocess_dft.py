#!/usr/bin/python

""".. _preprocess_dft:

Preprocessing DFT Data
======================

In this tutorial we will preprocess our DFT data. CP2K generates data with units in `Hartree` and `Hartree/Bohr`
but GAP takes data in units of `eV` and `eV/Å`.
Furthermore, GAP uses slightly different labelling from CP2K. That's why we need to preprocess

We start with importing our python modules. We use tqdm to show a nice progress bar and pint to do unit conversions
"""
from pathlib import Path
from tqdm import tqdm
import pint
ureg = pint.UnitRegistry()

# %%
# Then we set our project path. Replace this with your own project path
PROJECT_PATH = Path("../../../solutions")

# %%
# Now, we define our conversion constants
HARTREE_BOHR_TO_EVOLT_ANGSTROM = (1 * ureg.hartree / ureg.bohr).to(ureg.e * ureg.volt / ureg.angstrom).magnitude 
HARTREE_TO_EVOLT = (1 * ureg.hartree).to(ureg.e * ureg.volt).magnitude

# %% 
# Next, we have our converter. You don't have to read the whole function, just take a look at the parameters the function takes as an input. 

def _xyz_to_extxyz(
    outfile="Dataset", positions=None, forces=None, pressure=None, lattice=None
):
    """
    Convert xyz files to extxyz files
    The most efficient text based file input for ASE is the extended xyz format.

    kwargs:
        outfile (str) -- name of the output file
        positions (str) -- file path of the positions file
        forces (str) -- file path to the forces file
        virials (str) -- file path to the virials file
        box (list) -- Box array
    """
    FORCE_FACTOR = HARTREE_BOHR_TO_EVOLT_ANGSTROM # 51.4220670719
    ENERGY_FACTOR = HARTREE_TO_EVOLT  # 27.21138602

    print(f"the force factor is {FORCE_FACTOR}")
    print(f"the energy factor is {ENERGY_FACTOR}")

    def _header_line(obj, box, index, energy, time, conversion=True):
        """Function to print the header line
        The header line in the extxyz format is somewhat complicated. For this reason,
        we use a separate function to generate this line during each iteration in the
        sampling function. This function will write directly to the given file object,
        it will not return a string to be written.
        args:
            obj (object) -- file object to write to
            lattice (array) -- a lattice describing the cell
            index (str) -- the configuration number
            energy (str) -- energy of the system
            time (str) -- time given in the configuration
        kwargs:
            conversion (bool) -- Most cp2k outputs here will be in Hartree.
            This will convert it to eV
        """

        if conversion:
            energy = float(energy) * ENERGY_FACTOR

        # Calculate the properties string
        if forces is not None and pressure is not None:
            properties_string = "species:S:1:pos:R:3:forces:R:3:virials:R:3"
        elif forces is not None and pressure is None:
            properties_string = "species:S:1:pos:R:3:forces:R:3"
        elif forces is None and pressure is not None:
            properties_string = "species:S:1:pos:R:3:virials:R:3"
        else:
            properties_string = "species:S:1:pos:R:3"

        obj.write(
            f'Lattice="{box[0][0]} {box[0][1]} {box[0][2]}'
            f" {box[1][0]} {box[1][1]} {box[1][2]}"
            f' {box[2][0]} {box[2][1]} {box[2][2]}"'
            f" Properties={properties_string}"
            f" cutoff=-1.0 energy={energy} nneightol=0.0 i={index}"
            f' pbc="T T T" time={time}\n'
        )

    def _read_file(filename):
        """read a file into memory"""
        data = []
        with open(filename) as f_obj:
            for line in f_obj:
                data.append(line.split())

        return data

    def _get_system_properties():
        """Characterize the system"""

        with open(positions) as f:
            COMMENT_LINE = [next(f).split() for _ in range(2)]
            number_of_atoms = int(COMMENT_LINE[0][0])

        with open(positions) as f:
            number_of_lines = sum(1 for line in f)

        number_of_configurations = number_of_lines / (number_of_atoms + 2)

        if forces is not None and pressure is not None:
            properties = [positions, forces, pressure]
        elif forces is not None and pressure is None:
            properties = [positions, forces]
        elif forces is None and pressure is not None:
            properties = [positions, pressure]
        else:
            properties = [positions]

        return number_of_atoms, number_of_configurations, properties

    number_of_atoms, number_of_configurations, properties = _get_system_properties()
    data_arrays = []
    for item in properties:
        data_arrays.append(_read_file(item))

    start = 0
    stop = number_of_configurations
    step = number_of_atoms + 2
    with open(f"{outfile}.xyz", "w") as f:
        for i in tqdm(range(int(start), int(stop))):
            f.write(f"{number_of_atoms}\n")
            _header_line(
                f,
                lattice,
                data_arrays[0][1 + i * step][2],
                data_arrays[0][1 + i * step][8],
                data_arrays[0][1 + i * step][5],
            )
            for j in range(2 + i * step, number_of_atoms + i * step + 2):
                for k in range(len(data_arrays)):
                    if k == 0:
                        f.write(
                            f"{data_arrays[k][j][0]:<2}    "
                            f"{float(data_arrays[k][j][1]):>14.10f}    "
                            f"{float(data_arrays[k][j][2]):>14.10f}    "
                            f"{float(data_arrays[k][j][3]):>14.10f}    "
                        )
                    else:
                        f.write(
                            f"{float(data_arrays[k][j][1]) * FORCE_FACTOR:>14.10f}    "
                            f"{float(data_arrays[k][j][2]) * FORCE_FACTOR:>14.10f}    "
                            f"{float(data_arrays[k][j][3]) * FORCE_FACTOR:>14.10f}    "
                        )
                f.write("\n")

# %%
# We now call the converter on our DFT files.

_xyz_to_extxyz(
    outfile=PROJECT_PATH / "gap/trajectory",
    positions=PROJECT_PATH / "dft/liquid_argon_85K/Argon_Simulation-pos-1.xyz",
    forces=PROJECT_PATH / "dft/liquid_argon_85K/Argon_Simulation-frc-1.xyz",
    lattice=[[17.0742, 0, 0],
             [0, 17.0742, 0],
             [0, 0, 17.0742]])

# %%
# The converted file can be found in ``gap/data/trajectory.xyz``
