#################################################
# Flask Setup
#################################################

import requests
from flask import Flask, render_template, request, session, redirect, url_for
import requests

app = Flask(__name__)

# Set up the Yelp API endpoint URL
base_url = 'https://api.yelp.com/v3/businesses/search'

# Set up the Google Geocoding API endpoint URL
geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'

#################################################
# Flask Routes
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/restaurant_names')
def get_restaurant_names():
    address = request.args.get('address')

    if address:
        location = geocode_address(address)

        if location:
            latitude, longitude = location
        else:
            return 'Error occurred while geocoding the address.'

        restaurants = fetch_restaurants(latitude, longitude)

        if restaurants:
            restaurant_names = [restaurant.get('name') for restaurant in restaurants]
            return render_template('restaurant_names.html', restaurant_names=restaurant_names)
        else:
            return 'No restaurants found within the specified radius.'
    else:
        return 'Please provide an address.'

@app.route('/restaurant_types')
def get_restaurant_types():
    address = request.args.get('address')

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

            return render_template('restaurant_types.html', restaurant_types=restaurant_counts)
        else:
            return 'No restaurants found.'
    else:
        return 'Please provide an address.'
    
@app.route('/avg_rating')
def get_avg_rating():
    address = request.args.get('address')

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
                return render_template('avg_rating.html', avg_rating=avg_rating)
            else:
                return 'No ratings available for restaurants in the specified area.'
        else:
            return 'No restaurants found.'
    else:
        return 'Please provide an address.'

# Run the application
if __name__ == "__main__":
    app.run(debug=True)