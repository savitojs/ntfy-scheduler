from flask import Flask, request, render_template, jsonify
from database import (
    init_db, add_message, get_messages, delete_message, edit_message,
    add_topic, get_topics, delete_topic, add_server, get_servers, delete_server,
    get_default_server, set_default_server, get_default_topic, set_default_topic,
    calculate_next_schedule, get_sent_messages
)
import os
import json
from datetime import datetime, timedelta
import pytz
from dateutil import parser

app = Flask(__name__)

@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    try:
        message = request.form['message']
        datetime_str = request.form['datetime']
        server = request.form['server']
        topic = request.form['topic']
        interval = request.form.get('interval', '')
        custom_days = request.form.get('custom_days', '')
        timezone_str = request.form.get('timezone', 'UTC')
        headers = {
            "Title": request.form.get('header_title', ''),
            "Priority": request.form.get('header_priority', ''),
            "Tags": request.form.get('header_tags', '')
        }

        local_tz = pytz.timezone(timezone_str)
        local_datetime = parser.isoparse(datetime_str)

        # If the datetime is naive (lacking timezone info), localize it
        if local_datetime.tzinfo is None:
            local_datetime = local_tz.localize(local_datetime)
        else:
            # Convert aware datetime to the target timezone
            local_datetime = local_datetime.astimezone(local_tz)

        print(f"Scheduling message with server '{server}' and topic '{topic}' at '{local_datetime}' in timezone '{timezone_str}'")
        add_message(message, local_datetime, server, topic, interval, custom_days, timezone_str, json.dumps(headers))
        return 'Message scheduled successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/scheduled', methods=['GET'])
def scheduled():
    try:
        messages = get_messages()
        for message in messages:
            local_tz = pytz.timezone(message['timezone'])
            utc_datetime = parser.isoparse(message['datetime'])
            local_datetime = utc_datetime.astimezone(local_tz)
            message['datetime'] = local_datetime.isoformat()
            if message['interval']:
                next_schedule_utc = calculate_next_schedule(utc_datetime.isoformat(), message['interval'], message['custom_days'])
                next_schedule_local = parser.isoparse(next_schedule_utc).astimezone(local_tz).isoformat()
                message['next_schedule'] = next_schedule_local
            else:
                message['next_schedule'] = ''
        return jsonify({'messages': messages})
    except Exception as e:
        return f"An error occurred: {e}"

def calculate_next_schedule(datetime_str, interval, custom_days):
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
        next_schedule = dt  # Default to the current datetime if interval is not recognized
    return next_schedule.isoformat()

@app.route('/sent', methods=['GET'])
def sent():
    try:
        messages = get_sent_messages()
        for message in messages:
            local_tz = pytz.timezone(message['timezone'])
            utc_datetime = parser.isoparse(message['datetime'])
            local_datetime = utc_datetime.astimezone(local_tz)
            message['datetime'] = local_datetime.isoformat()
            sent_at_utc = parser.isoparse(message['sent_at'])
            message['sent_at'] = sent_at_utc.astimezone(local_tz).isoformat()
        return jsonify({'messages': messages})
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        delete_message(id)
        return 'Message deleted successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/edit/<int:id>', methods=['PUT'])
def edit(id):
    try:
        message = request.form['message']
        datetime_str = request.form['datetime']
        server = request.form['server']
        topic = request.form['topic']
        interval = request.form['interval']
        custom_days = request.form.get('custom_days', '')
        timezone_str = request.form.get('timezone', 'UTC')
        headers = {
            "Title": request.form.get('header_title', ''),
            "Priority": request.form.get('header_priority', ''),
            "Tags": request.form.get('header_tags', '')
        }

        local_tz = pytz.timezone(timezone_str)
        local_datetime = parser.isoparse(datetime_str)

        # If the datetime is naive (lacking timezone info), localize it
        if local_datetime.tzinfo is None:
            local_datetime = local_tz.localize(local_datetime)
        else:
            # Convert aware datetime to the target timezone
            local_datetime = local_datetime.astimezone(local_tz)

        edit_message(id, message, local_datetime, server, topic, interval, custom_days, timezone_str, json.dumps(headers))
        return 'Message edited successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/topics', methods=['GET'])
def topics():
    try:
        topics = get_topics()
        return jsonify({'topics': topics})
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/add_topic', methods=['POST'])
def add_topic_route():
    try:
        name = request.form['name']
        add_topic(name)
        return 'Topic added successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/delete_topic/<int:id>', methods=['DELETE'])
def delete_topic_route(id):
    try:
        delete_topic(id)
        return 'Topic deleted successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/servers', methods=['GET'])
def servers():
    try:
        servers = get_servers()
        return jsonify({'servers': servers})
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/add_server', methods=['POST'])
def add_server_route():
    try:
        address = request.form['address']
        add_server(address)
        return 'Server added successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/delete_server/<int:id>', methods=['DELETE'])
def delete_server_route(id):
    try:
        delete_server(id)
        return 'Server deleted successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/default_server', methods=['GET'])
def default_server():
    try:
        server = get_default_server()
        return jsonify({'default_server': server})
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/set_default_server', methods=['POST'])
def set_default_server_route():
    try:
        server = request.form['server']
        set_default_server(server)
        return 'Default server set successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/default_topic', methods=['GET'])
def default_topic():
    try:
        topic = get_default_topic()
        return jsonify({'default_topic': topic})
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/set_default_topic', methods=['POST'])
def set_default_topic_route():
    try:
        topic = request.form['topic']
        set_default_topic(topic)
        return 'Default topic set successfully!'
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    try:
        init_db()
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    except Exception as e:
        print(f"An error occurred during startup: {e}")
