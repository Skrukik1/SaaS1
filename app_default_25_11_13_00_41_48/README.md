# Kompleksowa Aplikacja Backend + Discord Bot + Frontend

## Opis projektu
Projekt to rozbudowana aplikacja webowa z backendem opartym o FastAPI, botem Discord integrującym się z backendem oraz opcjonalnym frontendem React. Aplikacja oferuje:
- Uwierzytelnianie OAuth2 z JWT i RBAC (Role-Based Access Control)
- Zarządzanie użytkownikami i rolami
- Logowanie zdarzeń i audyt
- Międzynarodowość (i18n) z wykrywaniem języka
- Rate limiting z Redis
- Cache Redis dla zwiększenia wydajności
- Monitoring metryk Prometheus i dashboard Grafana
- Kompletną dokumentację API i bot commandów
- Testy jednostkowe i integracyjne backendu i bota
- Konteneryzację Dockera i orkiestrację Docker Compose

## Funkcje
- Bezpieczne logowanie i odświeżanie tokenów JWT
- Administracja użytkownikami i rolami przez API i bota
- Spersonalizowane komendy Discord z lokalizacją i ochroną antyspamową
- Skalowalny backend asynchroniczny z FastAPI i PostgreSQL
- Automatyczne migracje bazy danych Alembic
- Obsługa statycznych plików frontendu oraz API w jednym serwisie
- Centralna obsługa błędów i standaryzacja odpowiedzi
- Wsparcie dla wielu środowisk: development, staging, production

---

## Wymagania wstępne

- Docker (wersja >= 20.x)
- Docker Compose (wersja >= 1.29)
- Python 3.10+ (do lokalnego uruchomienia backendu i bota)
- Node.js 16+ (do lokalnej pracy frontendu)
- PostgreSQL (jeśli nie korzystasz z Dockera)
- Redis (jeśli nie korzystasz z Dockera)

---

## Instalacja i uruchomienie

### 1. Klonowanie repozytorium
