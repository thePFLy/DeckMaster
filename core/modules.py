from os.path import exists, getsize
from os import scandir
from importlib import import_module
from json import dumps, load


class Modules:
    def __init__(self, module: str = None):
        self.module = module
        self.modules = []
        self.temp_credentials = {}

    def is_initialized(self, module: str = None) -> bool:
        """
        It check if the module have a credential file, with your datas, etc..c
        """
        m = self.module if self.module is not None else module
        if exists(rf"modules/{m}/credentials.json"):
            return getsize(rf"modules/{m}/credentials.json") > 0
        else:
            return False

    def load(self) -> None:
        """
        dynamicaly get all modules names and launch it when we will feel better...
        """
        with scandir("modules") as it:
            for entry in it:
                if entry.is_dir():
                    self.modules.append(
                        {
                            "name": entry.name,
                            "initialized": self.is_initialized(module=entry.name)
                        }
                    )

        if len(self.modules) > 1:
            print("Select a module to run:")
            index = 0
            for [index, name] in enumerate(self.modules, 1):
                print(f"{str(index).zfill(2)}. {name['name']}")
            while int(index) < 1:
                index = input(">> ")
            module = import_module(rf"modules.{self.modules[int(index)]['name']}")
            module.run(parameters=self.modules[int(index)])
        elif len(self.modules) == 0:
            print("No modules detected")
            exit()
        else:
            module = import_module(rf"modules.{self.modules[0]['name']}")
            module.run(parameters=self.modules[0])

    def set_credential(self, key: str, value: str) -> None:
        """
        """
        self.temp_credentials[key] = value

    def save(self):
        with open(rf'modules/{self.module}/credentials.json', 'a') as credential:
            credential.write(dumps(self.temp_credentials, indent=2))

    def empty_credential(self) -> None:
        with open(rf'modules/{self.module}/credentials.json', 'w') as credential:
            credential.write('')

    def get_credential(self, key: str) -> str:
        with open(f"modules/{self.module}/credentials.json", "r") as credential:
            return load(credential)[key]
