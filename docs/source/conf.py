# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sys
import os
import runpandas as rp
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'runpandas'
copyright = '2020, Corri por ai Development Team'
author = 'Marcel Caraciolo'

import IPython

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


source_suffix = ".rst"
master_doc = "index"



# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = rp.__version__.split("+")[0]
if "+" in rp.__version__:
    commit = rp.__version__.split("+")[1]
    commits_since_tag, commit_hash = commit.split(".")[:2]
    commit_hash = commit_hash[1:]
    commit = " (+" + commits_since_tag + ", " + commit_hash + ")"
    version += commit
# The full version, including alpha/beta/rc tags.
release = rp.__version__

language = None


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

pygments_style = "default"

todo_include_todos = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}

# Output file base name for HTML help builder.
htmlhelp_basename = "runpandasdoc"


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "runpandas.tex",
        "runpandas Documentation",
        "corriporai",
        "manual",
    )
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "runpandas", "runpandas Documentation", [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "runpandas",
        "runpandas Documentation",
        author,
        "runpandas",
        "One line description of project.",
        "Miscellaneous",
    )
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"http://docs.python.org/": None}


extlinks = {
    "issue": ("https://github.com/corriporai/runpandas/issues/%s", "GH"),
    "wiki": ("https://github.com/corriporai/runpandas/wiki/%s", "wiki "),
}