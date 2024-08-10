#TODO ersetzte \emdash durch entsprechenden Wert.
#TODO Achte darauf, den Begriff Umschreibsystem nicht falsch zu verwenden. Consize ist auch schon ein umschreibsystem.
#TODO Verwende entweder Datastack oder Datenstapel, aber nicht beides und Diagramm verwendes DS und CS, sollte Englisch verwenden.

# Implementierung von Consize mittels eines Pattern-Matching-Systems

## Übersicht

Dieser Bericht befasst sich &mdash; wie der Titel schon andeutet &mdash; mit der konkreten Implementierung der Programmiersprache Consize, auf Basis eines formalen Umschreibsystems, welches im Anhang B von [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf) beschrieben ist. Im ersten Teil des Berichtes wird ein kurzer Überblick über die Sprache und Implementierung von Consize gegeben. Es wird Argumentiert, dass sowohl die Implementierung von, als auch die Entwicklung mit konkatenativen Programmiersprachen, durch die Verwendung eines formalen Umschreibsystems deutlich vereinfacht werden kann.

Anschließend wird im Abschnitt [TODO] auf die Syntax und Semantik des umgesetzten Umschreibsystems eingegangen, bevor schließlich dessen Implementierung im Abschnitt [TODO] beschrieben wird. Zuletzt werden zukünftige Verbesserungen vorgestellt (Abschnitt [TODO]), sowie der aktuelle Projektstand nochmals kurz zusammengefasst.


# Was ist Consize &mdash; Ein sehr kurzer Überblick

