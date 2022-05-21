# LDAP GitLab Sync

Dieses Script synchronisiert Benutzer:innen aus einem LDAP-Server mit Benutzer:innen in GitLab-Gruppen.

## Vorbereitung
Für dieses Script wird installiertes Python3 und Poetry vorausgesetzt.

Mit ```poetry install``` können alle nötigen Abhängigkeiten installiert werden.

## Konfiguration
Es muss eine .env angelegt werden. Eine Vorlage hierfür ist .env.template.

## Nutzung
Mit ```poetry run sync --help``` kann die Hilfe des Scripts angezeigt werden.
