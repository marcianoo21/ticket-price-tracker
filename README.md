# Ticket Price Checker ✈️

Prosta aplikacja webowa napisana w Pythonie (Flask), służąca do śledzenia cen biletów lotniczych linii Ryanair. Aplikacja pozwala na przypinanie interesujących nas połączeń i sprawdzanie ich aktualnych cen oraz historii zmian.

## 🚀 Funkcjonalności

- **Śledzenie cen:** Pobieranie aktualnych cen biletów bezpośrednio z API przewoźnika.
- **Historia cen:** Automatyczne zapisywanie historii cen w lokalnej bazie danych SQLite.
- **Wykrywanie zmian:** System porównuje aktualną cenę z ostatnią zapisaną i rejestruje tylko zmiany.
- **Przypinanie linków:** Możliwość zapisania ulubionych tras (linków do wyszukiwarki Ryanair) w celu szybkiego dostępu.
- **Lekki interfejs:** Proste API zwracające dane w formacie JSON.

## 🛠️ Wymagania i Instalacja

1.  **Wymagania:** Python 3.x
2.  **Instalacja zależności:**
    ```bash
    pip install flask requests
    ```

## ▶️ Uruchomienie

Uruchom główny plik aplikacji:

```bash
python ticket.py
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:5000`

## 📖 Dokumentacja API

### 1. Sprawdzenie ceny (`POST /api/check`)

Pobiera aktualną cenę dla podanego linku i zapisuje ją w bazie, jeśli uległa zmianie.

- **Body:** `{"url": "https://www.ryanair.com/..."}`

### 2. Przypięcie linku (`POST /api/pin`)

Zapisuje link w bazie "ulubionych".

- **Body:** `{"url": "https://www.ryanair.com/..."}`

### 3. Pobranie przypiętych linków (`GET /api/pinned`)

Zwraca listę wszystkich zapisanych linków.

## 🗄️ Baza Danych

Aplikacja automatycznie tworzy plik `prices.db` przy pierwszym uruchomieniu. Zawiera on dwie tabele:

- `prices`: historia cen (trasa, data lotu, cena, waluta, data sprawdzenia).
- `pinned_links`: zapisane adresy URL.

---

**Uwaga:** Aplikacja korzysta z nieoficjalnego API. Używaj odpowiedzialnie.
