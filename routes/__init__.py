# routes/__init__.py
import os
import importlib
from flask import Blueprint

# Dictionary to store all blueprints
blueprints = {}

# Get the current directory (routes/)
current_dir = os.path.dirname(__file__)

# Loop through all Python files in this folder
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # remove .py
        module_path = f"{__name__}.{module_name}"
        module = importlib.import_module(module_path)
        # Check if the module has a variable 'bp_' (blueprint)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, Blueprint):
                blueprints[attr] = obj
