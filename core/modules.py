from os import scandir
from json import dumps, load
from os.path import exists
from importlib import import_module


class Modules:
    def __init__(self):
        self.modules_list = []
        self.modules_list_error = []
        self.module = None

    def load(self) -> None:
        """
        This method permit to scan the module directory and detect all modules...
        It use the scandir method to scan all module's folder name and add it to the list in self.modules_list...
        """
        with scandir("modules") as modules_library:
            for entry in modules_library:
                if entry.is_dir() and exists(f"modules/{entry.name}/__init__.py"):
                    self.module = entry.name
                    setup_import = import_module(f"modules.{entry.name}.setup")
                    if getattr(setup_import, "try_init")(self.credentials(), setup_mode=True):
                        self.modules_list.append({
                            "name": entry.name,
                            "path": f"modules.{entry.name}"
                        })
                    else:
                        self.modules_list_error.append(entry.name)
                        print(f"Le module {entry.name} présente des problèmes lors de la fonction try_init()")

    def modules_names(self):
        tab = []
        for module in self.modules_list:
            tab.append(module["name"])
        return tab

    def set_key(self, key: str, value: str):
        with open(file=f"config/{self.module}.json", mode="r") as file:
            content = load(file)
        content[key] = value
        with open(file=f"config/{self.module}.json", mode="w") as file:
            file.write(dumps(content, indent=2))
        print(f"La clé {key} ayant pour valeur {value} a été sauvegardée...")

    def credentials(self, key: str = None) -> dict or str:
        if not exists(f"config/{self.module}.json"):
            with open(file=f"config/{self.module}.json", mode="w") as file:
                file.write(dumps({}, indent=2))
        with open(file=f"config/{self.module}.json", mode="r") as file:
            if key is None:
                return load(file)
            elif load(file)[key] != '' and key in load(file):
                return load(file)[key]
            else:
                value = input(
                    "La clé {key} n'existe pas ou n'as pas de valeur dans la configuration, veuillez y définir sa valeur: ")
                self.set_key(key=key, value=value)
                return value
