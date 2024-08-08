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

# class AddToRuleSet(NativeRule):
#     def execute(i: Interpreter):
#         # TODO if a word is unkown, call read-word, which will move the word
#         # over to the datastack
#         rule = RuleParser.parse(" | ; -> ")
#         matches = rule.matches(i)
#         if not matches:
#             return False

#         rule = matches["@RULE"]
#         i.add_rule1(rule)

#         *rest, wordstack = i.ds
#         i.ds = StackPattern
#         i.cs.pop(0)
#         return True

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
        ccWrd = i.ds.pop()
        ncs = StackParser.parse(ccWrd)
        i.ds = Stack(*i.ds, *ncs)
        return True

class ReplaceCC(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or not i.cs.peek() == "rcc":
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

        i.ds = Stack(*rest, final_content)
        i.cs = Stack(*rcs)
        return True
