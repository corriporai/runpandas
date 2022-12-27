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
import runpandas as rp
import datetime as dt

# -- Project information -----------------------------------------------------

project = "runpandas"
copyright = "2022, Corri por ai Development Team"
author = "Marcel Caraciolo"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "nbsphinx",
    "sphinxcontrib_github_alt",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


source_parsers = {
    ".md": "recommonmark.parser.CommonMarkParser",
}

source_suffix = [".rst", ".md"]  # #".ipynb"]
master_doc = "index"

github_project_url = "https://github.com/corriporai/runpandas"


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

# Write version and build date
with open("_version.txt", "w") as version_file:
    doc_date = dt.datetime.now().strftime("%B %-d, %Y")
    version_file.write(f"Version: **{version}** Date: **{doc_date}**\n")

# Default language for syntax highlighting in reST and Markdown cells:
highlight_language = "none"

language = None

autosummary_generate = True
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

pygments_style = "default"

todo_include_todos = True

# Don't add .txt suffix to source files:
html_sourcelink_suffix = ""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "external_links": [],
    "github_url": "https://github.com/corriporai/runpandas",
}

# List of arguments to be passed to the kernel that executes the notebooks:
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_logo = "./_static/images/runpandas_banner.png"
html_favicon = "./_static/images/favicon.ico"


def setup(app):
    app.add_css_file("custom.css")  # may also be an URL


html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}

# Output file base name for HTML help builder.
htmlhelp_basename = "runpandasdoc"

# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = 'docs/' + env.doc2path(env.docname, base=None) %}
.. raw:: html

    <div></div>
    <div class="admonition note">
      This page was generated from
      <a class="reference external" href="https://github.com/corriporai/runpandas/blob/HEAD/{{ docname|e }}">{{ docname|e }}</a>.
      Interactive online version:
      <span style="white-space: nowrap;"><a href="https://mybinder.org/v2/gh/corriporai/runpandas/HEAD?filepath={{ docname|e }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>.</span>
      <script>
        if (document.location.host) {
          $(document.currentScript).replaceWith(
            '<a class="reference external" ' +
            'href="https://nbviewer.jupyter.org/url' +
            (window.location.protocol == 'https:' ? 's/' : '/') +
            window.location.host +
            window.location.pathname.slice(0, -4) +
            'ipynb">View in <em>nbviewer</em></a>.'
          );
        }
      </script>
    </div>
"""


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
man_pages = [(master_doc, "runpandas", "runpandas Documentation", [author], 1)]


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
intersphinx_mapping = {
    "http://docs.python.org/": None,
    "ipython": ("https://ipython.readthedocs.io/en/stable/", None),
    "nbconvert": ("https://nbconvert.readthedocs.io/en/latest/", None),
    "nbformat": ("https://nbformat.readthedocs.io/en/latest/", None),
    "jupyter": ("https://jupyter.readthedocs.io/en/latest/", None),
}

extlinks = {
    "issue": ("https://github.com/corriporai/runpandas/issues/%s", "GH"),
    "wiki": ("https://github.com/corriporai/runpandas/wiki/%s", "wiki "),
}
