
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

    # # # This rule is ambigious
    # # "[ @S1 ] [ @S2 ] | concat -> [ @S1 @S2 ]",

    # "[ @S ] [ ] | concat -> [ @S ]",
    # "[ @S ] [ #H @T ] | concat -> [ @S #H ] [ @T ] | concat",

    # # "[ #H @T ] [ @S ] | concat -> [ @T ] [ @S ] | concat \ #H push",
    # # "[ ] [ @S ] | concat -> [ @S ]",

    # # Escape the word, which means the word is not interpreted on the callstack,
    # # therefore moved to the datastack.
    # "\ #H -> #H",

    # # Move stacks/quatation which are on the callstack over to the datastack
    # "| [ @T ] -> [ @T ]",

    # # Reverse rules
    # # "[ ] | reverse -> [ ]",
    # # "[ #H @T ] | reverse -> [ @T ] | reverse [ #H ] concat",

    # # "[ ] | reverse -> [ ]",
    # # "[ @H #T ] | reverse -> [ @H ] | reverse \ #T push",

    # "[ ] | reverse -> [ ]",
    # "[ @H #T ] | reverse -> [ #T ] [ @H ] | reverse concat",

    # # Dictionary rules
    # "[ @KVP ] | mapping -> { @KVP }",
    # "{ @KVP } | unmap -> [ @KVP ]",

    # "{ } | keys -> [ ]",
    # "{ #K #V @R } | keys -> [ #K ] [ @R ] | keys concat",

    # "#V #K { } | assoc -> { #K #V }",
    # "#V #K { #K #V2 @RKVP } | assoc -> { #K #V }",
    # "#V #K { #K2 #V2 @RKVP } {  } | assoc -> #K #V { @RKVP } { #K2 #V2 } ",
    # "#V #K { #K2 #V2 @RKVP } | assoc -> #K #V { @RKVP } { #K2 #V2 } ",
    # # Find entry and remove it, then add new entry

    # "#K { } #DEFAULT | get -> #DEFAULT",
    # "#K { @KVPs1 } { @KVPs2 #K #V } #DEFAULT | get -> #V",
    # "#K { @KVPs1 } { @KVPs2 #K2 #V } #DEFAULT | get -> #K { @KVPs1 #K2 #V } { @KVPs2 } #DEFAULT | get",
    # "#K { @KVPs #K #V } #DEFAULT | get -> #V",
    # "#K { @KVPs #K2 #V } #DEFAULT | get -> #K { #K2 #V } { @KVPs } #DEFAULT | get",

    "#K { } #DEFAULT | get -> #DEFAULT",
    "#K { @KVPs #K #V } #DEFAULT | get -> #V",
    "#K { @KVPs #K2 #V } #DEFAULT | get -> #K { @KVPs } #DEFAULT | get"
)
