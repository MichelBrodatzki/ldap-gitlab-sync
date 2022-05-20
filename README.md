# Referat GitLab Sync

Dieses Script ist die Verbindungsstelle zwischen den Referatsgruppen im LDAP und den Gruppen im GitLab.

## Vorbereitung
Für dieses Script wird installiertes Python3 und Poetry vorausgesetzt.

Mit ```poetry install``` können alle nötigen Abhängigkeiten installiert werden.

## Konfiguration
Es muss eine .env angelegt werden. Eine Vorlage hierfür ist .env.template.

## Nutzung
### Referat und GitLab-Gruppe verbinden
Um die Verbindungen zwischen Referaten und GitLab-Gruppen zu verwalten, kann man ```poetry run referate``` benutzen. Mit dem Flag -h wird hier die Hilfe angezeigt.

### Synchronisierung von LDAP und GitLab
TBA. Sollte dann aber ```poetry run sync``` werden. Und am Besten noch ein --dry-run Flag, damit man den Befehl auch testweise ausführen kann.
