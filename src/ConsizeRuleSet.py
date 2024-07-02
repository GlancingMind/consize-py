
from RuleParser import RuleParser
from RuleSet import RuleSet

CONSIZE_RULE_SET = RuleSet(
    RuleParser(),
    "#X #Y | swap -> #Y #X",
    "#X | dup -> #X #X",
    "#F | drop -> ",
    "#X #Y #Z | rot -> #Z #X #Y",

    "#X #X | equal? -> t",
    "#X #Y | equal? -> f",

    "#X #X | identical? -> t",
    "#X #Y | identical? -> f",

    "emptystack -> [ ]",
    "[ ] #X | push -> [ #X ]",

    "[ #H @T ] | top -> #H",
    "[ ] | top -> nil",
    "nil | top -> nil",

    "[ ] | unpush -> [ ] nil",
    "[ #H @T ] | unpush -> [ @T ] #H"
    # "-rot -> rot rot rot"
    # TODO fuhre : als regel ein, so dass neue Regeln ins Regelwerk aufgenommen werden können.
)
