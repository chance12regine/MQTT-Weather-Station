# MQTT Weather Station Dashboard

A real-time weather monitoring dashboard that collects temperature and humidity data from MQTT sensors, stores it in SQLite, and visualizes it using interactive charts.

## Features

- Real-time temperature and humidity monitoring
- Interactive scatter plot showing temperature vs humidity correlation
- Historical data table with measurements
- Data persistence using SQLite database
- 5-minute averaged measurements
- Responsive design using Tailwind CSS

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mqtt-weather-app
   ```

2. Create a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python server.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

The dashboard will automatically:
- Connect to the MQTT broker
- Start collecting temperature and humidity data
- Store measurements in the SQLite database
- Update the visualizations every 5 minutes

## Project Structure

- `server.py` - Flask backend server and MQTT client
- `index.html` - Frontend dashboard
- `requirements.txt` - Python dependencies
- `weather_data.db` - SQLite database (created automatically)

## Technologies Used

- Backend:
  - Flask (Python web framework)
  - SQLite (Database)
  - Paho-MQTT (MQTT client)

- Frontend:
  - HTML/JavaScript
  - Tailwind CSS (Styling)
  - Plotly.js (Charts)
  - MQTT.js (WebSocket client)

## Troubleshooting

If you encounter any issues:

1. Make sure all required packages are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Check if the SQLite database was created:
   ```bash
   ls weather_data.db
   ```

3. Verify MQTT broker connection in the browser console

4. If the database gets corrupted, you can delete `weather_data.db` and restart the server - it will create a new database automatically.

## License

[MIT License](LICENSE) "# MQTT-Weather-Station" 
"# MQTT-Weather-Station" 
