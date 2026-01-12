# Ticket Price Checker ✈️

A simple web application written in Python (Flask) for tracking Ryanair flight ticket prices. The application allows you to pin connections of interest and check their current prices as well as price history.

## 🚀 Features

- **Price Tracking:** Fetching current ticket prices directly from the carrier's API.
- **Price History:** Automatically saving price history in a local SQLite database.
- **Change Detection:** The system compares the current price with the last saved one and records only changes.
- **Pinning Links:** Ability to save favorite routes (links to the Ryanair search engine) for quick access.
- **Lightweight Interface:** Simple API returning data in JSON format.

## 🛠️ Requirements and Installation

1.  **Requirements:** Python 3.x
2.  **Install dependencies:**
    ```bash
    pip install flask requests
    ```

## ▶️ Usage

Run the main application file:

```bash
python ticket.py
```
The application will be available at: `http://127.0.0.1:5678`

## 📖 API Documentation

### 1. Check price (`POST /api/check`)

Fetches the current price for the provided link and saves it to the database if it has changed.

- **Body:** `{"url": "https://www.ryanair.com/..."}`

### 2. Pin link (`POST /api/pin`)

Saves the link to the "favorites" database.

- **Body:** `{"url": "https://www.ryanair.com/..."}`

### 3. Get pinned links (`GET /api/pinned`)

Returns a list of all saved links.

## 🗄️ Database

The application automatically creates a `prices.db` file upon the first run. It contains two tables:

- `prices`: price history (route, flight date, price, currency, check date).
- `pinned_links`: saved URLs.

---

**Note:** The application uses an unofficial API. Use responsibly.