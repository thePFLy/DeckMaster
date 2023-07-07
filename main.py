from core.modules import Modules
from importlib import import_module

# Load all active modules
modules = Modules()
modules.list_modules
for module in modules.modules:
    module_path = f"modules.{module}"
    globals()[module] = import_module(module_path)
