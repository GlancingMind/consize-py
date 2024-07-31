
from RuleParser import RuleParser
from RuleSet import RuleSet

CONSIZE_RULE_SET = RuleSet(
    RuleParser(),
#    "#X #Y | swap -> #Y #X",
#    "#X | dup -> #X #X",
#    "#F | drop -> ",
#    "#X #Y #Z | rot -> #Z #X #Y",
#
#    "#X #X | equal? -> t",
#    "#X #Y | equal? -> f",
#
#    "#X #X | identical? -> t",
#    "#X #Y | identical? -> f",
#
#    "emptystack -> [ ]",
#    "[ @S ] #X | push -> [ #X @S ]",
#
#    "[ #H @T ] | top -> #H",
#    "[ ] | top -> nil",
#    "nil | top -> nil",
#
#    "[ #H @T ] | pop -> [ @T ]",
#    "[ ] | pop -> [ ]",
#
#    "[ ] | unpush -> [ ] nil",
#    "[ #H @T ] | unpush -> [ @T ] #H",
#
#    # # This rule is ambigious
#    # "[ @S1 ] [ @S2 ] | concat -> [ @S1 @S2 ]",
#
#    "[ @S ] [ ] | concat -> [ @S ]",
#    "[ @S ] [ #H @T ] | concat -> [ @S #H ] [ @T ] | concat",
#
#    # "[ #H @T ] [ @S ] | concat -> [ @T ] [ @S ] | concat \ #H push",
#    # "[ ] [ @S ] | concat -> [ @S ]",
#
#    # # Escape the word, which means the word is not interpreted on the callstack,
#    # # therefore moved to the datastack.
#    "\ #H -> #H",
#
#    # # Move stacks/quatation which are on the callstack over to the datastack
#    "| [ @T ] -> [ @T ]",
#
#    # # Reverse rules
#    # "[ ] | reverse -> [ ]",
#    # "[ #H @T ] | reverse -> [ @T ] | reverse [ #H ] concat",
#
#    # "[ ] | reverse -> [ ]",
#    # "[ @H #T ] | reverse -> [ @H ] | reverse \ #T push",
#
#    "[ ] | reverse -> [ ]",
#    "[ @H #T ] | reverse -> [ #T ] [ @H ] | reverse concat",

    # # Dictionary rules
    # "[ @KVP ] | mapping -> { @KVP }",
    "{ @KVP } | unmap -> [ @KVP ]",

#    "{ } | keys -> [ ]",
#    "{ #K #V @R } | keys -> [ #K ] [ @R ] | keys concat",
#
#    # "#V #K { } | assoc -> { #K #V }",
#    # "#V #K { #K #V @KVPs #K #OLD_VAL } | assoc -> { #K #V @KVPs }",
#    # "#V #K { #K #V @KVPs #K2 #V2 } | assoc -> #V #K { #K #V #K2 #V2 @KVPs } | assoc",
#    # "#V #K { @KVPs } | assoc -> #V #K { #K #V @KVPs } | assoc",
#
#    "#K { } #DEFAULT | get -> #DEFAULT",
#    "#K { @KVPs #K #V } #DEFAULT | get -> #V",
#    "#K { @KVPs #K2 #V } #DEFAULT | get -> #K { @KVPs } #DEFAULT | get",
)
