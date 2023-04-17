from flask import Flask, request
import pandas as pd
import requests
from datetime import datetime

app = Flask(__name__)

# Load the crime dataset
crime_df = pd.read_csv('crime_data.csv')

@app.route('/update_crime_dataset', methods=['POST'])
def update_crime_dataset():
    # Get the form input data
    print(request.form)
    new_crime = {
        'type': request.form['type'],
    }
    print(new_crime)
    # Get the current date and time
    now = datetime.now()
    new_crime['date'] = now.strftime('%Y-%m-%d')
    new_crime['time'] = now.strftime('%H:%M:%S')
    
    # Get the user's location using the HTML5 Geolocation API
    user_location = request.form['location']
    lat, long = user_location.split(',')
    
    # Geocode the user's location to get the address
    response = requests.get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={long}&format=json')
    address = response.json()['display_name']
    
    # Add the user's location and address to the new crime
    new_crime['latitude'] = lat
    new_crime['longitude'] = long
    new_crime['address'] = address
    
    # Add the new crime to the dataset
    crime_df = crime_df.append(new_crime, ignore_index=True)
    
    # Save the updated dataset to a file
    crime_df.to_csv('crime_dataset.csv', index=False)
    
    # Return a success message
    return {'message': 'Crime dataset updated successfully.'}, 200

if __name__ == '__main__':
    app.run(debug=True)
