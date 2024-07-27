
from RuleParser import RuleParser
from RuleSet import RuleSet

CONSIZE_RULE_SET = RuleSet(
    RuleParser(),
    # "#X #Y | swap -> #Y #X",
    # "#X | dup -> #X #X",
    # "#F | drop -> ",
    # "#X #Y #Z | rot -> #Z #X #Y",

    # "#X #X | equal? -> t",
    # "#X #Y | equal? -> f",

    # "#X #X | identical? -> t",
    # "#X #Y | identical? -> f",

    # "emptystack -> [ ]",
    # "[ @S ] #X | push -> [ #X @S ]",

    # "[ #H @T ] | top -> #H",
    # "[ ] | top -> nil",
    # "nil | top -> nil",

    # "[ #H @T ] | pop -> [ @T ]",
    # "[ ] | pop -> [ ]",

    # "[ ] | unpush -> [ ] nil",
    # "[ #H @T ] | unpush -> [ @T ] #H",

    "[ @S1 ] [ @S2 ] | concat -> [ @S1 @S2 ]",

    # "[ ] | reverse -> [ ]",
    # "[ @H #T ] | reverse -> [ #T ] [ @H ] | reverse concat",

    # "[ @KVP ] | mapping -> { @KVP }",

    "{ } | unmap -> [ ]",
    "{ #K #V } | unmap -> [ #K #V ] | concat",
    "#K #V } | unmap -> [ #K #V ] @RDS } | unmap concat",
    # Could also add "} {" between elements and then call concat

    # [ #X ]       | word -> #X
    # [ #X #Y ]    | word -> #X #Y builtin-word
    # [ #X #Y @R ] | word -> #X #Y builtin-word @R word

    # TODO fuhre : als regel ein, so dass neue Regeln dynamisch ins Regelwerk aufgenommen werden können.
    # Bspw. diese Wörter wären allerdings nicht:
    #   ": -rot rot rot"
    # Da diese auch so ausgedrückt werden können:
    #   " | -rot -> | rot rot"
    # Eine knappere Syntax wäre aber cooler. Bspw:
    #   "alias -rot -> rot rot" oder
    #   ": -rot -> rot rot"

    # Bräuchte noch ein Wort um arbitären Pythoncode auszuführen.
    # Das wären dann die Devices in Modal.

    # Das geht nicht. : liegt auf dem input stack, nicht auf dem Datastack!
    # => Regel müsste feuern, wenn callstack leer ist...
    # Oder schreibe interpreter um, so dass nur noch ein stack existiert.

    #
)

# defWord = Rule
