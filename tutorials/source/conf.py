# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
sys.path.append(".")
import cp2klexer
from sphinx.highlighting import lexers
from pygments_lammps import LAMMPSLexer

def setup(app):
    app.add_lexer("lammps", LAMMPSLexer)

project = 'Machine Learning of Atomic Interactions'
copyright = '2025, IPFM'
author = 'Kira Fischer, Richard Schömig and Alexander Schlaich, IPFM'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_gallery.gen_gallery"]

sphinx_gallery_conf = {
     'examples_dirs': 'examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path to where to save gallery generated output
     'example_extensions': {'.py', '.in', '.sh'}
}

templates_path = ['_templates']
exclude_patterns = ["examples/GALLERY_HEADER.rst"]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
pygments_style = "sphinx"


lexers["cp2k"] = cp2klexer.CP2KLexer(startinline=True)
