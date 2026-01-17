from flask import Flask, render_template, request, jsonify
import requests
import datetime
from urllib.parse import urlparse, parse_qs
import sqlite3
# import os
# from dotenv import load_dotenv 

# load_dotenv()


# db init
def init_db():
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prices
                 (origin TEXT, destination TEXT, flight_date TEXT, price REAL, currency TEXT, checked_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pinned_links
                 (url TEXT PRIMARY KEY, created_at TEXT)''')
    conn.commit()
    conn.close()

init_db()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pin', methods=['POST'])
def pin_link():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'Brak linku'}), 400

    try:
        conn = sqlite3.connect('prices.db')
        c = conn.cursor()
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT OR IGNORE INTO pinned_links (url, created_at) VALUES (?, ?)", (url, created_at))
        conn.commit()
        
        # Pobierz zaktualizowaną listę z bazy
        c.execute("SELECT url FROM pinned_links")
        rows = c.fetchall()
        current_links = [row[0] for row in rows]
        conn.close()
        
        return jsonify({'success': True, 'links': current_links})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/pinned', methods=['GET'])
def get_pinned_links():
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute("SELECT url FROM pinned_links")
    rows = c.fetchall()
    conn.close()
    return jsonify({'links': [row[0] for row in rows]})

@app.route('/api/check', methods=['POST'])
def check_price_api():
    data = request.get_json()
    ticket_url = data.get('url', '').strip()
    
    if not ticket_url:
        return jsonify({'success': False, 'error': 'Brak linku'}), 400

    try:
        parsed_url = urlparse(ticket_url)
        query_params = parse_qs(parsed_url.query)

        api_url = "https://www.ryanair.com/api/farfnd/3/oneWayFares"
        
        origin = query_params.get("originIata", ["LCJ"])[0]
        destination = query_params.get("destinationIata", ["AGP"])[0]
        date_out = query_params.get("dateOut", [""])[0]
        
        if not date_out:
             date_out = query_params.get("tpStartDate", [""])[0]

        params = {
            "departureAirportIataCode": origin,
            "arrivalAirportIataCode": destination,
            "outboundDepartureDateFrom": date_out,
            "outboundDepartureDateTo": date_out,
            "adults": query_params.get("adults", ["1"])[0],
            "children": query_params.get("children", ["0"])[0],
            "teens": query_params.get("teens", ["0"])[0],
            "infants": query_params.get("infants", ["0"])[0]
        }

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        api_data = response.json()

        if api_data.get("fares"):
            fare = api_data["fares"][0]["outbound"]
            price_val = fare["price"]["value"]
            currency = fare["price"]["currencySymbol"]
            last_update_ms = fare["priceUpdated"]
            
            dep_airport = fare["departureAirport"]["name"]
            dep_iata = fare["departureAirport"]["iataCode"]
            arr_airport = fare["arrivalAirport"]["name"]
            arr_iata = fare["arrivalAirport"]["iataCode"]
            
            dep_dt = fare["departureDate"]
            arr_dt = fare["arrivalDate"]

            dep_date_str = dep_dt.split("T")[0].replace("-", ".")
            dep_time_str = dep_dt.split("T")[1][:-3]
            arr_date_str = arr_dt.split("T")[0].replace("-", ".")
            arr_time_str = arr_dt.split("T")[1][:-3]

            timestamp = last_update_ms / 1000
            dt_update = datetime.datetime.fromtimestamp(timestamp)
            update_date = dt_update.strftime("%Y.%m.%d")
            update_time = dt_update.strftime("%H:%M")

            # bazka
            conn = sqlite3.connect('prices.db')
            c = conn.cursor()
            
            # pobiera ostatnią cene dla sprawdzanego lotu, zanim zapiszemy aktualną cene
            c.execute('''SELECT price, currency, checked_at FROM prices 
                         WHERE origin=? AND destination=? AND flight_date=? 
                         ORDER BY checked_at DESC LIMIT 1''', (origin, destination, date_out))
            last_record = c.fetchone()
            
            last_price = last_record[0] if last_record else None
            
            if last_price != price_val:
            # zapisuje aktualną cene
                current_check_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO prices VALUES (?, ?, ?, ?, ?, ?)", 
                        (origin, destination, date_out, price_val, currency, current_check_time))
                conn.commit()
                conn.close()

            response_data = {
                'success': True,
                'route': f"{dep_airport} ({dep_iata}) ➡ {arr_airport} ({arr_iata})",
                'date': f"Wylot: {dep_date_str} {dep_time_str}<br>Przylot: {arr_date_str} {arr_time_str}",
                'price': f"{price_val} {currency}",
                'updated': f"{update_date} {update_time}",
                'prev_price': f"{last_record[0]} {last_record[1]}" if last_record else None,
                'prev_date': last_record[2] if last_record else None
            }
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': 'Nie znaleziono lotu (sprawdź datę/trasę).'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # run flask
    app.run(debug=True, port=5678, host='127.0.0.1')