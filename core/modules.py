from json import dumps, load
from importlib import import_module
from os import scandir
from sys import modules


class Modules:
    def __init__(self):
        self.loaded_modules = []

    def list_modules_folder(self):
        list_modules = []
        for module in scandir("modules/"):
            list_modules.append(module.name)
        return list_modules

    def is_module_imported(self, module: str, log: bool = False):
        result = []
        for module_name in modules:
            if module in module_name:
                result.append(module_name)
        if log:
            return {
                "response": len(result) > 0,
                "result": result
            }
        else:
            return len(result) > 0

    def load(self, module: str):
        if self.is_module_imported(module=module):
            return "MODULE_ALREADY_LOADED"
        elif module in self.list_modules_folder():
            setup = import_module(f"modules.{module}.setup")
            if getattr(setup, "try_init")(self.credentials(module="spotify")):
                import_module(f"modules.{module}")
                self.loaded_modules.append(module)
                return "LOADED"
            else:
                print("????")
                return getattr(setup, "setup")
        else:
            return "MODULE_NOT_FOUND"

    def unload(self, module: str):
        self.table_modules["disabled"].remove(module)

    def set_key(self, module: str, key: str, value: str):
        with open(file=f"config/{module}.json", mode="r") as file:
            content = load(file)
        content[key] = value
        with open(file=f"config/{module}.json", mode="w") as file:
            file.write(dumps(content, indent=2))
        return "KEY_HAS_BEEN_SET"

    def credentials(self, module: str, key: str = None) -> dict or str:
        with open(file=f"config/{module}.json", mode="r") as file:
            if key is None:
                return load(file)
            elif key in load(file) and load(file)[key] != '':
                return load(file)[key]
            else:
                return "KEY_NOT_FOUND"
