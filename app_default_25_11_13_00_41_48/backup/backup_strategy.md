# Strategia Backupów Bazy Danych

## Harmonogram backupów

- Pełny backup bazy PostgreSQL wykonywany codziennie o 02:00
- Backup inkrementalny co godzinę

## Retencja backupów

- Pełne backupy przechowywane przez 14 dni
- Backup inkrementalny przez 7 dni

## Procedury backupu

- Backup wykonywany za pomocą `pg_dump` w formacie skompresowanym
- Pliki backupu przechowywane na zewnętrznym serwerze lub w chmurze (np. S3)

## Przywracanie danych

- Przywracanie z pełnego backupu i najnowszego backupu inkrementalnego
- Komenda:
    