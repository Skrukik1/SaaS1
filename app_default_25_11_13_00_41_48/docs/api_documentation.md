# Dokumentacja API Backend

## Autoryzacja
- Wymagane tokeny JWT w nagłówku `Authorization: Bearer <token>`
- Endpoints opisane z wymaganiami ról (np. admin, user)

## Endpointy

### POST /auth/login
- Opis: Logowanie użytkownika
- Request:
    - `username` (string)
    - `password` (string)
- Response:
    - `access_token` (string)
    - `token_type` (string, "bearer")
    - `expires_in` (int, sekundy)
- Błędy:
    - 401: Nieprawidłowe dane logowania

### GET /users
- Opis: Pobierz listę użytkowników (admin)
- Query:
    - `skip` (int, domyślnie 0)
    - `limit` (int, domyślnie 20)
- Response: lista użytkowników (UserResponse)
- Uprawnienia: admin

### POST /users
- Opis: Tworzenie użytkownika (admin)
- Request: UserCreate
- Response: UserResponse
- Uprawnienia: admin

### PUT /users/{id}
- Opis: Aktualizacja użytkownika (admin)
- Request: UserUpdate
- Response: UserResponse
- Uprawnienia: admin

### DELETE /users/{id}
- Opis: Usuwanie użytkownika (admin)
- Response: 204 No Content
- Uprawnienia: admin

### GET /admin/roles
- Opis: Pobierz role (admin)
- Response: lista ról
- Uprawnienia: admin

### POST /admin/roles
- Opis: Dodaj rolę (admin)
- Request: Role
- Response: Role
- Uprawnienia: admin

### GET /admin/logs
- Opis: Pobierz logi z filtrami (admin)
- Query: `level`, `source`, `limit`
- Response: lista logów
- Uprawnienia: admin

## Kody błędów
- 400: Błędne dane wejściowe
- 401: Brak autoryzacji
- 403: Brak uprawnień
- 404: Nie znaleziono zasobu
- 429: Limit zapytań przekroczony
- 500: Błąd serwera

## Przykład zapytania

