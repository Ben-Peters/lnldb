# -*- coding: utf-8 -*-
#
# LNL Database documentation build configuration file, created by
# sphinx-quickstart on Tue Dec 12 12:57:05 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import django
sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'lnldb.settings'
django.setup()


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'LNL Database'
copyright = u'2017, Jake Merdich, Gabe Morell'
author = u'Jake Merdich, Gabe Morell'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u''
# The full version, including alpha/beta/rc tags.
release = u''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'agogo'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'LNLDatabasedoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'LNLDatabase.tex', u'LNL Database Documentation',
     u'Jake Merdich, Gabe Morell', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'lnldatabase', u'LNL Database Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'LNLDatabase', u'LNL Database Documentation',
     author, 'LNLDatabase', 'One line description of project.',
     'Miscellaneous'),
]

# -- Special Autoprocessing -----------------------------------------------

# https://djangosnippets.org/snippets/2533/
import inspect
from django.utils.html import strip_tags
from django.utils.encoding import force_text

def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
           if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects

def default_to_parent_docstr(app, what, name, obj, options, lines):
    if inspect.isfunction(obj) and obj.__doc__ is None and len(lines) == 0:
        cls = get_class_that_defined_method(obj)
        if cls is not None:
            mro = inspect.getmro(cls)
            for parent_cls in mro:
                parent_func = getattr(parent_cls, obj.__name__, None)
                if parent_func.__doc__ is not None:
                    lines[:] = parent_func.__doc__.split('\n')
                    return


field_formatters = {
        'to': lambda f,v: " :class:`~%s.%s`" % (f.related_model.__module__, f.related_model.__name__)
        }

# Gives a pretty field description
def format_field_name(model, field):
    field_type = field.get_internal_type()
    
    args = field.deconstruct()[3]
    for arg, val in args.items():
        if arg in field_formatters:
            args[arg] = field_formatters[arg](field,val)
        elif inspect.isfunction(val):
            args[arg] = val.__name__ + "()"
        elif isinstance(val, str):
            args[arg] = '"' + str(val) + '"'
   
    outargs = ["%s=%s" % (k,v) for k,v in args.items()]
    out = "%s(%s)" % (field_type, ", ".join(outargs))
    return out
    
# Automatically generate a nice overview for each model
def process_model(app, what, name, obj, options, lines):
    # This causes import errors if left outside the function
    from django.db import models
    from django.db.models.fields.related import RelatedField

    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        # Grab the field list from the meta class
        fields = obj._meta.get_fields()

        for field in fields:
            # skip relations
            if not hasattr(field, 'verbose_name'):
                continue

            # Decode and strip any html out of the field's help text
            help_text = strip_tags(force_text(field.help_text))

            # Decode and capitalize the verbose name, for use if there isn't
            # any help text
            verbose_name = force_text(field.verbose_name).capitalize()

            if help_text:
                # Add the model field to the end of the docstring as a param
                # using the help text as the description
                lines.append(u':param %s: %s' % (field.name, help_text))
            else:
                # Add the model field to the end of the docstring as a param
                # using the verbose name as the description
                lines.append(u':param %s: %s' % (field.name, verbose_name))

            if field.null == False and field.default == models.NOT_PROVIDED:
                lines[-1] += u' (required)'
            elif field.default != models.NOT_PROVIDED:
                lines[-1] += u' (default=%s)' % str(field.default)

            # Add the field's type to the docstring
            if isinstance(field, RelatedField):
                to = field.rel.to
                lines.append(u':type %s: %s to :class:`~%s.%s`' % (field.name, type(field).__name__, to.__module__, to.__name__))
            else:
                lines.append(u':type %s: %s' % (field.name, type(field).__name__))

    # Return the extended docstring
    return lines

# Properly document model fields by refetching from model._meta
def process_modelfield(app, what, name, obj, options, lines):
    # This causes import errors if left outside the function
    from django.db.models.query_utils import DeferredAttribute
    from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor, ReverseManyToOneDescriptor
    from importlib import import_module
    from django.db import models
    import pdb

    # Only look at objects that inherit from Django's base model class
    if what == "attribute" and isinstance(obj, (DeferredAttribute, ForwardManyToOneDescriptor)):
        model_path = '.'.join(name.split('.')[:-2])
        model_name = name.split('.')[-2]
        field_name = name.split('.')[-1]
        model_module = import_module(model_path)
        model = getattr(model_module, model_name)
        field = model._meta.get_field(field_name)

        # the previous stuff is crap
        del lines[:]

        if isinstance(field, models.ForeignKey) and field_name == field.attname:
            lines.append("Raw (integer) FK for :py:attr:`%s`" % (field.name))
            return

        # Decode and strip any html out of the field's help text
        help_text = strip_tags(force_text(field.help_text))

        # Decode and capitalize the verbose name, for use if there isn't
        # any help text
        verbose_name = force_text(field.verbose_name).capitalize()

        lines.append(format_field_name(obj, field))
        lines.append("")

        if help_text:
            # Add the model field to the end of the docstring as a param
            # using the help text as the description
            lines.append(u'%s: %s' % (verbose_name, help_text))
    elif what == "attribute" and isinstance(obj, (ReverseManyToOneDescriptor)):
        del lines[:]
        field = obj.field
        model = field.model
        lines.append("Reverse Manager for %s's :py:attr:`~%s.%s.%s`" % (model._meta.label, model.__module__, model.__name__, field.name))

    # Return the extended docstring
    return lines

def setup(app):
    # Register the docstring processor with sphinx
    app.connect('autodoc-process-docstring', process_model)
    app.connect('autodoc-process-docstring', process_modelfield)
    app.connect('autodoc-process-docstring', default_to_parent_docstr)
