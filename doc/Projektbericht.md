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

Wollen wir Regeln wie das Verhalten von `clear` beschreiben können muss `=>` anstelle von `->` verwendet werden. Mit `=>` wird ausgedrückt, dass keine @-Matcher implizit hinzugefügt werden sollen. Damit wäre die korrekte Regel für `clear`: `@RDS | clear @RCS => | @RCS`.



Wir können jetzt schon erkennen, dass `dup` ein Element auf dem Datastack erwartet und, dass nach `dup` dieses Element auf dem Datastack zweimal vorkommt.

Diese Notation, welche auf einem Mustererkennungssystem beschrieben, welches
welche sich aus einem sehr kleinen Sprachkern zusammensetzt. Ihre Implementierung umfasst lediglich 160 Zeilen (mit Kommentaren) Clojure Code.
trotz bzw. wegen ihrer syntaktischen Kompaktheit, um einiges schwieriger ist

# Quellen:

- [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf)
- Sowie alle verlinkten Seiten in diesem Bericht. [TODO]
