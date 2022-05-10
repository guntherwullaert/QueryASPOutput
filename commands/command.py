class QueryCommand:
    def get_help(self, app, args):
        return ""

    def is_input_command(self, app, args):
        pass

    def requires_run_before(self):
        return False

    def run_command(self, app, args):
        pass