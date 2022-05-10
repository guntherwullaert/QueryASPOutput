from commands.command import QueryCommand

class HelpCommand(QueryCommand):
    def get_help(self, app, args):
        return "help - show a list of each command"

    def is_input_command(self, app, args):
        return len(args) > 0 and args[0] == "help"

    def run_command(self, app, args):
        help_texts = []
        for command in app.commands:
            help_text = command.get_help(app, args)
            if(help_text == ""): continue
            help_texts.append(help_text)

        help_texts.sort()
        for text in help_texts:
            print(text)
