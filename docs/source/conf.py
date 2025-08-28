import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))  # путь к твоему пакету

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'public_webhooks_server_acceptor_python'
copyright = '2025, Arbitragescanner'
author = 'Arbitragescanner'
release = '1.0'

autodoc_mock_imports = ["src"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",        # Google/NumPy style docstrings
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']



