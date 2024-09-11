from json import load


class System:
    def __init__(self):
        self.system_data = self.read_file()
        self.language = self.read_file(file="config/config.ini")["LANGUAGE"]

    def read_file(self, file: str = "infos.ini"):
        final = {}
        with open(file=file, mode="r", encoding="utf-8") as file:
            data = file.readlines()
        for line in data:
            key, value = line.split("=")[0].strip(), line.split("=")[1].strip()
            final[key] = value
        return final

    def get_value(self, key: str):
        return self.system_data[key]

    def load_trad(self, file: str):
        with open(file=file, mode="r", encoding="utf-8") as file:
            return load(file)

    def show_traduction(self, key: str, module: str = None):
        if module is None:
            return self.load_trad(file=f"l10n/{self.language}.json")[key]
        else:
            return self.load_trad(file=f"modules/{module}/l10n/{self.language}.json")[key]