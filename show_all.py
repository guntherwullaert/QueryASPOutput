from commands.command import QueryCommand
from clingo.control import Control

class ShowAllCommand(QueryCommand):
    def get_help(self, app, args):
        return "show all - show all models returned by clingo"

    def is_input_command(self, app, args):
        return len(args) > 1 and args[0] == "show" and args[1] == "all"

    def requires_run_before(self):
        return True

    def run_command(self, app, args):
        for i in range(len(app.models)):
            app.show_model(i, app.models[i])