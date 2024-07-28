
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
    "[ @S ] #X | push -> [ #X @S ]",

    "[ #H @T ] | top -> #H",
    "[ ] | top -> nil",
    "nil | top -> nil",

    "[ #H @T ] | pop -> [ @T ]",
    "[ ] | pop -> [ ]",

    "[ ] | unpush -> [ ] nil",
    "[ #H @T ] | unpush -> [ @T ] #H",

    # # This rule is ambigious
    # # "[ @S1 ] [ @S2 ] | concat -> [ @S1 @S2 ]",

    # # "[ @S ] [ ] | concat -> [ @S ]",
    # # "[ @S ] [ #H @T ] | concat -> [ @S #H ] [ @T ] | concat",

    "[ #H @T ] [ @S ] | concat -> [ @T ] [ @S ] | concat \ #H push",
    "[ ] [ @S ] | concat -> [ @S ]",
    "\ #H -> #H",

    "[ ] | reverse -> [ ]",
    "[ @H #T ] | reverse -> [ #T ] [ @H ] | reverse concat",

    "[ @KVP ] | mapping -> { @KVP }",
    "{ @KVP } | unmap -> [ @KVP ]",

    "{ } | keys -> [ ]",
    "{ #K #V @R } | keys -> [ #K ] [ @R ] | keys concat",
)
