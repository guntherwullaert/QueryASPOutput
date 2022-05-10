from commands.command import QueryCommand

class ConfigCommand(QueryCommand):
    def get_help(self, app, args):
        return "config files <file_names>* - loads clingo with a number of files"

    def is_input_command(self, app, args):
        return len(args) > 2 and args[0] == "config" and args[1] == "files"

    def run_command(self, app, args):
        app.configuration["files"] = []
        for file in args[2:]:
            app.configuration["files"].append(file)
        print("Configuration set!")