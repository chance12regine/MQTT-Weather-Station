from flask import Flask, jsonify, send_file
import sqlite3
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Add root route to serve index.html
@app.route('/')
def index():
    return send_file('index.html')

# Database setup
def setup_database():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_readings
                 (timestamp DATETIME, temperature REAL, humidity REAL)''')
    conn.commit()
    conn.close()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe("/work_group_01/room_temp/#")

def on_message(client, userdata, msg):
    topic = msg.topic
    value = float(msg.payload.decode())
    print(f"Received: {topic} → {value}")
    
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    current_time = datetime.now()
    
    # First, try to find a reading from the same timestamp
    c.execute("""
        SELECT rowid, temperature, humidity 
        FROM weather_readings 
        WHERE timestamp >= datetime(?, '-5 seconds')
        AND timestamp <= datetime(?, '+5 seconds')
        ORDER BY timestamp DESC
        LIMIT 1
    """, (current_time, current_time))
    
    existing_row = c.fetchone()
    
    if existing_row:
        # Update existing reading
        rowid, temp, hum = existing_row
        if "temperature" in topic:
            c.execute("UPDATE weather_readings SET temperature = ? WHERE rowid = ?",
                     (value, rowid))
        elif "humidity" in topic:
            c.execute("UPDATE weather_readings SET humidity = ? WHERE rowid = ?",
                     (value, rowid))
    else:
        # Insert new reading
        if "temperature" in topic:
            c.execute("INSERT INTO weather_readings (timestamp, temperature, humidity) VALUES (?, ?, NULL)",
                     (current_time, value))
        elif "humidity" in topic:
            c.execute("INSERT INTO weather_readings (timestamp, temperature, humidity) VALUES (?, NULL, ?)",
                     (current_time, value))
    
    conn.commit()
    conn.close()

# Flask routes
@app.route('/api/data')
def get_data():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    # Get only readings that have both temperature and humidity
    c.execute("""
        SELECT 
            datetime(timestamp) as time_block,
            temperature,
            humidity
        FROM weather_readings
        WHERE temperature IS NOT NULL 
        AND humidity IS NOT NULL
        ORDER BY timestamp DESC
    """)
    
    results = c.fetchall()
    data = [{
        'timestamp': row[0],
        'temperature': row[1],
        'humidity': row[2]
    } for row in results]
    
    conn.close()
    return jsonify(data)

# Add a new route to get statistics
@app.route('/api/stats')
def get_stats():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    # Modified query to handle NULL values better
    c.execute("""
        SELECT 
            COUNT(*) as total_readings,
            COALESCE(MIN(temperature), 0) as min_temp,
            COALESCE(MAX(temperature), 0) as max_temp,
            COALESCE(AVG(temperature), 0) as avg_temp,
            COALESCE(MIN(humidity), 0) as min_humidity,
            COALESCE(MAX(humidity), 0) as max_humidity,
            COALESCE(AVG(humidity), 0) as avg_humidity
        FROM weather_readings
        WHERE temperature IS NOT NULL 
        OR humidity IS NOT NULL
    """)
    
    result = c.fetchone()
    stats = {
        'total_readings': result[0],
        'temperature': {
            'min': float(result[1]) if result[1] is not None else 0,
            'max': float(result[2]) if result[2] is not None else 0,
            'avg': float(result[3]) if result[3] is not None else 0
        },
        'humidity': {
            'min': float(result[4]) if result[4] is not None else 0,
            'max': float(result[5]) if result[5] is not None else 0,
            'avg': float(result[6]) if result[6] is not None else 0
        }
    }
    
    conn.close()
    return jsonify(stats)

if __name__ == '__main__':
    setup_database()
    
    # Setup MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("157.173.101.159", 1883, 60)
    mqtt_client.loop_start()
    
    app.run(debug=True) 