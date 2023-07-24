from json import loads, dump


class Modules:
    def __init__(self):
        """
        Will manage all modules (delete, add, update, ...)
        """
        self.modules = []

    @property
    def list_modules(self):
        """
        Will list all modules active by reading the modules.json file in modules.
        If the module is specified as active, it will be added in the self.modules list.
        """
        with open('modules/modules.json', 'r', encoding='utf-8') as modules:
            modules = loads(modules.read())
        for item in modules:
            if modules[item]['active']:
                self.modules.append(item)
        return self.modules

    def initialized(self, module):
        """
        Some modules need to be configured. If it's not the case, and, if it's the first time you call the module, the init
        file will be runned and launch the setting mode.
        """
        with open('modules/modules.json', 'r', encoding='utf-8') as modules:
            modules = loads(modules.read())[module]
        return modules['initialized']

    def set_initialized(self, module):
        """
        Once module is configured, this will be set as initialized, so, the next time you will run the module,
        you will not have to set credentials again or fill some settings.
        """
        with open('modules/modules.json', 'r') as file:
            temp = loads(file.read())
            temp[module]['initialized'] = True

        with open('modules/modules.json', 'w') as file:
            dump(temp, file, indent=2)