Consize ist eine Programmiersprache, welche die funktionalle [konkatenative Programmierung](https://en.wikipedia.org/wiki/Concatenative_programming_language) umsetzt. Anders als in gängigeren Programmiersprachen, werden in konkatenativen Programmiersprachen Funktionen nicht aufeinander angewandt, sondern konkateniert.

Dies führt zu einem völlig anderen Programmierstil, als wie jener von applikativen Programmiersprachen &mdash; wie etwar Java &mdash;, in welchen die Funktionsanwendung einer Funktion $f$ auf einer Funktion $g$ üblicherweiße wie folgt aussieht: $f(g(x))$. In Consize hingegen, sähe die selbe Funktionsanwendung folgendermaßen aus: $x g f$.

Im Prinzip funktioniert Consize auf einer Stapelverarbeitungsmachine (die Consize-VM), welche konzeptionell ein Callstack und einen Datastack umfasst. Beide Stapel enthalten sogenannte Wörter. Ein Wort kann ein Zeichen (`foobar`,`42`,`221B`), ein andere Stapel (`[ ]`,`[ 1 2 3 ]`) oder ein Wörterbücher `{ foo bar }` sein. Wörter, welche auf dem Datastack abgelegt sind, werden von der VM als reine Daten betrachtet, während Wörter, welche auf dem Callstack liegen von der Consize-VM interpretiert werden und ggf. einen definierten Effekt haben. Bspw. umfasst die Consize-VM einen vordefinieren Wortschatz von 56 primitiven Wörtern [siehe Quellcode](https://github.com/denkspuren/consize/blob/master/src/consize.clj) und deren (Stapel)-Effekte. Eines dieser Wörter wäre bspw. `dup`. Es sei angenommen, `dup` läge als oberstes Element auf dem Callstack, so wird die Consize-VM, das Wort `dup` im Wörterbuch der VM nachgeschlagen. Befindet sich zu `dup` ein Eintrag im Wörterbuch, wird der damit assoziierte Effekt eintreten \emdash sofern dessen Vorbedingungen erfüllt sind. Im Falle von `dup` wäre der Stapeleffekt folgender: `(x -- x x)`, woebi linke Seite von `--` den Zustand des Datastacks vor, und die rechte Seite den Zustand nach der Ausführung von `dup` beschreibt. `(x -- x x)` bedeutet demnach soviel wie, "Nehme das oberste Wort vom Datastack und lege diesen, sowie ein duplikat des Wortes auf dem Datastack zurück". Die Vorbedingung wäre hierbei, dass sich zwangsweise ein Wort auf dem Datastack, vor der unmittelbaren Ausführung von `dup`, befinden muss.

Nun ist `dup` alleine nicht ausreichend, um ein vollständiges Programm zu beschreiben. Es wird ein Mechanismus benötigt, um eigene Wörter und deren Effekte zu kodieren. Bspw. wie es in anderen Programmiersprachen auch üblich ist, Funktionen zu konkatenieren, um komplexeres Verhalten zu beschreiben oder von diesem zu abstrahieren. Daher bietet die Consize-VM die Möglichkeit das interne Wörterbuch, um eigene/neue Wörter zu erweitern. Dazu werden diese Wörter aus der konkatenation der bestehenden Wörter gebildet \emdash wie es auch unter gängigen Programmiersprachen mit Funktionen der Fall ist. Bspw. lässt sich das Wort `unpush` mit den Stapeleffekt `( [ itm & stk ] -- stk itm )` aus einer konkatenation folgender primitiver Wörter bilden: `dup pop swap top`.

Angenommen die obige Definition von `unpush` wäre im aktuellen Wörterbuch der Consize-VM vorhanden und `unpush` wäre das oberste Element auf dem Callstack. Dann würde die Consize-VM die Wörter `dup`,`pop`,`swap` und `top` auf den Callstack legen, so dass sie (wie hier angegeben) von links nach rechts einzeln Interpretiert und ausgeführt werden. Sprich zuerst würde `dup` ausgeführt werden, dann `pop` usw. Sollte die ausführung erfolgreich sein, bewirkt `unpush`, dass das oberste Element eines Stapels herausgenommen und als oberstes Element auf dem Datastack gelegt wird.

```
-----------------------------------------------------------------
DS vor unpush:  ... [ Moriarty Sherlock Watson ]  | unpush ... CS vor unpush
-----------------------------------------------------------------
DS nach unpush: ... [ Sherlock Watson ] Moriarty  | ...        CS nach unpush
-----------------------------------------------------------------
```

# Stapeleffekte: Notieren, Verstehen und richtig Interpretieren, garnicht so schwer oder...?

Anhand von `unpush` wird ein Problem deutlich. Um `unpush` zu verstehen, muss ein tiefgehendes Verständnis der Effekte von jeden einzelnen Worte, aus dem `unpush` zusammengesetzt ist, vorliegen. Andernfalls ist unklar, was `unpush` tatsächlich macht. Zwar deutet `unpushs` Stapeleffektdokumentation `( [ itm & stk ] -- stk itm )` darauf hin, was passieren sollte, jedoch ist diese Dokumentation nicht für alle Wörter gleich hilftreich. Betrachten wir die Definition von `each`.

```
: each ( seq quot -- ... )
    swap dup empty?
        [ 2drop ]
        [ unpush  -rot over [ call ] 2dip each ]
    if ;
```

Each erwartet auf dem Datastack eine Quotierung $quot$ und darunter einen Stapel mit Wörtern $seq$. Für jedes Element aus $seq$ wird `each` die Quotierung $quot$ anwenden.
Zur Veranschaulichung nehmen wir an, dass wir folgenden Datastack haben: `... [ 1 2 3 ] [ dup ]`, auf dem dessen `each` angewandt wird. Die Folge ist, dass `dup` auf `1`,`2` und `3` angewandt wird. Der Datastack nach `each` wäre entsprechend: `... 1 1 2 2 3 3`. Für Ungeübte wird die Definition von `each` schwer zu durchdringen sein. Die Stapeleffektdokumentation hilft hierbei auch nur bedingt \emdash Wären Sie auch darauf gekommen, dass die Elemente nicht mehr in einem Stapel liegen? Ich hatte das anfangs nicht erwartet.

Diese Problem ist dem Entwickler von Consize bekannt. In der Dokumentation zu Consize [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf) wird daher im Anhang B eine alternative Notation für Stapeleffekte beschrieben, welche einerseits für Menschen verständlicher und andererseits von Maschinen auswertbar ist. Im nachfolgenden Abschnitt wird jene Notation beschrieben.


# Eine Stapeleffekt-Notation für Menschen

Wenn wir uns die Anwendung eines hinreichend komplexen Wortes in Consize betrachten, wird klar, dass ein Word lediglich ersetzt wird, gegen dessen Definition. Welche wieder lediglich aus Wörtern besteht, die wiederum ersetzt werden gegen deren Definition usw. Solange, bis nur noch primitive Wörter vorhanden sind und diese ausgewertet wurden. Demnach, entspricht die Auswertung eines Consize Programms einer Abfolge von Ersetzungsschritten; und damit die Consize-VM im Grunde einem Umschreibsystem.

Die in [Anhang B von Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf) vorgeschlagene Stapeleffekt-Notation beschreibt genau jene einzelne Ersetzungsschritte, welche von der Consize-VM durchgeführt werden. D. h., wie sieht der aktuelle Zustand des Systems vor und nach einem Ersetzungsschritt aus.
Genauer:

1. Wie sieht der Datastack zum Zeitpunkt vor dem Ersetzten eines Wortes aus und
2. wie sieht danach aus; Sowie,
3. Wie sieht der Callstack zum Zeitpunkt vor dem Ersetzten eines Wortes aus und
4. wie sieht der Callstach danach aus.

Betrachten wir wieder das Wort `dup`. In der Stapeleffekt-Notation vom Anhang B, wird `dup` wie folgt beschrieben.

```
#X | dup -> #X #X |
```

Wir nennen einen solchen Ausdruck Regel(-Beschreibung) und lesen wie folgt:

- Alles links von einem Pfeil (`->` oder `=>`), nennen wir Matching-Pattern (M-Pat).
- Alles recht von einem Pfeil (`->` oder `=>`), nennen wir Instantiation-Pattern (I-Pat).

Die Pattern setzten sich wiederum aus zwei Teilen zusammen:

1. Dem Datenstapel-Pattern, welches alles links von einem `|`-Symbol ist und
2. dem Callstack-Pattern, welches alles recht von einem `|`-Symbol.

In Consize können wiederum drei Verschiedene Dinge auf einem Stapel auftauchen: andere Stapel, Wörterbücher und Wörter. Diese werden wie folgt in der Notation ausgedrückt.

- Ein Stapel beginnt mit einer öffnenden `[` und muss mit einer `]` enden \emdash auch hier gilt, dass innerhalb des Stapels wieder Stapel, Wörterbücher und Wörter erscheinen können.
- Ein Wörterbuch beginnt mit einer öffnenden `{` und muss mit einer `}` enden. Es gilt zu beachten, dass sich Wörterbücher von Stapel darin unterscheiden, dass deren Elemente immer Wort-Paare sein müssen, welche wiederum Stapel, Wörterbücher und Wörter sein können. Das heißt, Wörterbücher mit ungerader Anzahl an Elementen (wie etwar `{ a }` oder `{ a b c }`) sind nicht zulassig \emdash wie in Consize auch.
- Alle anderen Zeichen sind Literale, mit Ausnahme von Worten, welche mit einem `#`-Symbol oder `@`-Symbol beginnen. Jene nennen wir Matcher. Bzw. Worte, welche mit einem `#`-Symbol beginnen, nennen wir Hash-Matcher; und Worte, welche mit einem `@`-Symbol beginnen, nennen wir AT-Matcher. Deren Semantik wird noch noch erläuter.

Zuerst muss festgehalten werden, dass die obige Regel beschreibung eine vereinfachte Darstellen (zur Verbesserung der Lesbarkeit) ist. Denn, in dieser werden lediglich Elemente auf den Stapeln angegeben, welche von einen Umschreibschritt betroffen sind. Das wäre einmal das oberste Elemente auf dem Datanstapel und Callstack. Es wird jedoch keine Aussage darüber getroffen, was mit allen anderen Werten auf den Stapeln passiert, noch welches Element das erste auf einem Stapel ist (ist das erste `#X`, oder das zweite auf dem Zielstapel, das oberste Element auf dem neuen Datenstapel?). Dies geschieht implizit. Denn sobald `->` verwendet wird, muss die Regel wie folgt gelesen werden.

```
@RDS #X | dup @RCS -> @RDS #X #X | @RCS
```

Die AT-Matcher `@RDS` und `@RCS` stehen führ alle restlichen Elemente auf dem Datastack bzw. Callstack. Nun können wir sehen, dass das oberste Element vom Datenstapel immer rechts steht, während das oberste Element vom Callstack immer links steht. Außerdem, sehen wir, was mit den anderen Elementen auf dem Stapeln passiert, nachdem die Regel angewandt wurde.
Ein Beispiel. Angenommen wir hätten folgenden Datenstapel `1 2` und den Callstack `dup +`:

```
1 2 | dup +
```

Dann würde der Datenstapel und Callstack nach der Anwendung von `dup` folgendermaßen aussehen:

```
1 2 2 | +
```

Jetzt wird auch die Bedeutung der @- und #-Matcher deutlich. Ein #-Matcher ist im M-Pat ein Platzhalter, der für **ein** beliebiges Element stehen kann. Während ein @-Matcher eine beliebig lange Sequenz von Elementen zusammenfasst. Im obigen Beispiel stand `#X` für das Literal 2 und `@RDS` für alle restlichen Elemente des Datenstapels, also `[ 1 ]`.


Das implizite Hinzufügen von @-Matchern macht die kurzform deutlich einfacher zu lesen, hat jedoch eine erhebliche Konsequenz. Regeln \emdash wie bspw. `clear` \emdash lassen sich nicht mit dieser Ausdrücken. Zur Verdeutlichung: In der vereinfachten Regelnotation würden wir `clear` so beschreiben: `| clear -> |`, was den Eindruck erweckt, dass `clear` den gesamten Datenstapel leert.
In Wirklichkeit besagt die Regel jedoch, dass `clear` kein Element vom Datenstapel erwartet und auch nicht auf dem neuen Datenstapel veränder. Nach der Regeldefinition, wäre `clear` eine [NOP](https://en.wikipedia.org/wiki/NOP_(code)), es macht garnichts. Der Grund hierfür ist das implizite Hinzufügen von `@RDS` und `@RCS`. Die Regel ist: `@RDS | clear @RCS -> @RDS | @RCS`.

Wollen wir Regeln wie das Verhalten von `clear` beschreiben können, muss `=>`, anstelle von `->` verwendet werden. Mit `=>` wird ausgedrückt, dass keine @-Matcher implizit hinzugefügt werden sollen. Damit wäre die korrekte Regel für `clear`: `@RDS | clear @RCS => | @RCS`.

Damit wären die wichtigsten Formalien zur Notation der Umschreibregeln beschrieben. Im folgenden Abschnitt wird darauf eingegangen, wie das beschriebene Pattern-Matching-System in diesem Projekt zur Zeit implementiert ist.

# Auswertung der Umschreibregeln \emdash eine mögliche Implementierung in Python

Wenn wir Consize auf Basis der vorher eingeführten Regeln-Notation beschreiben und maschinell ausführen wollen, benötigen wir einen Interpreter der jene Regeln auswertet. Grundliegend muss dieser lediglich zwei Schritt wiederhohlt anwenden.

1. Finde eine anwendbare Regel und
2. wende jene Regel an.

Für Schritt 1. gibt es verschiedene Ansätze \emdash siehe Abschnitt [Zukünftige Verbesserung](#lastreduktion-beim-finden-von-regeln-anwendbaren-regeln) für andere Ideen. In der vorliegenden Implementierung handelt es sich um einen sehr einfachen Ansatz. Zunächst gehen wir davon aus, dass dem Interpreter ausschließlich korrekte Regeln, in einer für ihn verarbeitbaren Form, vorliegen. Diese Regeln stehen in einem sog. Regelwerk, welches letztlich eine einfache Liste ist. Der Interpreter prüft, sequentiell, für jede Regel aus dem Regelwerk, ob diese Anwendbar ist. Ist dies nicht der Fall, prüft er die Anwendbarkeit der nächsten Regel. Sollte eine Regel anwendbar sein, wird er das Instantiation-Pattern (rechte Seite der Regel) der Regel umsetzten (Schritt 2.) und anschließend wieder vom Anfang des Regelwerks, alle Regeln durchprüfen. Dies wird solange wiederhohlt, bis keine Regel mehr anwendbar ist \emdash was dem Programmende gleichkommt, weil kein Fortschritt mehr erziehlt werden kann. Die Implementierung dieser Schleife und dem Matching sind in den Methoden `make_step` und `run` in der *Interpreter.py* Datei kodiert.

Damit der Interpreter weiß, ob ein Pattern zutrifft, muss er den aktuellen Callstack und Datastack mit den Callstack bzw. Datastack vom M-Pat abgleichen. Auch hier gibt es wieder verschiedene Ansätze. Wir werden uns jetzt auf die aktuelle Implementierung fokusieren \emdash für andere Ansätze siehe Abschnitt [Alternative Pattern-Matching Strategien](#alternative-pattern-matching-strategien).

Das Pattern-Matching beginnt an oberster Stelle jeden Stapels und erfolgt rekursiv, bis das Pattern vollständig zutrifft, oder nicht. Trifft ein Pattern nicht zu, wird dies mit $False$ angegeben. Andernfalls, muss aus dem Pattern-Matching ein Zuordnung $Matches$ hervorgehen von allen Werten, die von einem #- oder @-Matcher gematcht wurden \emdash wie wir das bereits im `dup` Beispiel gesehen haben. Der Algorithmus betrachtet das oberste Element von dem zu matchenden Stapel $e_s$ und dem angegeben Pattern $e_p$. Nun gibt es fünf Fälle zu beachten.

- Literal: Ist $e_p$ ein Literal, muss $e_s$ das gleiche Literal sein. Trifft dies zu, wird mit den nächsten Elementen fortgefahren. Andernfalls, trifft das Pattern nicht zu.
- Stapel: Ist $e_p$ ein Stapel, muss $e_s$ auch ein Stapel sein. Trifft dies zu, werden die Stapel miteinander gematcht. Dies geschieht rekursiv. Matcht der Stapel dem gegeben Stapelpattern, wird mit den nächsten Elementen fortgefahren.
- Wörterbuch: Ist $e_p$ ein Wörterbuch, muss $e_s$ auch ein Wörterbuch sein. Trifft dies zu, werden beide Wörterbücher miteinander gematcht. Dies geschieht ebenfalls rekursiv. Hier sei angemerkt, dass die aktuelle Implementierung jedes Wörterbuch als eine Liste betrachtet. Dies ist zwar ineffizient, bietet allerdings die Möglichkeit, dass die Notation und Match-Logik zwischen Wörterbücher und Stapeln nicht unterscheiden.
- #-Matcher: Ist $e_p$ ein #-Matcher, wird $e_p$ mit $e_s$ assoziiert. D. h. sie werden in $Matches$ abgelegt, sofern für $e_p$ noch keine Zuordnung in $Matches$ existier. Existiert bereits eine Zurodnung, muss $e_s$ dem bereits zugeordneten Wert gleichen. Andernfalls, trifft das Pattern nicht zu.
- @-Matcher: Ist $e_p$ ein @-Matcher, werden die Lesereihenfolge der Elemente im Pattern, sowie dem zu matchenden Stapel umgekehrt und das matching weiter forgeführt. Bis wieder zum @-Matcher angekommen wurde, woraufhin die verbleibenden Elemente dem @-Matcher zugeordnet werden.

Der @-Matcher ist etwas kompliziert. Die Implementierung ist so umgesetzt, weil bspw. folgendes Pattern erlaubt sein: `#LAST 2 @MID #FIRST`. Hier würde `@MID` alle Elemente zwischen dem ersten und letzten Element eines Stapels zugeordnet bekommen. Wenn der @-Matcher einfach den kompletten Rest eines Stapels matchen würde, wäre er Greedy und der obige Ausdruck nicht mehr möglich. Nutzten wir das Pattern auch nochmal, um die Implementierung des Algorhtmus genauer zu verdeutlichen. Dazu nehmen wir an, dass das Pattern auf den Datastack `1 2 3 4` gematcht wird. Der Algorithmus wird zuerst `#FIRST` als $e_p$ zum matchen wählen, weil bei Datenstapel das erste Element rechts steht. Er findet auf den zu matchenden Stapel die `4` und ordnet damit `#FIRST` dem Element `4` zu und entfernt diesen vom Stapel. Nun folgt der @-Matcher `@MID`. Zuerst wird geprüft, ob bereits eine Zuordnung für `@MID` existiert, ist dies der Fall, beenden wird das Pattern-Matching und geben alle Zurodnungen/matches zurück. Andernfalls, wird diesem zunächst eine Referenz auf dem zu matchenden Stapel zugeordnet: Also `@MID=[ 1 2 3 ]`. Nun wird die Leserichtung gewechselt, auf links-nach-rechts. D. h. der nächste Matcher ist `#END`. Diesem wird das Element `1` zugewiesen und `1` anschließend vom Stack runtergenommen. Weil, `@MID` lediglich eine Referenz hat, sieht die zuordnung nun folgendermaßen aus: `@MID=[ 2 3 ]`. Im nächsten Schritt wird das Literal `2` gematcht; welches mit dem Literal `2` auf dem Datenstapel matcht. Die Folge: Beide Literale werden vom Stapel runtergenommen, womit sich `@MID` erneut aktualisiert auf `@MID=[ 3 ]`. Nun sind wir erneut bei `@MID` angekommen. Da bereits eine Zurodnung für `@MID` existiert, wird hier abgebrochen und alle Zuordnungen zurückgeliefert.

Beachte: Die derzeitige Implementierung setzt voraus, dass es niemals mehr als nur einen @-Matcher innerhalb eines M-Pat gibt. Andernfalls wären folgende Ausdrücke möglich: `[ @LEFT 3 @RIGHT ]`, welche nicht zulässig sind, weil es mehrere Lösungen gibt. So könnte bei einem Datenstapel mit den Elementen `1 3 3 3 7`, `@LEFT` die Literale `1 3 3` oder `1 3` oder nur `1` zugeordnet bekommen. Das Matching soll aber immer nur eine eindeutige Lösung erzeugen.

Dazu muss die Auswertung der Regeln festgelegt werden. Im Grund Prinzip l

Hierfür gibt es verschiedene

 In der aktuellen Implementierung besitzt der Interpreter einen dedizierten Data- und Callstack.


 dass es mehrere solcher Regeln geben wird. Diese Regeln werden in einem Regelwerk zusammengefasst.





Diese Notation, welche auf einem Mustererkennungssystem beschrieben, welches
welche sich aus einem sehr kleinen Sprachkern zusammensetzt. Ihre Implementierung umfasst lediglich 160 Zeilen (mit Kommentaren) Clojure Code.
trotz bzw. wegen ihrer syntaktischen Kompaktheit, um einiges schwieriger ist

# Zukünftige Verbesserungen

## Lastreduktion beim finden von Regeln anwendbaren Regeln

Anstelle jede Regel einzeln auf ihre Anwendbarkeit zu prüfen, können viele Regeln bereits vorzeitig ausgeschlossen werden, indem zunächst ausschließlich der Callstack betrachtet wird. Sollten umsetzbar sein:

### 1. Hashmap mit Chaining: Matche auf callstack, um alle Regeln

Konsequenz: Auf callstack darf immer nur eine bestimmte Anzahl an Elementen liegen, um matching entsprechend durchzuführen.

### 2. Baum

## Alternative Pattern-Matching Strategien

### Pattern-Matching mit Python unpack-Operationen

### Pattern-Matching via Reguläre Ausdrücke

# Quellen:

- [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf)
- Sowie alle verlinkten Seiten in diesem Bericht. [TODO]
