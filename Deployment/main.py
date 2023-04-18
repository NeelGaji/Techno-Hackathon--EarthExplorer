import csv
import datetime
from geopy.geocoders import Nominatim
from flask import Flask, request, render_template,jsonify

app = Flask(__name__)
geolocator = Nominatim(user_agent='crime_app')

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/prediction', methods = ['POST'])
def prediction():
    return render_template('routing.html')

@app.route('/fetch_recent_incident')
def fetch_recent():
    with open('file.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        second_row = next(csv_reader)  # Read the second row

    return jsonify(second_row)


@app.route('/update_crime_dataset', methods=['POST'])
def update_crime_dataset():
    # Get the crime type from the form data
    crime_type = request.form['type']

    # Get the user's location using the geolocation API of the browser
    latitude = request.headers.get('X-Forwarded-For')
    longitude = request.headers.get('X-Forwarded-Proto')

    # Reverse geocode the latitude and longitude into an address
    location = geolocator.reverse(f'{latitude}, {longitude}')
    address = location.address

    # Get the current date and time
    current_date_time = datetime.datetime.now()

    # Get the year, month, day, hour, and minute from the current date and time
    year = current_date_time.year
    month = current_date_time.month
    day = current_date_time.day
    hour = current_date_time.hour
    minute = current_date_time.minute

    # Add the new data to the dataset
    with open('crime_dataset.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([latitude, longitude, address, crime_type, month, year, day, hour, minute])

    return 'Data updated successfully'


if __name__ == '__main__':
    app.run(debug=True,port=6000)