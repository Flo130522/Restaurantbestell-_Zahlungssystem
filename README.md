# Restaurant-Bestelltool
Das Restaurant "golden seagull" benötigt ein Programm zur Abwicklung von Bestellungen im 
Restaurant und beauftragt euch als selbstständiges, kleines Developer-Team mit der 
Entwicklung der Software. Zusammen habt ihr folgende Anforderungen ausformuliert:

  a. Eine Speisekarte sollte im `.csv` Format abgelegt werden und als DataFrame 
  eingelesen werden. Die Speisen-Nummer soll der Zeilen-Index sein. Mit einer 
  Funktion soll die Speisekarte geladen werden. Mit einer anderen Funktion soll 
  man auch die Speisekarte anzeigen können.

  b. Die Liste der Bestellungen soll ebenfalls in einem DataFrame festgehalten 
  werden. Jede Bestellung soll eine ID, ein Datum, eine Tischnummer, SpeiseID, 
  Menge und Status enthalten. Man soll mit einer Funktion in der Lage sein, neue 
  Bestellungen zu erzeugen, und dabei die Tischnummer sowie mehrere 
  SpeiseIDs mit zugehörigen Mengen eingeben können. Das Datum, die ID, und 
  der Status "offen" sollen beim Erstellen automatisch vergeben werden. Es soll 
  durch die Erstell-Funktion ein DataFrame mit Zeilen für jede Speise der 
  Bestellung erzeugt werden. Dieses DataFrame soll an die Gesamtliste der 
  Bestellungen angefügt werden.
  
  c. Datenvalidierung ist hier sehr wichtig! Eine Funktion sollte Bestellungen prüfen, 
  und True zurückgeben, wenn alle Gerichte in der Speisekarte sind, sonst False. 
  Jede neue Bestellung sollte überprüft werden und Fehler entsprechend 
  behandelt werden, bevor die neue Bestellung zur Gesamtliste hinzugefügt wird.
  d. Man soll per Funktion in der Lage sein Bestellungen zu stornieren. Dabei soll 
  der Bestellstatus in der Liste auf "storno" gesetzt werden. 
  
  e. Mit einer Bezahlfunktion soll der Bestellstatus der Bestellung auf "Bezahlt" 
  gesetzt werden und eine Rechnung auf dem Bildschirm ausgegeben werden. 
  Die Rechnung umfasst die Gerichte, Nettopreis, Menge, MwSt., Bruttopreis, 
  sowie evtl. Trinkgeld. Die Preise der Gerichte sollten aus der Speisekarten Datei 
  erhältlich sein.

_Das bildet das Grundgerüst der Bestell-App. Wie immer können beliebige Zusatzfunktionen 
und Details eingebaut werden (z.B. logging, Bestellhistorie, Bestellstatistiken, 
Umsatzzahlen...). Auch das Interface ist wieder frei wählbar – Ob Kommandozeile, GUI, 
Notebook oder Widgets, oder als eigenständiges Modul. Als Abschluss-Präsentation eignet
sich eine live Demonstrationen zu eurer PowerPoint. Viel Erfolg!_
