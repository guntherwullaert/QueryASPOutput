from commands.command import QueryCommand
from clingo.control import Control

class RunCommand(QueryCommand):
    def get_help(self, app, args):
        return "run - run with the current loaded configuration"

    def is_input_command(self, app, args):
        return len(args) > 0 and args[0] == "run"

    def run_command(self, app, args):
        if(not app.check_field_in_configuration("files")): return
        
        print("Running...")
        app.models = []
        ctl = Control("0")
        for file in app.configuration["files"]:
            ctl.load(file)
        ctl.ground([("base", [])], context=app)
        ctl.solve(on_model=app.on_model, )
        app.has_run = True
        print("Finished!")