#TODO ersetzte \emdash durch entsprechenden Wert.

# Consize auf Basis eines Umschreibsystems

## Übersicht

Dieser Bericht befasst sich &mdash; wie der Titel schon andeutet &mdash; mit der konkreten Implementierung der Programmiersprache Consize, auf Basis eines formalen Umschreibsystems, welches im Anhang B von [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf) beschrieben ist. Im ersten Teil des Berichtes wird ein kurzer Überblick über die Sprache und Implementierung von Consize gegeben. Es wird Argumentiert, dass sowohl die Implementierung von, als auch die Entwicklung mit konkatenativen Programmiersprachen, durch die Verwendung eines formalen Umschreibsystems deutlich vereinfacht werden kann.

Anschließend wird im Abschnitt [TODO] auf die Syntax und Semantik des umgesetzten Umschreibsystems eingegangen, bevor schließlich dessen Implementierung im Abschnitt [TODO] beschrieben wird. Zuletzt werden zukünftige Verbesserungen vorgestellt (Abschnitt [TODO]), sowie der aktuelle Projektstand nochmals kurz zusammengefasst.


# Was ist Consize &mdash; Ein sehr kurzer Überblick

Consize ist eine Programmiersprache, welche die funktionalle [konkatenative Programmierung](https://en.wikipedia.org/wiki/Concatenative_programming_language) umsetzt. Anders als in gängigeren Programmiersprachen, werden in konkatenativen Programmiersprachen Funktionen nicht aufeinander angewandt, sondern konkateniert.

Dies führt zu einem völlig anderen Programmierstil, als wie jener von applikativen Programmiersprachen &mdash; wie etwar Java &mdash;, in welchen die Funktionsanwendung einer Funktion $f$ auf einer Funktion $g$ üblicherweiße wie folgt aussieht: $f(g(x))$. In Consize hingegen, sähe die selbe Funktionsanwendung folgendermaßen aus: $x g f$.

Im Prinzip funktioniert Consize auf einer Stapelverarbeitungsmachine (die Consize-VM), welche konzeptionell ein Callstack und einen Datastack umfasst. Beide Stapel enthalten sogenannte Wörter. Ein Wort kann ein Zeichen (`foobar`,`42`,`221B`), ein andere Stapel (`[ ]`,`[ 1 2 3 ]`) oder ein Wörterbücher `{ foo bar }` sein. Wörter, welche auf dem Datastack abgelegt sind, werden von der VM als reine Daten betrachtet, während Wörter, welche auf dem Callstack liegen von der Consize-VM interpretiert werden und ggf. einen definierten Effekt haben. Bspw. umfasst die Consize-VM einen vordefinieren Wortschatz von 56 primitiven Wörtern [siehe Quellcode](https://github.com/denkspuren/consize/blob/master/src/consize.clj) und deren (Stapel)-Effekte. Eines dieser Wörter wäre bspw. `dup`. Es sei angenommen, `dup` läge als oberstes Element auf dem Callstack, so wird die Consize-VM, das Wort `dup` im Wörterbuch der VM nachgeschlagen. Befindet sich zu `dup` ein Eintrag im Wörterbuch, wird der damit assoziierte Effekt eintreten \emdash sofern dessen Vorbedingungen erfüllt sind. Im Falle von `dup` wäre der Stapeleffekt folgender: `(x -- x x)`, woebi linke Seite von `--` den Zustand des Datenstapels vor, und die rechte Seite den Zustand nach der Ausführung von `dup` beschreibt. `(x -- x x)` bedeutet demnach soviel wie, "Nehme das oberste Wort vom Datenstapel und lege diesen, sowie ein duplikat des Wortes auf dem Datenstapel zurück". Die Vorbedingung wäre hierbei, dass sich zwangsweise ein Wort auf dem Datenstapel, vor der unmittelbaren Ausführung von `dup`, befinden muss.



 und Werte werden als Worte auf einen Stapel abgelegt und interpretiert. Dazu hat Consize ein Wörterbuch, indem bekannte Wörter abgelegt sind und deren Effekte. Bspw. gibt es in Consize das Wort `dup`, welches folgenden Stapeleffekt hat: `(x -- x x)`. Was soviel bedeutet wie, "Nehme den obersten Wert vom Stapel und lege diesen, sowie ein duplikat des Wertes auf dem Datenstapel".


Consize basiert dabei, wie viele konkatenative Programmiersprachen auch, auf einer Stapelverarbeitung.

Eine Ursache des konkatenativen Programmierstils ist, dass bspw. keine Namensbindung mehr benötigt wird.

Diese Art der Programmierung hat ihre Vor- und Nachteile, welche hier - aus Kontextgründen - nicht weiter beschrieben werden. All


welche sich aus einem sehr kleinen Sprachkern zusammensetzt. Ihre Implementierung umfasst lediglich 160 Zeilen (mit Kommentaren) Clojure Code.





trotz bzw. wegen ihrer syntaktischen Kompaktheit, um einiges schwieriger ist

# Quellen:

- [Konkatenative Programmierung mit Consize](https://github.com/denkspuren/consize/blob/master/doc/Consize.pdf)
- Sowie alle verlinkten Seiten in diesem Bericht. [TODO]
