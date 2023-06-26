from json import loads, dump


class Credentials:
    """
    Credentials is a class who manage how the Deck will store, get or edit values for all modules.
    """

    def __init__(self, module):
        self.module = module
        with open(f'modules/{module}/credentials.json') as credential:
            self.values = loads(credential.read())

    def set(self, key, value):
        """
        Write a value in the credential file
        """
        self.values[key] = value
        with open(f'modules/{self.module}/credentials.json', 'w') as file:
            dump(self.values, file, indent=2)
