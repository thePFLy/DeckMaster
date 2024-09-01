class System:
    def __init__(self):
        self.system_data = self.read_file()

    def read_file(self):
        final = {}
        with open(file="infos.ini", mode="r", encoding="utf-8") as file:
            data = file.readlines()
        for line in data:
            key, value = line.split("=")[0].strip(), line.split("=")[1].strip()
            final[key] = value
        return final

    def get_value(self, key: str):
        return self.system_data[key]
