import time
import sqlite3
import requests
from datetime import datetime, timedelta
import os
import json
import pytz
from dateutil import parser

DATABASE_PATH = '/app/messages.db'

def send_message(message, server, topic, headers):
    url = f'https://{server}/{topic}'
    print(f"Sending message to URL: {url}")  # Debug logging
    
    # Encode headers as UTF-8
    encoded_headers = {k: str(v).encode('utf-8') for k, v in headers.items()}
    
    try:
        response = requests.post(url, data=message.encode('utf-8'), headers=encoded_headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Message sent successfully. Response status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message. Error: {e}")

def get_next_schedule(datetime_str, interval, custom_days):
    dt = parser.isoparse(datetime_str)
    if interval == 'daily':
        next_schedule = dt + timedelta(days=1)
    elif interval == 'weekly':
        next_schedule = dt + timedelta(weeks=1)
    elif interval == 'monthly':
        next_schedule = dt + timedelta(days=30)
    elif interval == 'custom':
        next_schedule = dt + timedelta(days=int(custom_days))
    else:
        next_schedule = None
    return next_schedule

def check_scheduled_messages():
    while True:
        now = datetime.now(pytz.utc).isoformat()
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            c.execute('SELECT * FROM messages WHERE datetime <= ?', (now,))
            rows = c.fetchall()
            for row in rows:
                message_id, message, datetime_str, server, topic, interval, custom_days, timezone, headers = row
                print(f"Processing message ID {message_id} with server '{server}' and topic '{topic}' at '{datetime_str}' in timezone '{timezone}'")  # Debug logging
                
                # Decode headers JSON string
                headers = json.loads(headers)
                
                if server and topic:
                    send_message(message, server, topic, headers)
                    sent_at = datetime.now(pytz.utc).isoformat()
                    c.execute('INSERT INTO sent_messages (message, datetime, server, topic, sent_at, timezone, headers) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                              (message, datetime_str, server, topic, sent_at, timezone, json.dumps(headers)))
                    next_schedule = get_next_schedule(datetime_str, interval, custom_days)
                    if next_schedule:
                        c.execute('UPDATE messages SET datetime = ? WHERE id = ?', (next_schedule.isoformat(), message_id))
                    else:
                        c.execute('DELETE FROM messages WHERE id = ?', (message_id,))
                else:
                    print(f"Skipping message ID {message_id} due to missing server or topic")  # Debug logging
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
        time.sleep(60)

if __name__ == '__main__':
    check_scheduled_messages()
