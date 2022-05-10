from commands.command import QueryCommand
import shlex, pkg_resources, os, importlib, inspect

class QueryApp:
    def __init__(self):
        self.exit = False
        self.commands = []
        self.models = []
        self.has_run = False
        self.class_list_modules = set()
        self.configuration = {}

    def register_commands(self, *commands):
        for command in commands:
            self.commands.append(command)

    def load_commands(self):
        commands_folder = pkg_resources.resource_filename("commands", "")
        for root, directory, files in os.walk(commands_folder):
            python_files = [fname for fname in files if fname.endswith('.py') and not fname.startswith('__')]

            for file in python_files:
                module_name = os.path.basename(file)
                try:
                    if module_name in self.class_list_modules:
                        continue

                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(root, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.class_list_modules.add(module_name)
                except (SystemError, ImportError,
                        NotImplementedError, SyntaxError, NameError) as e:
                    print(f'\033[93mModule "{module_name}" could not be loaded: \033[0m')
                    print(e)
                    continue
                
                for class_object in dir(module):
                    actual_class_object = getattr(module, class_object)

                    if (inspect.isclass(actual_class_object) and inspect.getmodule(actual_class_object) == None and issubclass(actual_class_object, QueryCommand) and actual_class_object != QueryCommand):
                        self.register_commands(actual_class_object())

    def on_model(self, model):
        self.models.append(model.symbols(shown=True))

    def check_field_in_configuration(self, *names):
        for name in names:
            if(not (name in self.configuration)):
                print(f"{name} is not set in the configuration!")
                return False
        return True

    def show_model(self, model_number, atoms):
        print("{}: ".format(model_number), end = '')
        line = ""
        for atom in atoms:
            line += str(atom) + ", "
        
        if len(atoms) > 0:
            line = line[:-2]
        print(line)

    def run(self):
        self.exit = False

        while(not self.exit):
            input_from_user_string = input("> ")
            input_from_user = shlex.split(input_from_user_string)

            found_command = False
            for command in self.commands:
                if(command.is_input_command(self, input_from_user)):
                    if(command.requires_run_before() and self.has_run == False):
                        print("You need to use the run command first!")
                    else:
                        command.run_command(self, input_from_user)
                    found_command = True
                    break

            #if(not found_command):
                #HelpCommand().run_command(self, input_from_user)

if __name__ == "__main__":
    Q = QueryApp()
    Q.load_commands()
    Q.run()