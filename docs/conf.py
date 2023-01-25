# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BioSim January Block 2023'
copyright = '2023, Navneet Sharma and Sushant Kumar Srivastava'
author = 'Navneet Sharma and Sushant Kumar Srivastava'
release = '0.0.1'
version = '0.0.1'

import os
import sys
import re

sys.path.insert(0, os.path.abspath('../src'))
autoclass_content = 'both'
latex_elements = {'papersize': 'a4paper'}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

sphinx_gallery_conf = {
    'doc_module': 'bsl',
    'reference_url': dict(bsl=None),
    'examples_dirs': '../examples',
    'gallery_dirs': '../Exam/sample.gif',
    'plot_gallery': 'True',  # Avoid annoying Unicode/bool default warning
    'remove_config_comments': True,
    'abort_on_example_error': False,
    'filename_pattern': re.escape(os.sep),
    'line_numbers': False,
    'download_all_examples': True,
    'matplotlib_animations': True
    }