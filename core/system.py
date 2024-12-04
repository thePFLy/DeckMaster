from json import load, dumps


class System:
    def __init__(self):
        self.system_data = self.read_file()
        self.language = self.read_file(file="config/config.ini")["LANGUAGE"]

    @staticmethod
    def read_file(file: str = "infos.ini"):
        final = {}
        with open(file=file, mode="r", encoding="utf-8") as file:
            data = file.readlines()
        for line in data:
            key, value = line.split("=")[0].strip(), line.split("=")[1].strip()
            final[key] = value
        return final

    def get_value(self, key: str):
        return self.system_data[key]

    @staticmethod
    def load_trad(file: str):
        with open(file=file, mode="r", encoding="utf-8") as file:
            return load(file)

    def show_traduction(self, key: str, module: str = None):
        if module is None:
            try:
                return self.load_trad(file=f"l10n/{self.language}.json")[key]
            except KeyError:
                self.create_key(key=key, module=module)
        else:
            try:
                return self.load_trad(file=f"modules/{module}/l10n/{self.language}.json")[key]
            except KeyError:
                self.create_key(key=key, module=module)

    def create_key(self, key: str, module: str = None):
        if module is None:
            data = self.load_trad(file=f"l10n/{self.language}.json")
        else:
            data = self.load_trad(file=f"modules/{module}/l10n/{self.language}.json")
        data[key] = ""
        self.save_trad(data=data, module=module)

    def save_trad(self, data: dict, module: str = None):
        if module is None:
            with open(file=f"l10n/{self.language}.json", mode="w", encoding="utf-8") as new_data:
                new_data.write(dumps(data, indent=2))
        else:
            with open(file=f"modules/{module}/l10n/{self.language}.json", mode="w", encoding="utf-8") as new_data:
                new_data.write(dumps(data, indent=2))

    @staticmethod
    def get_css(module: str, filename: str):
        if module is None:
            filepath = f"templates/styles/{filename}.css"
        else:
            filepath = f"templates/{module}/{filename}.css"
        with open(file=filepath, mode="r", encoding="utf-8") as css:
            return css.read()

    @staticmethod
    def get_html(module: str, filename: str):
        if module is None:
            filepath = f"templates/styles/{filename}.html"
        else:
            filepath = f"templates/{module}/{filename}.html"
        with open(file=filepath, mode="r", encoding="utf-8") as html:
            return html.read()

    @staticmethod
    def get_image(module: str, filename: str, extention: str):
        if module is None:
            filepath = f"templates/styles/{filename}.{extention}"
        else:
            filepath = f"templates/{module}/icon/{filename}.{extention}"
        return filepath
