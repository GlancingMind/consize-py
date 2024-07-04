
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

    "[ ] | reverse -> [ ]",
    "[ #H @T ] | reverse -> [ @T ] | reverse [ #H ] concat"
    # TODO reverse is applied only on [ @T ], but currently recursive reverse is
    # applied on "[ #H ]" as this is it element preceeding reverse!
    # Might need to treat call- and datastack separate!

    # TODO fuhre : als regel ein, so dass neue Regeln ins Regelwerk aufgenommen werden können.
)
