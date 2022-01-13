from clingo.control import Control
from clingo.symbol import Number, Symbol
import re

class QueryApp:
    def __init__(self):
        self.models = []
        self.has_run = False

    def on_model(self, model):
        self.models.append(model.symbols(atoms=True))

    def check_for_run(self):
        if(not self.has_run): 
            print("ERROR: You need to run clingo first")
            return True
        return False

    def show_specifc_model(self, i):
        if(self.check_for_run()):
            return

        i = int(i)

        if(0 <= i <= len(self.models)):
            print(self.models[i])
        else:
            print("ERROR: Model out of bounds: 0 - "+len(self.models))

    def show_all_models(self):
        if(self.check_for_run()):
            return

        for i in range(len(self.models)):
            print("{} - {}".format(i, self.models[i]))

    def brave_atoms(self):
        if(self.check_for_run()):
            return

        found_atoms = []
        brave_atoms = []
        for m in self.models:
            for atom in m:
                if(atom in found_atoms and atom in brave_atoms):
                    brave_atoms.remove(atom)
                elif(not (atom in found_atoms)):
                    found_atoms.append(atom)
                    brave_atoms.append(atom)

        for atom in brave_atoms:
            print(atom)

    def cautious_atoms(self):
        if(self.check_for_run()):
            return

        cautious_atoms = []

        model_count = len(self.models)
        if(model_count <= 0):
            return

        for atom in self.models[0]:
                cautious_atoms.append(atom)

        for i in range(1, model_count):
            for atom in cautious_atoms:
                if(not (atom in self.models[i])):
                    cautious_atoms.remove(atom)

        for atom in cautious_atoms:
            print(atom)

    def clingo_constraint(self, constraint):
        if(self.check_for_run()):
            return

        model_count = len(self.models)
        facts = "1 {"
        for i in range(model_count):
            facts += "model({});".format(i)

        facts = facts[:-1]
        facts += "} 1."
        
        for i in range(model_count):
            for atom in self.models[i]:
                facts += "{} :- model({}).".format(atom, i)

        print(facts + constraint)

        self.models = []
        ctl = Control("0")
        ctl.add("base", [], facts+constraint)
        ctl.ground([("base", [])], context=self)
        ctl.solve(on_model=self.on_model, )

        #remove model from models
        regex = re.compile(r'model\([0-9]*\)')
        for i in range(len(self.models)):
            self.models[i] = [str(j) for j in self.models[i] if not regex.match(str(j))]

    def run(self):
        '''
        Runs the example.
        '''
        self.models = []
        ctl = Control("0")
        ctl.load("test.lp")
        ctl.ground([("base", [])], context=self)
        ctl.solve(on_model=self.on_model, )
        self.has_run = True

if __name__ == "__main__":
    Q = QueryApp()
    exit = False

    while(not exit):
        inputFromUserString = input("> ")
        inputFromUser = inputFromUserString.split(" ")
        command = inputFromUser[0]
        args = inputFromUser[1:]

        if(inputFromUserString.startswith(":-")):
            Q.clingo_constraint(inputFromUserString)
            continue

        if(command == "exit"):
            exit = True

        if(command == "run"):
            Q.run()

        if(command == "show" and args[0] == "all"):
            Q.show_all_models()

        elif(command == "show"):
            Q.show_specifc_model(args[0])

        if(command == "brave"):
            Q.brave_atoms()
        
        if(command == "cautious"):
            Q.cautious_atoms()
