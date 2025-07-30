from flask import jsonify, request, Flask
from flask_cors import CORS
import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})  


@app.route('/weather/by-location', methods=['GET'])
def weather_by_location():
    city = request.args.get("city")
    country = request.args.get("country")

    if not city or not country:
        return jsonify({"error": "City and country are required"}), 400

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={API_KEY}"
    geo_res = requests.get(geo_url).json()

    if not geo_res:
        return jsonify({"error": "Invalid location"}), 404

    lat = geo_res[0]['lat']
    lon = geo_res[0]['lon']

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()

    
    result = {
        "location": {
            "name": weather_data.get("name"),
            "country": weather_data["sys"].get("country"),
            "lat": lat,
            "lon": lon,
        },
        "weather": {
            "main": weather_data["weather"][0]["main"],
            "description": weather_data["weather"][0]["description"],
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "icon": weather_data["weather"][0]["icon"],
        },
        "wind": {
            "speed": weather_data["wind"]["speed"],
            "deg": weather_data["wind"]["deg"],
        },
        "clouds": weather_data["clouds"]["all"],
        "visibility": weather_data.get("visibility"),
        "timestamp": weather_data.get("dt")
    }

    return jsonify(result)


@app.route('/weather/by-coordinates', methods=['GET'])
def weather_by_coordinates():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()
        print(weather_data)
        result = {
            "location": {
                "name": weather_data.get("name"),
                "country": weather_data["sys"].get("country"),
                "lat": lat,
                "lon": lon,
            },
            "weather": {
                "main": weather_data["weather"][0]["main"],
                "description": weather_data["weather"][0]["description"],
                "temperature": weather_data["main"]["temp"],
                "feels_like": weather_data["main"]["feels_like"],
                "humidity": weather_data["main"]["humidity"],
                "pressure": weather_data["main"]["pressure"],
                "icon": weather_data["weather"][0]["icon"],
            },
            "wind": {
                "speed": weather_data["wind"]["speed"],
                "deg": weather_data["wind"]["deg"],
            },
            "clouds": weather_data["clouds"]["all"],
            "visibility": weather_data.get("visibility"),
            "timestamp": weather_data.get("dt")
        }

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__=='__main__':
    app.run(debug=True)