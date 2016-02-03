Anforderungen
* Materialien in beliebiger Kombination kombinierbar
* Materialien pro Konfiguration in unterschiedlicher Anzahl auswählbar
* Materialien können anderen Materialien zugeordnet sein
** z.B. stundenplan_alle_gruppen (Stundenplan-Gruppen-PDF)
** Kinder wären z.B. stundenplan_gruppe_1, stundenplan_gruppe_2
** wenn stundenplan_alle_gruppen selektiert wird, dann werden automatisch
   alle zugeordneten Materialien auch selektiert
** jedes der Kinder-Materialien hat eine Seite der PDF zugeordnet
* Konfigurationen auswählbar oft drucken
* Kombinationen/Konfigurationen speichern und verändern können
* Konfigurationen kombinierbar (z.B. conf1 und conf2 enthalten disjunktes
  Subset von Materialien, wodurch sie sich ergänzen)
* Konfiguration kann aus mehreren Konfigurationen zusammengestellt werden
* Teile einer PDF auswählbar als Material (z.B. Stundenplan - Seite(n) xy)
* ausgewählte Materialien zusammenfügen
* zusammengefügte PDF speichern und mit Konfiguration verknüpfen
** wird gleiche Konfiguration erneut ausgewählt und nichts verändert,
   dann kann gleich gedruckt werden
* PDF an ausgewählten Drucker schicken

Phasen
* Auswähl-/Konfigurationsphase
* Mergephase
* Druckphase

Konfigurationsphase
* Konfiguration auswählen
* anpassen
* Konfiguration bei Bedarf speichern (Namen vergeben)

Mergephase
* Konfiguration in eine druckbare PDF überführen
* wenn gespeicherte Konfiguration (Name vorhanden), dann PDF mit dieser verknüpfen

Druckphase
* druckbare PDF mittels lpr drucken

Client
* GUI-Anwendung mittels PyQt
* Auswahl und Selektion passiert hier
* Infos (Konfiguration und Materialien) werden lokal gecached und können mit dem
  Server synchronisiert werden
* gespeicherte Konfigurationen werden an Server gesendet und dort abgelegt
* SSH-Host wird im Client konfiguriert (z.B. nutze Host fbi, welcher in der SSH-Config
  auf rzssh1.informatik.uni-hamburg.de erweitert wird)
** vor der Nutzung des Clients muss man sich einmal per Shell "rauf ssh'en", damit
   der Client ohne Passwort SSH benutzen kann

Server
* nimmt Konfiguration von Client entgegen und legt sie ab
* merged ausgewählte Konfiguration und speichert PDF
* druckt ausgewählte PDF mit angegebenen Optionen
