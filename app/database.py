import sqlite3
import os
import json
from datetime import datetime, timedelta
import pytz
from dateutil import parser

DATABASE_PATH = '/app/data/messages.db'

def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY, message TEXT, datetime TEXT, server TEXT, topic TEXT, interval TEXT, custom_days INTEGER, timezone TEXT, headers TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS sent_messages
                     (id INTEGER PRIMARY KEY, message TEXT, datetime TEXT, server TEXT, topic TEXT, sent_at TEXT, timezone TEXT, headers TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS topics
                     (id INTEGER PRIMARY KEY, name TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS servers
                     (id INTEGER PRIMARY KEY, address TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS defaults
                     (key TEXT PRIMARY KEY, value TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in init_db: {e}")
    finally:
        if conn:
            conn.close()

def add_message(message, datetime, server, topic, interval, custom_days, timezone, headers):
    try:
        if datetime.tzinfo is None:
            raise ValueError("Datetime object must be timezone-aware")
        utc_time = datetime.astimezone(pytz.utc)
        utc_datetime = utc_time.strftime('%Y-%m-%dT%H:%M:%S%z')

        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO messages (message, datetime, server, topic, interval, custom_days, timezone, headers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                  (message, utc_datetime, server, topic, interval, custom_days, timezone, headers))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in add_message: {e}")
    finally:
        conn.close()

def get_messages():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM messages')
        messages = [{'id': row[0], 'message': row[1], 'datetime': row[2], 'server': row[3], 'topic': row[4], 
                     'interval': row[5], 'custom_days': row[6], 'timezone': row[7], 'headers': row[8]} for row in c.fetchall()]
        return messages
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in get_messages: {e}")
    finally:
        conn.close()

def delete_message(id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM messages WHERE id = ?', (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in delete_message: {e}")
    finally:
        conn.close()

def edit_message(id, message, datetime, server, topic, interval, custom_days, timezone, headers):
    try:
        if datetime.tzinfo is None:
            raise ValueError("Datetime object must be timezone-aware")
        utc_time = datetime.astimezone(pytz.utc)
        utc_datetime = utc_time.strftime('%Y-%m-%dT%H:%M:%S%z')

        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('UPDATE messages SET message = ?, datetime = ?, server = ?, topic = ?, interval = ?, custom_days = ?, timezone = ?, headers = ? WHERE id = ?', 
                  (message, utc_datetime, server, topic, interval, custom_days, timezone, headers, id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in edit_message: {e}")
    finally:
        conn.close()

def add_sent_message(message, datetime, server, topic, sent_at, timezone, headers):
    try:
        utc_time = sent_at.astimezone(pytz.utc)
        utc_sent_at = utc_time.strftime('%Y-%m-%dT%H:%M:%S%z')

        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO sent_messages (message, datetime, server, topic, sent_at, timezone, headers) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                  (message, datetime, server, topic, utc_sent_at, timezone, headers))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in add_sent_message: {e}")
    finally:
        conn.close()

def get_sent_messages():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM sent_messages')
        messages = [{'id': row[0], 'message': row[1], 'datetime': row[2], 'server': row[3], 'topic': row[4], 'sent_at': row[5], 'timezone': row[6], 'headers': row[7]} for row in c.fetchall()]
        return messages
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in get_sent_messages: {e}")
    finally:
        conn.close()

def delete_topic(id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM topics WHERE id = ?', (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in delete_topic: {e}")
    finally:
        conn.close()

def add_topic(name):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO topics (name) VALUES (?)', (name,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in add_topic: {e}")
    finally:
        conn.close()

def get_topics():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM topics')
        topics = [{'id': row[0], 'name': row[1]} for row in c.fetchall()]
        return topics
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in get_topics: {e}")
    finally:
        conn.close()

def add_server(address):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO servers (address) VALUES (?)', (address,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in add_server: {e}")
    finally:
        conn.close()

def get_servers():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM servers')
        servers = [{'id': row[0], 'address': row[1]} for row in c.fetchall()]
        return servers
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in get_servers: {e}")
    finally:
        conn.close()

def delete_server(id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM servers WHERE id = ?', (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in delete_server: {e}")
    finally:
        conn.close()

def get_default_server():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT value FROM defaults WHERE key = "default_server"')
        row = c.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in get_default_server: {e}")
    finally:
        conn.close()

def set_default_server(server):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('REPLACE INTO defaults (key, value) VALUES ("default_server", ?)', (server,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in set_default_server: {e}")
    finally:
        conn.close()

def get_default_topic():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT value FROM defaults WHERE key = "default_topic"')
        row = c.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in get_default_topic: {e}")
    finally:
        conn.close()

def set_default_topic(topic):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('REPLACE INTO defaults (key, value) VALUES ("default_topic", ?)', (topic,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Exception in set_default_topic: {e}")
    finally:
        conn.close()

def calculate_next_schedule(datetime_str, interval, custom_days):
    if not interval or interval == '':
        return ''
    dt = parser.isoparse(datetime_str)
    if interval == 'daily':
        next_schedule = dt + timedelta(days=1)
    elif interval == 'weekly':
        next_schedule = dt + timedelta(weeks=1)
    elif interval == 'monthly':
        next_schedule = dt + timedelta(days=30)
    elif interval == 'custom':
        next_schedule = dt + timedelta(days=int(custom_days))
    return next_schedule.isoformat()
