import importlib
import os
import subprocess
import sys
import tempfile

from Interpreter import Interpreter
from Rule import NativeRule, Rule
import RuleParser
from RuleSet import RuleSet
from Stack import Stack
import StackParser
from TerminalEscsapeCodes import TerminalEscapeCodes as TEC

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


class CurrentContinuation(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "cc":
            return False
        i.cs.pop(0)
        i.ds = Stack(*i.ds, i.ds)
        i.ds = Stack(*i.ds, i.cs)
        return True

class LiveEditCC(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "ecc":
            return False
        i.cs.pop(0)
        ccWrd = Stack(i.ds,i.cs).toString(addEnclosingParenthesis=False)
        i.ds = Stack(*i.ds, ccWrd)
        # Could also execute "cc" - current continuation - (as seen below) but
        # then "edit" will only work on the callstack, as edit only takes the
        # top of datastack. Therefore we will wrap the continuation in a stack
        # i.cs = Stack("cc", *i.cs)
        # i.make_step()
        i.cs = Stack("edit", *i.cs)
        i.make_step()
        ccLines, *rds = i.ds
        ncc = StackParser.parse(ccLines[0])
        i.ds = Stack(*rds, *ncc)
        return True

class SetCC(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "set-cc":
            return False

        if len(i.ds) <= 2:
            i.print_error("No valid continuation found on DS.")
        i.cs.pop(0)

        *rest, ds, cs = i.ds
        i.ds = StackParser.parse(ds) if isinstance(ds, str) else ds
        i.cs = StackParser.parse(cs) if isinstance(cs, str) else cs
        return True

class Callstack(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "cs":
            return False
        i.cs.pop(0)
        i.ds = Stack(*i.ds, str(i.cs))
        return True

class Datastack(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "ds":
            return False
        i.cs.pop(0)
        i.ds = Stack(*i.ds, str(i.ds))
        return True

class DumpRuleset(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "rules":
            return False

        i.ds = Stack(*i.ds, Stack(*[Stack(rule) for rule in i.ruleset]))
        i.cs.pop(0)
        return True

class SetRules(NativeRule):
    def execute(i: Interpreter):
        try:
            csw, *rcs = i.cs
            *rds, rules = i.ds
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
                    i.print_error(err)
                    return False
            new_ruleset.add(rule)

        i.ruleset = new_ruleset

        i.ds = Stack(*rds)
        i.cs = Stack(*rcs)
        return True

class Edit(NativeRule):
    def execute(i: Interpreter):
        if i.cs == []:
            return False

        cw, *rcs = i.cs
        if cw != "edit":
            return False

        if i.ds != []:
            *rest, word = i.ds
        else:
            rest = i.ds
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
                i.print_error(f"Failed to open the editor. Error: {e}")
                encounteredError = True

            # Read the content of the file after the editor is closed
            if not encounteredError:
                with open(temp_file.name, 'r', encoding='utf-8') as f:
                    final_content = f.read().strip()

        # Clean up the temporary file
        os.remove(temp_file.name)

        i.ds = Stack(*rest, Stack(*[str(line) for line in final_content.splitlines()]))
        i.cs = Stack(*rcs)
        return True

class Step(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "step":
            return False
        i.cs.pop(0)
        if not i.make_step():
            i.print_error(f"No applicative rules found.")
        return True

class Continue(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "continue":
            return False
        i.cs.pop(0)
        while i.make_step():
            pass
        return True

class Status(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "status":
            return False
        i.cs.pop(0)
        i.log_state()
        return True

class HaltRequest(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not (i.cs.peek() == "exit" or i.cs.peek() == "quit" or i.cs.peek() == ":q"):
            return False
        i.cs.pop(0)
        i.halt = True
        return True

class AddToRuleSet(NativeRule):
    def execute(i: Interpreter):
        if i.cs == []:
            return False

        cw, *rcs = i.cs
        if not cw == "add-rule":
            return False

        if i.ds == []:
            i.print_error("No rule description given.")
            return False

        *rds, ruleDesc = i.ds

        if not isinstance(ruleDesc, str):
            return False

        err, rule = RuleParser.parse(ruleDesc)
        if err:
            i.print_error(err.msg)
            return False
        err = i.ruleset.add(rule)
        if err:
            i.print_error(err.msg)
            return False

        i.ds = Stack(*rds)
        i.cs = Stack(*rcs)
        return True

class RedisoverNativeRules(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "rediscover":
            return False
        i.discover_native_rules()
        i.cs.pop(0)
        return True

class Write(NativeRule):
    # TODO should probably also write the rule native rules as comments into
    # the ruleset. Just for information, that some rules might not be
    # available. Sharing the ruleset-file.
    def execute(i: Interpreter):
        try:
            csw, *rcs = i.cs
            *rds, path = i.ds
        except ValueError:
            return False

        if not (csw == "write" and isinstance(path, str)):
            return False

        try:
            with open(path, "w") as file:
                file.write(str(i.ruleset))
        except FileNotFoundError:
            i.print_error(f"File not found: {path}")
            return False
        except PermissionError:
            i.print_error(f"Permission denied to write file: {path}")
            return False
        except IOError as e:
            i.print_error(f"An error occurred while writing the file: {e}")
            return False

        i.ds = Stack(*rds)
        i.cs = Stack(*rcs)
        return True

class ShowHelp(NativeRule):
    def execute(i: Interpreter):
        try:
            csw, *rcs = i.cs
        except ValueError:
            return False

        if not csw == "help":
            return False

        help = ("\n").join(["Native Rules:", *[f"{rule.name()} {rule.description()}" for rule in i.native_rules]])
        i.print(help)
        i.cs = Stack(*rcs)
        return True

# i.print(
# """
# Native Rules:
# ?                       Shows this help.
# exit                    Quits the program.
# step/enter              Try next execution step.
# continue                Continues rule evaluation.
# status                  Shows current evaluation state.
# rules                   Shows all current rules.
# + <Rule Description>    Add rule to current ruleset.
# - <Rule Description>    Remove rule from current ruleset. (Not yet implemented)
# edit                    Open the current ruleset within an editor and load it on save.
# save <path>             Save the current ruleset into the given file.
# load <path>             Replaces the current ruleset with the one in the given file.
# append ruleset <path>   Load the given ruleset into the current one.
# rediscover              Rediscover native rules.
# """)
