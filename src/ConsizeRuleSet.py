import glob
from ExternalWords import ExternalWordModules, ExternalWords
from RuleParser import RuleParser
from RuleSet import RuleSet

# TODO might want to parse a file or accept this rules in the terminal.
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

    # "[ @S1 ] [ @S2 ] | concat -> [ @S1 @S2 ]",

    "[ @S ] [ ] | concat -> [ @S ]",
    "[ @S ] [ #H @T ] | concat -> [ @S #H ] [ @T ] | concat",

    # "[ #H @T ] [ @S ] | concat -> [ @T ] [ @S ] | concat \ #H push",
    # "[ ] [ @S ] | concat -> [ @S ]",

    # # Escape the word, which means the word is not interpreted on the callstack,
    # # therefore moved to the datastack.
    "\ #H -> #H",

    # # Move stacks/quatation which are on the callstack over to the datastack
    "[ @T ] -> [ @T ]",

    # # Reverse rules
    "[ ] | reverse -> [ ]",
    "[ #H @T ] | reverse -> [ @T ] | reverse [ #H ] concat",

    # "[ ] | reverse -> [ ]",
    # "[ @H #T ] | reverse -> [ @H ] | reverse \ #T push",

    # "[ ] | reverse -> [ ]",
    # "[ @H #T ] | reverse -> [ #T ] [ @H ] | reverse concat",

    # # Dictionary rules
    "[ @KVP ] | mapping -> { @KVP }",
    "{ @KVP } | unmap -> [ @KVP ]",

    "{ } | keys -> [ ]",
    "{ #K #V @R } | keys -> [ #K ] { @R } | keys concat",

    "#V #K { } | assoc -> #V #K { } | assoc'",
    "#V #K { #K  #_  @REM } | assoc -> #V  #K { @REM } | assoc assoc'",
    "#V #K { #K2 #V2 @REM } | assoc -> #V2 #K2 #V #K { @REM } | assoc assoc'",
    "#V #K { @KVPs } | assoc' -> { #K #V @KVPs }",

    "#K { } | dissoc -> { }",
    "#K { #K  #_  @REM } | dissoc -> { @REM }",
    "#K { #K2 #V2 @REM } | dissoc -> #V2 #K2 #K { @REM } | dissoc assoc'",

    "#K { } #DEFAULT | get -> #DEFAULT",
    "#K { @KVPs #K #V } #DEFAULT | get -> #V",
    "#K { @KVPs #K2 #V } #DEFAULT | get -> #K { @KVPs } #DEFAULT | get",

    "{ @M1 } { #K #V @M2 } | merge -> #V #K { @M1 } { @M2 } | merge assoc",
    "{ @M1 } { } | merge -> { @M1 }",

    "@RDS [ @Q ] | call/cc @RCS => [ @RDS ] [ @RCS ] | @Q",
    "@RDS [ @DS ] [ @CS ] | continue @RCS => @DS | @CS",
    "[ @Q ] | call -> | @Q",

    "| load -> | slurp uncomment tokenize",
    "| run -> | load call",

    # Transcribed Prelude
    "@RDS | clear @RCS => | @RCS",

    rules=[
        ExternalWordModules(moduleDir="./src/external-words/modules"),
        ExternalWords(wordScripts=glob.glob("./src/external-words/*"))
    ],
)
