from commands.command import QueryCommand

class ExitCommand(QueryCommand):
    def get_help(self, app, args):
        return "exit - exit the console"

    def is_input_command(self, app, args):
        return len(args) > 0 and args[0] == "exit"

    def run_command(self, app, args):
        exit()