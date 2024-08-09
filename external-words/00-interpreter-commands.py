import os
import subprocess
import tempfile

from Interpreter import Interpreter
from Rule import NativeRule, Rule
import RuleParser
from RuleSet import RuleSet
from Stack import Stack
import StackParser

# TODO move call- and datastack validation into superclass.
# The just call super.match(), or let NativeRules.py call isSatisfied() - see
# specification pattern by evans and fowler - and only when this is True, then
# NativeRules will call execute. This way the check cannot be forgotten.
# TODO add name attribute to NativeRule, so that NativeRuleLoader can print
# the Word from rule

# TODO add alias rule `" <rulename> <wrd> <wrd>` -> `<rulename> -> | <wrd> <wrd>`
# Use a new ruleclass for this, to print this rule in the simple form, not the converted one.
# AND adjust the parser to also accept this type of rules from loading a file.
# Or use `read-word`. Word is unkown, put it on DS and push read-word, which can
# be implemented by the user

# TODO add name and description to rules
# TODO Fix unit-test and main entrypoint, loading of rules
# TODO Restructure native rules/move some rules from consize into this file
# TODO add alias Rule (as seen above)

class ShowHelp(NativeRule):
    """
    Displays this help.
    """

    def name(self) -> str:
        return "?"

    def execute(self, interpreter) -> bool | dict:
        try:
            csw, *rcs = interpreter.cs
        except ValueError:
            return False

        if not csw == "?":
            return False

        help = ("\n").join(["Native Rules:", *[f"{rule.name()} {rule.description()}" for rule in interpreter.native_rules]])
        interpreter.print(help)
        interpreter.cs = Stack(*rcs)
        return True

class CurrentContinuation(NativeRule):
    """
    Puts the current continuation on the datastack.
    [ DS ] [ CS ]
    """

    def name(self) -> str:
        return "cc"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "cc":
            return False
        interpreter.cs.pop(0)
        interpreter.ds = Stack(*interpreter.ds, interpreter.ds)
        interpreter.ds = Stack(*interpreter.ds, interpreter.cs)
        return True

class LiveEditCC(NativeRule):
    """
    Opens the current continuation within the editor for modification.
    Upon save, the changed continuation will be put on the DS.
    """

    def name(self) -> str:
        return "ecc"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "ecc":
            return False
        interpreter.cs.pop(0)
        ccWrd = Stack(interpreter.ds,interpreter.cs).toString(addEnclosingParenthesis=False)
        interpreter.ds = Stack(*interpreter.ds, ccWrd)
        # Could also execute "cc" - current continuation - (as seen below) but
        # then "edit" will only work on the callstack, as edit only takes the
        # top of datastack. Therefore we will wrap the continuation in a stack
        # interpreter.cs = Stack("cc", *interpreter.cs)
        # interpreter.make_step()
        interpreter.cs = Stack("edit", *interpreter.cs)
        interpreter.make_step()
        ccLines, *rds = interpreter.ds
        ncc = StackParser.parse(ccLines[0])
        interpreter.ds = Stack(*rds, *ncc)
        return True

class SetCC(NativeRule):
    """
    Replace the current continuation with one from the top of the DS.
    The old one, will be no longer available.
    """

    def name(self) -> str:
        return "set-cc"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "set-cc":
            return False

        if len(interpreter.ds) <= 2:
            interpreter.print_error("No valid continuation found on DS.")
        interpreter.cs.pop(0)

        *rest, ds, cs = interpreter.ds
        interpreter.ds = StackParser.parse(ds) if isinstance(ds, str) else ds
        interpreter.cs = StackParser.parse(cs) if isinstance(cs, str) else cs
        return True

class Callstack(NativeRule):
    """
    Puts the current callstack on top of the DS.
    """

    def name(self) -> str:
        return "cs"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "cs":
            return False
        interpreter.cs.pop(0)
        interpreter.ds = Stack(*interpreter.ds, str(interpreter.cs))
        return True

class Datastack(NativeRule):
    """
    Puts the datastack on top of the DS.
    """

    def name(self) -> str:
        return "ds"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "ds":
            return False
        interpreter.cs.pop(0)
        interpreter.ds = Stack(*interpreter.ds, str(interpreter.ds))
        return True

class Rules(NativeRule):
    """
    Puts the current rules on the datastack.
    Every rule will be a Wrd wrapped within a Stack (which resembels lines)
    which are also wrapped within a stack. E.g.
    [ [ Rule ] [ Rule ] ... ]
    """

    def name(self) -> str:
        return "rules"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "rules":
            return False

        interpreter.ds = Stack(*interpreter.ds, Stack(*[Stack(rule) for rule in interpreter.ruleset]))
        interpreter.cs.pop(0)
        return True

class SetRules(NativeRule):
    """
    Replaces the current rules with the rules taken from top of the datastack.
    Rules must be given in the form of: [ [ RuleWrd ] [ RuleWrd ] ...]
    """

    def name(self) -> str:
        return "set-rules"

    def execute(self, interpreter):
        try:
            csw, *rcs = interpreter.cs
            *rds, rules = interpreter.ds
        except ValueError:
            return False

        if not csw == "set-rules":
            return False

        if not isinstance(rules, Stack):
            return False

        new_ruleset = RuleSet([])
        for [rule] in rules:
            if not isinstance(rule, Rule):
                err, rule = RuleParser.parse(rule)
                if err:
                    interpreter.print_error(err)
                    return False
            new_ruleset.add(rule)

        interpreter.ruleset = new_ruleset

        interpreter.ds = Stack(*rds)
        interpreter.cs = Stack(*rcs)
        return True

