from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)

NASA_API_KEY = "Fl7OB7GRKLC897uDogSaISKJujCfsuc2IaDc46r6"
NASA_API_BASE_URL = "https://api.nasa.gov/neo/rest/v1/neo/"

def get_asteroid_info(neo_id):
    url = f"{NASA_API_BASE_URL}{neo_id}?api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        api_data = response.json()
        return api_data
    else:
        return None

def get_all_asteroid_ids():
    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        api_data = response.json()
        # Extracting NEO IDs from the response
        return [asteroid["id"] for asteroid in api_data["near_earth_objects"]]
    else:
        return None

@app.route('/')
def home():
    all_ids = get_all_asteroid_ids()
    return render_template('home.html', all_ids=all_ids)

@app.route('/search', methods=['POST'])
def search():
    neo_id = request.form.get('neo_id')
    neo_data = get_asteroid_info(neo_id)

    if neo_data:
        return render_template('search.html', neo_data=neo_data)
    else:
        return render_template('error.html', error="Unable to fetch asteroid information.")

if __name__ == '__main__':
    app.run(debug=True)
