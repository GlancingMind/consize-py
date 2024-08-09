#TODO ersetzte \emdash durch entsprechenden Wert.

# Consize auf Basis eines Umschreibsystems

## Übersicht

Dieser Bericht befasst sich &mdash; wie der Titel schon andeutet &mdash; mit der konkreten Implementierung der Programmiersprache Consize, auf Basis eines formalen Umschreibsystems, welches im Anhang B von [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf) beschrieben ist. Im ersten Teil des Berichtes wird ein kurzer Überblick über die Sprache und Implementierung von Consize gegeben. Es wird Argumentiert, dass sowohl die Implementierung von, als auch die Entwicklung mit konkatenativen Programmiersprachen, durch die Verwendung eines formalen Umschreibsystems deutlich vereinfacht werden kann.

Anschließend wird im Abschnitt [TODO] auf die Syntax und Semantik des umgesetzten Umschreibsystems eingegangen, bevor schließlich dessen Implementierung im Abschnitt [TODO] beschrieben wird. Zuletzt werden zukünftige Verbesserungen vorgestellt (Abschnitt [TODO]), sowie der aktuelle Projektstand nochmals kurz zusammengefasst.


# Was ist Consize &mdash; Ein sehr kurzer Überblick

Consize ist eine Programmiersprache, welche die funktionalle [konkatenative Programmierung](https://en.wikipedia.org/wiki/Concatenative_programming_language) umsetzt. Anders als in gängigeren Programmiersprachen, werden in konkatenativen Programmiersprachen Funktionen nicht aufeinander angewandt, sondern konkateniert.

Dies führt zu einem völlig anderen Programmierstil, als wie jener von applikativen Programmiersprachen &mdash; wie etwar Java &mdash;, in welchen die Funktionsanwendung einer Funktion $f$ auf einer Funktion $g$ üblicherweiße wie folgt aussieht: $f(g(x))$. In Consize hingegen, sähe die selbe Funktionsanwendung folgendermaßen aus: $x g f$.

Im Prinzip funktioniert Consize auf einer Stapelverarbeitungsmachine (die Consize-VM), welche konzeptionell ein Callstack und einen Datastack umfasst. Beide Stapel enthalten sogenannte Wörter. Ein Wort kann ein Zeichen (`foobar`,`42`,`221B`), ein andere Stapel (`[ ]`,`[ 1 2 3 ]`) oder ein Wörterbücher `{ foo bar }` sein. Wörter, welche auf dem Datastack abgelegt sind, werden von der VM als reine Daten betrachtet, während Wörter, welche auf dem Callstack liegen von der Consize-VM interpretiert werden und ggf. einen definierten Effekt haben. Bspw. umfasst die Consize-VM einen vordefinieren Wortschatz von 56 primitiven Wörtern [siehe Quellcode](https://github.com/denkspuren/consize/blob/master/src/consize.clj) und deren (Stapel)-Effekte. Eines dieser Wörter wäre bspw. `dup`. Es sei angenommen, `dup` läge als oberstes Element auf dem Callstack, so wird die Consize-VM, das Wort `dup` im Wörterbuch der VM nachgeschlagen. Befindet sich zu `dup` ein Eintrag im Wörterbuch, wird der damit assoziierte Effekt eintreten \emdash sofern dessen Vorbedingungen erfüllt sind. Im Falle von `dup` wäre der Stapeleffekt folgender: `(x -- x x)`, woebi linke Seite von `--` den Zustand des Datenstapels vor, und die rechte Seite den Zustand nach der Ausführung von `dup` beschreibt. `(x -- x x)` bedeutet demnach soviel wie, "Nehme das oberste Wort vom Datenstapel und lege diesen, sowie ein duplikat des Wortes auf dem Datenstapel zurück". Die Vorbedingung wäre hierbei, dass sich zwangsweise ein Wort auf dem Datenstapel, vor der unmittelbaren Ausführung von `dup`, befinden muss.

Nun ist `dup` alleine nicht ausreichend, um ein vollständiges Programm zu beschreiben. Es wird ein Mechanismus benötigt, um eigene Wörter und deren Effekte zu kodieren. Bspw. wie es in anderen Programmiersprachen auch üblich ist, Funktionen zu konkatenieren, um komplexeres Verhalten zu beschreiben oder von diesem zu abstrahieren. Daher bietet die Consize-VM die Möglichkeit das interne Wörterbuch, um eigene/neue Wörter zu erweitern. Dazu werden diese Wörter aus der konkatenation der bestehenden Wörter gebildet \emdash wie es auch unter gängigen Programmiersprachen mit Funktionen der Fall ist. Bspw. lässt sich das Wort `unpush` mit den Stapeleffekt `( [ itm & stk ] -- stk itm )` aus einer konkatenation folgender primitiver Wörter bilden: `dup pop swap top`.

Angenommen die obige Definition von `unpush` wäre im aktuellen Wörterbuch der Consize-VM vorhanden und `unpush` wäre das oberste Element auf dem Callstack. Dann würde die Consize-VM die Wörter `dup`,`pop`,`swap` und `top` auf den Callstack legen, so dass sie (wie hier angegeben) von links nach rechts einzeln Interpretiert und ausgeführt werden. Sprich zuerst würde `dup` ausgeführt werden, dann `pop` usw. Sollte die ausführung erfolgreich sein, bewirkt `unpush`, dass das oberste Element eines Stapels herausgenommen und als oberstes Element auf dem Datenstapel gelegt wird.

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
Zur Veranschaulichung nehmen wir an, dass wir folgenden Datenstapel haben: `... [ 1 2 3 ] [ dup ]`, auf dem dessen `each` angewandt wird. Die Folge ist, dass `dup` auf `1`,`2` und `3` angewandt wird. Der Datenstapel nach `each` wäre entsprechend: `... 1 1 2 2 3 3`. Für Ungeübte wird die Definition von `each` schwer zu durchdringen sein. Die Stapeleffektdokumentation hilft hierbei auch nur bedingt \emdash Wären Sie auch darauf gekommen, dass die Elemente nicht mehr in einem Stapel liegen?



welche sich aus einem sehr kleinen Sprachkern zusammensetzt. Ihre Implementierung umfasst lediglich 160 Zeilen (mit Kommentaren) Clojure Code.


# Pattern-Matching: Eine Stapeleffekt-Notation für Menschen


trotz bzw. wegen ihrer syntaktischen Kompaktheit, um einiges schwieriger ist

# Quellen:

- [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf)
- Sowie alle verlinkten Seiten in diesem Bericht. [TODO]