class Edit(NativeRule):
    """
    Opens the top element on the stack in the editor, for live editing.
    """

    def name(self) -> str:
        return "edit"

    def execute(self, interpreter):
        if interpreter.cs == []:
            return False

        cw, *rcs = interpreter.cs
        if cw != "edit":
            return False

        if interpreter.ds != []:
            *rest, word = interpreter.ds
        else:
            rest = interpreter.ds
            word = ""

        encounteredError = False
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            # Write the current ruleset to the temporary file
            temp_file.write(str(word).encode('utf-8'))
            temp_file.close()  # Close the file to ensure it's saved

            # Open the users prefered text-editor, otherwise nano
            editor = os.environ.get('EDITOR', 'nano')  # Default to 'nano' if EDITOR is not set
            try:
                subprocess.run([editor, temp_file.name])
            except Exception as e:
                interpreter.print_error(f"Failed to open the editor. Error: {e}")
                encounteredError = True

            # Read the content of the file after the editor is closed
            if not encounteredError:
                with open(temp_file.name, 'r', encoding='utf-8') as f:
                    final_content = f.read().strip()

        # Clean up the temporary file
        os.remove(temp_file.name)

        interpreter.ds = Stack(*rest, Stack(*[str(line) for line in final_content.splitlines()]))
        interpreter.cs = Stack(*rcs)
        return True

class Step(NativeRule):
    """
    Performs a single rule substitution step.
    """

    def name(self) -> str:
        return "step"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "step":
            return False
        interpreter.cs.pop(0)
        if not interpreter.make_step():
            interpreter.print_error(f"No applicative rules found.")
        return True

class Continue(NativeRule):
    """
    Performse as many steps as possible, until no rule cant be applied.
    """

    def name(self) -> str:
        return "continue"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "continue":
            return False
        interpreter.cs.pop(0)
        while interpreter.make_step():
            pass
        return True

class Status(NativeRule):
    """
    Prints the current data- and callstack to the console.
    """

    def name(self) -> str:
        return "status"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "status":
            return False
        interpreter.cs.pop(0)
        interpreter.log_state()
        return True

class HaltRequest(NativeRule):
    """
    Will request the interpreter to terminate.
    Can also use: quit and :q
    """

    def name(self) -> str:
        return "exit"

    def execute(self, interpreter):
        if interpreter.cs == [] or not (interpreter.cs.peek() == "exit" or interpreter.cs.peek() == "quit" or interpreter.cs.peek() == ":q"):
            return False
        interpreter.cs.pop(0)
        interpreter.halt = True
        return True

class AddToRuleSet(NativeRule):
    """
    Adds a rule to the ruleset. The rule must be a word on top of the datastack.
    """

    def name(self) -> str:
        return "add-rule"

    def execute(self, interpreter):
        if interpreter.cs == []:
            return False

        cw, *rcs = interpreter.cs
        if not cw == "add-rule":
            return False

        if interpreter.ds == []:
            interpreter.print_error("No rule description given.")
            return False

        *rds, ruleDesc = interpreter.ds

        if not isinstance(ruleDesc, str):
            return False

        err, rule = RuleParser.parse(ruleDesc)
        if err:
            interpreter.print_error(err.msg)
            return False
        err = interpreter.ruleset.add(rule)
        if err:
            interpreter.print_error(err.msg)
            return False

        interpreter.ds = Stack(*rds)
        interpreter.cs = Stack(*rcs)
        return True

class RedisoverNativeRules(NativeRule):
    """
    Tries to discover and add new native rules from the module directory.
    """

    def name(self) -> str:
        return "rediscover"

    def execute(self, interpreter):
        if interpreter.cs == [] or not interpreter.cs.peek() == "rediscover":
            return False
        interpreter.discover_native_rules()
        interpreter.cs.pop(0)
        return True

class Write(NativeRule):
    """
    Takes the filepath from the top of datastack and writes the seconds element
    from the datastack to the file, located at the filepath.
    """

    def name(self) -> str:
        return "write"

    # TODO should probably also write the rule native rules as comments into
    # the ruleset. Just for information, that some rules might not be
    # available. Sharing the ruleset-file.
    def execute(self, interpreter):
        try:
            csw, *rcs = interpreter.cs
            *rds, path = interpreter.ds
        except ValueError:
            return False

        if not (csw == "write" and isinstance(path, str)):
            return False

        try:
            with open(path, "w") as file:
                file.write(str(interpreter.ruleset))
        except FileNotFoundError:
            interpreter.print_error(f"File not found: {path}")
            return False
        except PermissionError:
            interpreter.print_error(f"Permission denied to write file: {path}")
            return False
        except IOError as e:
            interpreter.print_error(f"An error occurred while writing the file: {e}")
            return False

        interpreter.ds = Stack(*rds)
        interpreter.cs = Stack(*rcs)
        return True
