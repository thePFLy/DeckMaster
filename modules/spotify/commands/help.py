"""
This class manage the help menu command !
"""

class Help:
    def __init__(self, arg, commands):
        self.commands = commands
        self.arg = arg
        self.help

    def style(self, style):
        """
        Simple and quick method for customizing strings !
        u is underline
        i is italic
        r is for reset style
        """
        if style == 'u':
            return '\033[4m'
        elif style == 'i':
            return '\033[3m'
        elif style == 'r':
            return '\033[0m'

    @property
    def help(self):
        """
        if
        """
        if self.arg == 'help':
            for command in self.commands:
                print(f"{self.style('u')}{command}:{self.style('r')}\n"
                      f" - Info: {self.commands[command]['help']}\n"
                      f" - Usage: {self.commands[command]['usage']}\n"
                      f" - Premium: {self.commands[command]['premium']}"
                      )
                if self.commands[command]['sub_commands']:
                    print(f" - {self.style('u')}Sub-commands:{self.style('r')}")
                    for command2 in self.commands[command]['subcommands']:
                        print(f"   {self.style('i')}{command2}:{self.style('r')}\n"
                              f"     - info: {self.commands[command]['subcommands'][command2]['help']}\n"
                              f"     - usage: {self.commands[command]['subcommands'][command2]['usage']}\n"
                              f"     - usage: {self.commands[command]['subcommands'][command2]['premium']}"
                              )
        elif len(self.arg) < 3:
            if self.arg[1] in self.commands:
                print(
                    f"{self.style('u')}{self.arg[1]}:{self.style('r')}\n"
                    f" - Info: {self.commands[self.arg[1]]['help']}\n"
                    f" - Usage: {self.commands[self.arg[1]]['usage']}\n"
                    f" - Premium: {self.commands[self.arg[1]]['premium']}"
                )
                if self.commands[self.arg[1]]['sub_commands']:
                    print(f" - {self.style('u')}Sub-commands:{self.style('r')}")
                    for command2 in self.commands[self.arg[1]]['subcommands']:
                        print(f"   {self.style('i')}{command2}:{self.style('r')}\n"
                              f"     - info: {self.commands[self.arg[1]]['subcommands'][command2]['help']}\n"
                              f"     - usage: {self.commands[self.arg[1]]['subcommands'][command2]['usage']}\n"
                              f"     - usage: {self.commands[self.arg[1]]['subcommands'][command2]['premium']}"
                              )
            else:
                print(f"{self.arg} is not know as command.\nPlease check commands with: help")
