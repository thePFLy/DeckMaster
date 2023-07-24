class Userinfo:
    def __init__(self, account):
        self.account = account
        self.userinfo

    @property
    def userinfo(self):
        print("\033[4mUser informations:\033[0m\n"
              f"User: {self.account['display_name']}\n"
              f"Image: {self.account['images'][0]['url']}\n"
              f"Type of account: {'Free' if self.account['product'] == 'free' else 'Premium'}")
        return None
