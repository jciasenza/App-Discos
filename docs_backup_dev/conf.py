# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GestionMusical'
copyright = '2026, Juan Carlos Iasenza'
author = 'Juan Carlos Iasenza'

version = '4.5.0'
release = '4.5.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

autodoc_mock_imports = ["peewee", "PIL", "Pillow", "dotenv"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

extensions.append("sphinx_wagtail_theme")
html_theme = 'sphinx_wagtail_theme'
html_static_path = ['_static']

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

import os
import sys
from unittest.mock import MagicMock


# docs/conf.py

# ... (tus otros imports)

class MockSqliteDatabase(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Añadimos el método que falta para que inicializar_db() no falle
    def is_closed(self):
        return True  # Le decimos que está cerrada para que no intente hacer nada raro

class MockModel(MagicMock):
    pass

# Definimos las clases que tu código busca explícitamente
class MockSqliteDatabase(MagicMock): pass
class MockModel(MagicMock): pass

# Creamos el objeto mock de peewee
mock_peewee = MagicMock()
mock_peewee.SqliteDatabase = MockSqliteDatabase
mock_peewee.Model = MockModel
# Añadimos tipos de campos comunes por si acaso
mock_peewee.CharField = MagicMock
mock_peewee.TextField = MagicMock
mock_peewee.IntegerField = MagicMock
mock_peewee.ForeignKeyField = MagicMock

# INYECCIÓN CRÍTICA:
# Esto hace que 'from peewee import *' encuentre los nombres
sys.modules["peewee"] = mock_peewee

# Otros mocks
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.Image"] = MagicMock()
sys.modules["PIL.ImageTk"] = MagicMock()
sys.modules["dotenv"] = MagicMock()

autodoc_mock_imports = ["peewee", "PIL", "Pillow", "dotenv"]

sys.path.insert(0, os.path.abspath('../'))
