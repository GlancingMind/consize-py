import re

patterns = []

words = re.split(r"\s+", "#F [ #S ] #L")
for word in words:
    if word.startswith("#"):    patterns.append(rf"(?P<H_{word[1:]}>\S+)")
    elif word.startswith("@"):  patterns.append(rf"(?P<T_{word[1:]}>\S|\s)*")
    else:                       patterns.append(re.escape(word))

# TODO Das erwarten von Whitespace (+-Operator) nach einen @-Matcher führt dazu,
#      dass kein Pattern mehr gematcht wird, weil der @-Matcher bereits den
#      Whitespace konsumiert und für den whitespace-Matcher kein Whitespace mehr
#      vorhanden ist. Nach den @-Matcher darf kein Whitespace mehr folgen.
#      Entweder, weil * verwendet wird, oder weil kein Whitespace angehängt wird.
regex = r"\s+".join(patterns)

m = re.match(regex, "A [ C ] Z")
for group in m.groups():
    print(group)

print(m.groupdict())

def subs(matchobj):
    return m.groupdict().get(matchobj.group())

instance = re.sub(r"H_F|H_S|H_L", subs, r"H_F H_F H_L H_S")
print(instance)

# Wieso ist RegEx evtl. doch nicht so gut?
# 1. Brauche named Capture-Groups
# 2. Die Namen von den named Capture-Groups sind (zumindest in Python) nicht
#    frei wählbar, sondern müssen einen gültigen Identifier entsprechen. D.h.
#    Kann # und @ nicht im Namen der Capture-Group haben. Deswegen können die
#    Identifier der Gruppen nicht 1-1 aus der Regelbeschreibung übernommen.
#    Stattdessen wird im regulären Ausdruck H_ für # genommen und T_ für @.
#    Selbe Änderung muss auch für die Subsitution-Patterns vorgenommen werden.
# 3. Beim Substituieren kann in Python eine Funkton übergeben werden, um die
#    entsprechende Subsitution für das gematchte Element durchzuführen. Bei
#    anderen RegEx-Engines wird evtl. kein Funktionsübergabe unterstützt. Das
#    ersetzten muss u.U. anders vorgenommen werden.
# 4. RegExp machen es schwer, das Pattern auf korrektheit zu überprüfen.
#    Bspw. richtige Klammerung oder ob sich Regeln gegenseitig ausschließen.
#    Es müssen demnach nachwievor die Patterns untersucht werden.
