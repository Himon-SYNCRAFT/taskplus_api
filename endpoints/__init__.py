import os
from importlib import import_module

for module in os.listdir(os.path.dirname(__file__)):
    if module != '__init__.py' and module[-3:] == '.py':
        import_module('endpoints.' + module[:-3])

del module
del os
del import_module
