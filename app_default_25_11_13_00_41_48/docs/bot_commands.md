# Dokumentacja Komend Bota Discord

## Komendy Administracyjne

### !ban @user [reason]
- Opis: Banuje użytkownika na serwerze
- Wymagane uprawnienia: Ban members lub rola Admin/Moderator
- Przykład:
    - `!ban @Janek Nieprzestrzeganie zasad`
- Ograniczenia: cooldown 5 sekund na użytkownika

### !unban username
- Opis: Coś do unbanu użytkownika
- Wymagane uprawnienia: Ban members lub rola Admin/Moderator
- Przykład:
    - `!unban Janek`

### !clearcache
- Opis: Czyści cache bota i backendu
- Wymagane uprawnienia: rola Admin

## Komendy Publiczne

### !help
- Opis: Wyświetla listę dostępnych komend i pomoc
- Przykład: `!help`

### !info
- Opis: Informacje o serwerze i bocie
- Przykład: `!info`

### !profile
- Opis: Wyświetla profil użytkownika
- Przykład: `!profile`

## Limity i Ochrona

- Komendy mają cooldown 5 sekund na użytkownika
- Automatyczna detekcja i blokada spamu (wielokrotne identyczne wiadomości)
- Komendy są lokalizowane według języka serwera

## Międzynarodowość

- Bot wspiera języki angielski oraz polski
- W przypadku braku tłumaczenia, zwracany jest klucz komendy

