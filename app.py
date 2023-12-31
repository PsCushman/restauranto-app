#################################################
# Flask Setup
#################################################

import requests
import secrets
from flask import Flask, render_template, request, session, redirect, url_for
from api_keys import yelp_key, google_maps_key


app = Flask(__name__)

# Set the secret key for sessions
app.secret_key = secrets.token_hex(16)

# Set up the Yelp API endpoint URL
base_url = 'https://api.yelp.com/v3/businesses/search'

# Set up the Google Geocoding API endpoint URL
geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'

#################################################
# Flask Functions
#################################################

def fetch_restaurants(latitude, longitude):
    headers = {
        'Authorization': f'Bearer {yelp_key}'
    }

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': 1000,
        'categories': 'restaurants',
        'limit': 50
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        restaurant_data = response.json()
        return restaurant_data.get('businesses', [])
    else:
        print('Error occurred while fetching restaurant data.')
        return []

def geocode_address(address):
    params = {
        'address': address,
        'key': google_maps_key
    }

    response = requests.get(geocoding_url, params=params)

    if response.status_code == 200:
        geocoding_data = response.json()

        results = geocoding_data.get('results', [])

        if results:
            location = results[0].get('geometry', {}).get('location')
            latitude = location.get('lat')
            longitude = location.get('lng')
            return latitude, longitude
        else:
            return None
    else:
        return None

#################################################
# Flask Routes
#################################################

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        address = request.form.get('address')
        session['address'] = address
        return redirect(url_for('home'))

    address = session.get('address')

    if address:
        location = geocode_address(address)

        if location:
            latitude, longitude = location

            print(latitude, longitude)  # Add this line to check the values

            restaurants = fetch_restaurants(latitude, longitude)

            return render_template('index.html', latitude=latitude, longitude=longitude, restaurants=restaurants)

    return render_template('index.html')

@app.route('/restaurant_info', methods=['GET', 'POST'])
def restaurant_info():
    if request.method == 'POST':
        address = request.form.get('address')
        if address:
            session['address'] = address
            return redirect(url_for('restaurant_info'))
        else:
            return 'Please provide an address.'

    address = session.get('address')

    if address:
        location = geocode_address(address)

        if location:
            latitude, longitude = location

            print(latitude, longitude)  # Add this line to check the values

            restaurants = fetch_restaurants(latitude, longitude)

            return render_template('index.html', latitude=latitude, longitude=longitude, restaurants=restaurants)

    return render_template('index.html')

@app.route('/restaurant_names')
def restaurant_names():
    address = session.get('address')

    if address:
        location = geocode_address(address)

        if location:
            latitude, longitude = location
        else:
            return 'Error occurred while geocoding the address.'

        restaurants = fetch_restaurants(latitude, longitude)

        if restaurants:
            restaurant_names = [restaurant.get('name') for restaurant in restaurants]
            restaurant_count = len(restaurant_names)  # Calculate the count
            return render_template('restaurant_names.html', restaurant_names=restaurant_names, restaurant_count=restaurant_count)  # Pass the count to the template
        else:
            return 'No restaurants found.'
    else:
        return redirect(url_for('restaurant_info'))

@app.route('/restaurant_types')
def restaurant_types():
    address = session.get('address')

    if address:
        location = geocode_address(address)

        if location:
            latitude, longitude = location
        else:
            return 'Error occurred while geocoding the address.'

        restaurants = fetch_restaurants(latitude, longitude)

        if restaurants:
            restaurant_counts = {}
            for restaurant in restaurants:
                categories = restaurant.get('categories', [])
                for category in categories:
                    title = category.get('title')
                    restaurant_counts[title] = restaurant_counts.get(title, 0) + 1

            sorted_counts = dict(sorted(restaurant_counts.items(), key=lambda x: x[1], reverse=True))

            return render_template('restaurant_types.html', restaurant_counts=sorted_counts)

    return redirect(url_for('restaurant_info'))
    
@app.route('/avg_rating')
def avg_rating():
    address = session.get('address')
    
    if address:
        location = geocode_address(address)

        if location:
            latitude, longitude = location
        else:
            return 'Error occurred while geocoding the address.'

        restaurants = fetch_restaurants(latitude, longitude)

        if restaurants:
            total_rating = 0
            total_restaurants = 0

            for restaurant in restaurants:
                rating = restaurant.get('rating')
                if rating:
                    total_rating += rating
                    total_restaurants += 1

            if total_restaurants > 0:
                avg_rating = total_rating / total_restaurants
            
            return render_template('avg_rating.html', avg_rating=avg_rating, address=address)
    else:
        return redirect(url_for('restaurant_info'))
    
@app.route('/property_information')
def property_information():
    return render_template('property_information.html')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)