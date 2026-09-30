from flask import Flask, render_template, request
import requests

app = Flask(__name__)
def get_weather(city):
    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city + ", India",
            "count": 1,
            "language": "en",
            "format": "json",
            "countryCode": "IN"
        }

        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()
        print("GEO DATA:", geo_data)

        if "results" not in geo_data or not geo_data["results"]:
            return "🌤️ Weather information not available"

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )
        weather_data = weather_response.json()

        current = weather_data.get("current")

        if not current:
            return "🌤️ Weather information not available"

        temperature = current.get("temperature_2m")
        weather_code = current.get("weather_code")

        weather_labels = {
            0: "☀️ Clear sky",
            1: "🌤️ Mainly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Foggy",
            48: "🌫️ Foggy",
            51: "🌦️ Light drizzle",
            53: "🌦️ Drizzle",
            55: "🌧️ Heavy drizzle",
            61: "🌧️ Light rain",
            63: "🌧️ Rain",
            65: "🌧️ Heavy rain",
            71: "🌨️ Light snow",
            73: "🌨️ Snow",
            75: "❄️ Heavy snow",
            80: "🌦️ Rain showers",
            81: "🌧️ Rain showers",
            82: "🌧️ Heavy rain showers",
            95: "⛈️ Thunderstorm",
            96: "⛈️ Thunderstorm with hail",
            99: "⛈️ Thunderstorm with heavy hail"
        }

        condition = weather_labels.get(
            weather_code,
            "🌤️ Weather information available"
        )

        return f"{condition}<br>🌡️ Temperature: {temperature}°C"

    except Exception as e:
        print("Weather error:", e)
        return "🌤️ Weather information not available"
def get_forecast(city):
    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
            "countryCode": "IN"
}

        geo_response = requests.get(geo_url, params=geo_params)
        geo_data = geo_response.json()

        if "results" not in geo_data:
            return []

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "forecast_days": 5,
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params
        )

        weather_data = weather_response.json()

        dates = weather_data["daily"]["time"]
        max_temps = weather_data["daily"]["temperature_2m_max"]
        min_temps = weather_data["daily"]["temperature_2m_min"]
        weather_codes = weather_data["daily"]["weather_code"]

        weather_conditions = {
            0: "☀️ Clear sky",
            1: "🌤️ Mainly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Foggy",
            51: "🌦️ Light drizzle",
            61: "🌧️ Light rain",
            63: "🌧️ Moderate rain",
            71: "❄️ Snow",
            80: "🌦️ Rain showers",
            95: "⛈️ Thunderstorm"
        }

        forecast = []

        for i in range(5):
            condition = weather_conditions.get(
                weather_codes[i],
                "🌤️ Weather information available"
            )

            forecast.append(
                f"{dates[i]} — {min_temps[i]}°C to "
                f"{max_temps[i]}°C — {condition}"
            )

        return forecast

    except Exception:
        return []

# Destination information
destinations = {
    "goa": [
        "🏖️ Visit Baga Beach",
        "🏰 Visit Fort Aguada",
        "🌊 Enjoy water sports",
        "🌅 Watch the sunset",
        "🛍️ Explore the local market"
    ],

    "mumbai": [
        "🌊 Visit Marine Drive",
        "🏛️ Visit Gateway of India",
        "🏖️ Explore Juhu Beach",
        "🛍️ Visit Colaba Causeway",
        "🍴 Try Mumbai street food"
    ],

    "delhi": [
        "🏰 Visit Red Fort",
        "🌳 Visit India Gate",
        "🏛️ Explore Qutub Minar",
        "🛍️ Visit Chandni Chowk",
        "🍴 Try Delhi street food"
    ],

    "manali": [
        "🏔️ Explore Solang Valley",
        "🌲 Visit Hadimba Temple",
        "🏞️ Explore Old Manali",
        "❄️ Enjoy snow activities",
        "🌅 Enjoy mountain views"
    ],

    "shimla": [
        "🏔️ Visit Mall Road",
        "⛪ Visit Christ Church",
        "🌲 Explore Kufri",
        "🏞️ Visit Shimla Ridge",
        "🌅 Enjoy mountain views"
    ],

    "kerala": [
        "🌴 Explore Alleppey backwaters",
        "🏖️ Visit Kovalam Beach",
        "🌿 Explore Munnar",
        "🚤 Enjoy a houseboat ride",
        "🍃 Visit a tea plantation"
    ],

    "jaipur": [
        "🏰 Visit Amber Fort",
        "🏯 Explore Hawa Mahal",
        "🏛️ Visit City Palace",
        "🌅 Watch the sunset at Nahargarh Fort",
        "🛍️ Explore local markets"
    ],

    "leh": [
        "🏔️ Visit Pangong Lake",
        "🏯 Explore Leh Palace",
        "🛕 Visit Thiksey Monastery",
        "🏍️ Enjoy a mountain drive",
        "🌄 Explore Nubra Valley"
    ],

    "pune": [
        "🏰 Visit Shaniwar Wada",
        "🌳 Explore Aga Khan Palace",
        "🏞️ Visit Sinhagad Fort",
        "🌿 Explore local gardens",
        "🍴 Try local Maharashtrian food"
    ],

    "andaman": [
        "🏖️ Visit Radhanagar Beach",
        "🤿 Enjoy scuba diving",
        "🐠 Explore marine life",
        "🏝️ Visit Havelock Island",
        "🌅 Watch the sunset"
    ]
   }
    
packing_lists = {
    "goa": [
        "🕶️ Sunglasses",
        "🧴 Sunscreen",
        "👕 Comfortable clothes",
        "👟 Comfortable shoes",
        "💧 Water bottle"
    ],

    "mumbai": [
        "☂️ Umbrella",
        "👕 Comfortable clothes",
        "👟 Comfortable shoes",
        "💧 Water bottle",
        "🎒 Small backpack"
    ],

    "delhi": [
        "🧴 Sunscreen",
        "💧 Water bottle",
        "👟 Comfortable shoes",
        "🧢 Cap",
        "🎒 Small backpack"
    ],

    "manali": [
        "🧥 Warm clothes",
        "🧤 Gloves",
        "🥾 Comfortable shoes",
        "🧢 Woollen cap",
        "💧 Water bottle"
    ],

    "shimla": [
        "🧥 Warm clothes",
        "🧤 Gloves",
        "🥾 Comfortable shoes",
        "🧢 Woollen cap",
        "☂️ Umbrella"
    ],

    "kerala": [
        "👕 Light clothes",
        "🧴 Sunscreen",
        "🦟 Mosquito repellent",
        "☂️ Umbrella",
        "👟 Comfortable shoes"
    ],

    "jaipur": [
        "🧢 Cap",
        "🧴 Sunscreen",
        "💧 Water bottle",
        "👟 Comfortable shoes",
        "🕶️ Sunglasses"
    ],

    "leh": [
        "🧥 Warm clothes",
        "🧤 Gloves",
        "🧢 Warm cap",
        "🥾 Trekking shoes",
        "🧴 Sunscreen"
    ],

    "pune": [
        "👕 Comfortable clothes",
        "👟 Comfortable shoes",
        "💧 Water bottle",
        "🧢 Cap",
        "🎒 Small backpack"
    ],

    "andaman": [
        "🩴 Beach footwear",
        "🕶️ Sunglasses",
        "🧴 Sunscreen",
        "👕 Beach clothes",
        "🤿 Swimming gear"
    ]
    }
    
hotel_recommendations = {
    "goa": [
        "🏨 Beachside Resort",
        "🏨 Palm Grove Hotel",
        "🏨 Sunset Beach Stay"
    ],

    "mumbai": [
        "🏨 Sea View Hotel",
        "🏨 City Comfort Hotel",
        "🏨 Gateway Stay"
    ],

    "delhi": [
        "🏨 Central Delhi Hotel",
        "🏨 Heritage Stay",
        "🏨 City View Hotel"
    ],

    "manali": [
        "🏨 Mountain View Resort",
        "🏨 Snow Valley Hotel",
        "🏨 Himalayan Stay"
    ],

    "shimla": [
        "🏨 Mountain View Hotel",
        "🏨 Shimla Valley Resort",
        "🏨 Hilltop Stay"
    ],

    "kerala": [
        "🏨 Backwater Resort",
        "🏨 Green Palm Hotel",
        "🏨 Kerala Riverside Stay"
    ],

    "jaipur": [
        "🏨 Heritage Palace Hotel",
        "🏨 Pink City Hotel",
        "🏨 Royal Jaipur Stay"
    ],

    "leh": [
        "🏨 Mountain View Hotel",
        "🏨 Leh Palace Stay",
        "🏨 Himalayan Resort"
    ],

    "pune": [
        "🏨 City Comfort Hotel",
        "🏨 Pune Central Stay",
        "🏨 Green View Hotel"
    ],

    "andaman": [
        "🏨 Beach Resort",
        "🏨 Island Paradise Stay",
        "🏨 Ocean View Resort"
    ]
    }

food_recommendations = {
    "goa": [
        "🍤 Goan Prawn Curry",
        "🐟 Goan Fish Thali",
        "🥘 Chicken Xacuti",
        "🍰 Bebinca",
        "🥥 Poi Bread"
    ],

    "mumbai": [
        "🌭 Vada Pav",
        "🥘 Pav Bhaji",
        "🥪 Bombay Sandwich",
        "🍛 Misal Pav",
        "🍨 Kulfi"
    ],

    "delhi": [
        "🥘 Butter Chicken",
        "🥙 Chole Bhature",
        "🍢 Seekh Kebab",
        "🥟 Momos",
        "🍨 Kulfi"
    ],

    "manali": [
        "🥟 Momos",
        "🍜 Thukpa",
        "🥔 Aloo Paratha",
        "🍵 Local Chai",
        "🍲 Tibetan Soup"
    ],

    "shimla": [
        "🥔 Aloo Paratha",
        "🥟 Momos",
        "🍜 Thukpa",
        "🍵 Chai",
        "🍰 Himachali Desserts"
    ],

    "kerala": [
        "🍛 Kerala Sadya",
        "🥥 Appam with Stew",
        "🐟 Kerala Fish Curry",
        "🥞 Dosa",
        "🍌 Banana Chips"
    ],

    "jaipur": [
        "🥘 Dal Baati Churma",
        "🌶️ Laal Maas",
        "🥙 Pyaz Kachori",
        "🍛 Gatte Ki Sabzi",
        "🍬 Ghevar"
    ],

    "leh": [
        "🥟 Momos",
        "🍜 Thukpa",
        "🍚 Skyu",
        "🍵 Butter Tea",
        "🥞 Tingmo"
    ],

    "pune": [
        "🥪 Misal Pav",
        "🥙 Vada Pav",
        "🍚 Puran Poli",
        "🥘 Bhakri",
        "🍵 Mastani"
    ],

    "andaman": [
        "🐟 Grilled Fish",
        "🍤 Seafood Curry",
        "🥥 Coconut Prawn Curry",
        "🍚 Fish Rice",
        "🍹 Tropical Fruit"
    ]
    }

travel_tips = {
    "goa": "🏖️ Carry sunscreen, sunglasses, and comfortable clothes for beach activities.",
    "mumbai": "🌆 Keep some extra time for traffic and explore local street food.",
    "delhi": "🏛️ Wear comfortable shoes and carry water while exploring historical places.",
    "manali": "🏔️ Carry warm clothes and comfortable shoes for mountain activities.",
    "shimla": "🏔️ Carry warm clothes and comfortable shoes for exploring the hills.",
    "kerala": "🌴 Carry light clothes, sunscreen, and an umbrella for exploring Kerala.",
    "jaipur": "🏰 Carry water, sunscreen, and comfortable shoes while exploring forts and markets.",
    "leh": "🏔️ Carry warm clothes, sunscreen, and stay hydrated while exploring high-altitude areas.",
    "pune": "🏞️ Carry comfortable shoes and water while exploring forts and local attractions.",
    "andaman": "🏖️ Carry sunscreen, beachwear, and comfortable footwear for island activities."
}
# Travel style recommendations
travel_styles = {
    "Adventure": [
        "🌊 Try water sports",
        "🥾 Go trekking",
        "🚵 Enjoy an adventure activity",
        "🏕️ Explore an outdoor location"
    ],

    "Relaxation": [
        "🏖️ Relax at a peaceful place",
        "🌅 Watch the sunset",
        "☕ Visit a relaxing cafe",
        "🌴 Enjoy some leisure time"
    ],

    "Historical": [
        "🏰 Visit a historical monument",
        "🏛️ Explore a famous heritage site",
        "📖 Learn about local history",
        "🕌 Visit an ancient landmark"
    ],

    "Nature": [
        "🌲 Explore nature",
        "🏞️ Visit a scenic location",
        "🌅 Enjoy beautiful views",
        "🥾 Take a nature walk"
    ],

    "Family": [
        "👨‍👩‍👧 Visit a family-friendly attraction",
        "🎡 Enjoy a fun activity",
        "🍴 Try local food together",
        "📸 Take family photos"
    ]
}

def get_personalized_recommendation(budget, style):
    if budget < 5000:
        if style == "Adventure":
            return "💡 Choose low-cost outdoor activities, local food, and budget-friendly stays."
        elif style == "Relaxation":
            return "💡 Choose peaceful local places and affordable stays to keep your trip within budget."
        elif style == "Historical":
            return "💡 Focus on nearby historical attractions and use public transport to save money."
        elif style == "Nature":
            return "💡 Explore free or low-cost natural attractions and scenic locations."
        else:
            return "💡 Choose family-friendly local attractions and affordable restaurants."

    elif budget < 15000:
        return f"✨ Your budget allows a balanced {style} trip with comfortable accommodation, food, and activities."

    else:
        return f"🌟 With your budget, you can enjoy a more comfortable {style} trip with better accommodation and activities."
def get_distance(starting, destination):
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"

        start_response = requests.get(
            url,
            params={
                "name": starting,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        destination_response = requests.get(
            url,
            params={
                "name": destination,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        start_data = start_response.json()
        destination_data = destination_response.json()

        if "results" not in start_data or "results" not in destination_data:
            return "Distance information not available"

        start_lat = start_data["results"][0]["latitude"]
        start_lon = start_data["results"][0]["longitude"]

        destination_lat = destination_data["results"][0]["latitude"]
        destination_lon = destination_data["results"][0]["longitude"]

        route_url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{start_lon},{start_lat};{destination_lon},{destination_lat}"
            f"?overview=false"
        )

        route_response = requests.get(route_url)
        route_data = route_response.json()

        if route_data["code"] != "Ok":
            return "Distance information not available"

        distance_km = route_data["routes"][0]["distance"] / 1000
        duration_minutes = route_data["routes"][0]["duration"] / 60

        hours = int(duration_minutes // 60)
        minutes = int(duration_minutes % 60)

        return (
            f"🗺️ Distance: {distance_km:.1f} km<br>"
            f"🚗 Estimated Travel Time: {hours} hours {minutes} minutes"
        )

    except Exception:
        return "Distance information not available"

def get_day_transport(distance_info, day):
    try:
        distance_text = distance_info.split("Distance: ")[1]
        distance_km = float(distance_text.split(" km")[0])

        if day == 1:
            if distance_km <= 10:
                return "🚶 Walking or 🛵 Bike — Suitable for a short journey."
            elif distance_km <= 100:
                return "🚗 Car or 🚌 Bus — Convenient for this distance."
            elif distance_km <= 500:
                return "🚆 Train or 🚌 Bus — Suitable for this journey."
            else:
                return "✈️ Flight or 🚆 Train — Suitable for this long journey."

        elif day % 3 == 2:
            return "🚌 Local Bus or 🚕 Taxi — Suitable for sightseeing."

        else:
            return "🚕 Local Taxi or 🚗 Car — Convenient for visiting nearby attractions."

    except Exception:
        return "🚌 Local transport recommended."
    
def get_transport_suggestion(distance_info):
    try:
        distance_text = distance_info.split("Distance: ")[1]
        distance_km = float(distance_text.split(" km")[0])

        if distance_km <= 10:
            return "🚶 Walking or 🛵 Bike — Suitable for short distances."
        elif distance_km <= 100:
            return "🚗 Car or 🚌 Bus — Convenient for short to medium distances."
        elif distance_km <= 500:
            return "🚆 Train or 🚌 Bus — Suitable for medium-distance travel."
        else:
            return "✈️ Flight or 🚆 Train — Recommended for long-distance travel."

    except Exception:
        return "🚌 Transportation suggestion not available"

def get_transport_cost(distance_info):
    try:
        distance_text = distance_info.split("Distance: ")[1]
        distance_km = float(distance_text.split(" km")[0])

        if distance_km <= 10:
            return "💰 Estimated Transport Cost: ₹50–₹150"
        elif distance_km <= 100:
            return "💰 Estimated Transport Cost: ₹200–₹800"
        elif distance_km <= 500:
            return "💰 Estimated Transport Cost: ₹800–₹2,500"
        else:
            return "💰 Estimated Transport Cost: ₹2,500–₹8,000"

    except Exception:
        return "💰 Transportation cost not available"


def get_smart_travel_decision(distance_info, budget):
    try:
        distance_text = distance_info.split("Distance: ")[1]
        distance_km = float(distance_text.split(" km")[0])

        if distance_km <= 100:
            return "🤖 Smart Recommendation: Car or bus is a convenient choice for this distance."

        elif distance_km <= 500:
            if budget < 10000:
                return "🤖 Smart Recommendation: Train or bus may be a budget-friendly choice."
            else:
                return "🤖 Smart Recommendation: Train or car are suitable options for this distance."

        else:
            if budget < 15000:
                return "🤖 Smart Recommendation: Train may help reduce your transportation cost."
            else:
                return "🤖 Smart Recommendation: Flight may save travel time for this long journey."

    except Exception:
        return "🤖 Smart travel recommendation not available"


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        starting = request.form["starting"]
        destination = request.form["destination"]
        days = int(request.form["days"])
        budget = request.form["budget"]
        style = request.form["style"]
        distance_info = get_distance(starting, destination)
        transport_suggestion = get_transport_suggestion(distance_info)
        transport_cost = get_transport_cost(distance_info)

        budget_amount = int(budget)

        personalized_recommendation = get_personalized_recommendation(
            budget_amount,
            style
)
        weather = get_weather(destination)
        forecast = get_forecast(destination)
        travel_tip = travel_tips.get(
           destination.lower().strip(),
           "💡 Explore the destination, try local food, and enjoy your trip!"
)
        hotel_list = hotel_recommendations.get(
    destination.lower().strip(),
    [
        "🏨 Comfortable local hotel",
        "🏨 Budget-friendly stay",
        "🏨 City center hotel"
    ]
)
        food_list = food_recommendations.get(
    destination.lower().strip(),
    [
        "🍴 Try local food",
        "🥗 Explore local restaurants",
        "🍽️ Try a traditional dish"
    ]
)
        packing_list = packing_lists.get(
        destination.lower().strip(),
        [
            "👕 Comfortable clothes",
            "👟 Comfortable shoes",
            "💧 Water bottle",
            "🎒 Small backpack"
        ]
    )

        weather = get_weather(destination)
         # Smart Budget Breakdown
        budget_amount = int(budget)
        smart_travel_decision = get_smart_travel_decision(distance_info, budget_amount)
        transport = int(budget_amount * 0.25)
        accommodation = int(budget_amount * 0.30)
        food = int(budget_amount * 0.20)
        activities = int(budget_amount * 0.15)
        miscellaneous = budget_amount - (
            transport + accommodation + food + activities
        )

        destination_key = destination.lower().strip()

        places = destinations.get(
            destination_key,
            [
                "📍 Explore popular places",
                "🏛️ Visit local attractions",
                "🍴 Try local food",
                "🛍️ Explore the local market",
                "🌅 Enjoy the local scenery"
            ]
        )
        style_places = travel_styles.get(style, [])

        # Create itinerary
        itinerary = ""

        for day in range(1, days + 1):
            day_transport = get_day_transport(distance_info, day)
            activity1 = places[(day - 1) % len(places)]
            map_place = activity1
            map_url = "https://www.google.com/maps/search/?api=1&query=" + map_place

            if style_places:
                activity2 = style_places[(day - 1) % len(style_places)]
            else:
                activity2 = places[day % len(places)]
            itinerary += f"""
            <div class="day-card">

                <h2>📅 Day {day}</h2>

                <p>📍 <a href="{map_url}" target="_blank">{activity1}</a></p>

                <p>✨ {activity2}</p>

                <p>🎯 Travel Style: <b>{style}</b></p>

                <p>🚗 Transport: <b>{day_transport}</b></p>

                <p> {transport_cost}</p>

                </div>
                """
        summary = f"""
        <div class="day-card">
            <h2>📋 Trip Summary</h2>
            <p>📍 Starting Point: <b>{starting}</b></p>
            <p>🗺️ Destination: <b>{destination}</b></p>
            <p>📅 Duration: <b>{days} days</b></p>
            <p>💰 Total Budget: <b>₹{budget_amount}</b></p>
            <p>🚗 Transport: <b>{transport_suggestion}</b></p>
            <p>💵 Transport Cost: <b>₹{transport_cost}</b></p>
            <p>🏨 Accommodation Budget: <b>₹{accommodation}</b></p>
            <p>🍴 Food Budget: <b>₹{food}</b></p>
            <p>🎯 Activities Budget: <b>₹{activities}</b></p>
       </div>
       """        

        return f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>AI Travel Plan</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: #f0f8ff;
                    margin: 0;
                    padding: 30px;
                }}

                .container {{
                    max-width: 850px;
                    margin: auto;
                }}

                .title {{
                    text-align: center;
                    color: #023e8a;
                    margin-bottom: 30px;
                }}

                .card {{
                    background: white;
                    padding: 25px;
                    margin-bottom: 25px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}

                .details {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                }}

                .detail-box {{
                    background: #e8f7ff;
                    padding: 15px;
                    border-radius: 10px;
                }}

                .day-card {{
                    background: white;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 15px;
                    border-left: 6px solid #0077b6;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                }}

                .day-card h2 {{
                    color: #0077b6;
                }}

                .day-card p {{
                    font-size: 17px;
                    margin: 12px 0;
                }}

                .budget {{
                    background: #e8f7ff;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                }}

                .back {{
                    display: inline-block;
                    padding: 12px 25px;
                    background: #0077b6;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    margin-top: 10px;
                }}

                .back:hover {{
                    background: #023e8a;
                }}

                @media print {{

                    .print-button,
                    .back {{
                        display: none;
                    }}

                    body {{
                        background: white;
                        padding: 10px;
                    }}

                    .card {{
                        box-shadow: none;
                        page-break-inside: avoid;
                    }}

                }}
                   
            </style>

        </head>

        <body>

            <div class="container">

                <h1 class="title">✈️ Your AI Travel Plan 🌍</h1>
<div class="card">

    <h2>🌤️ Current Weather</h2>

    <h3>{destination.title()}</h3>

    <p>{weather}</p>

</div>
<div class="card">

    <h2>📅 5-Day Weather Forecast</h2>

    <ul>
        {"".join(f"<li>{day}</li>" for day in forecast)}
    </ul>

</div>
<div class="card">

    <h2>💡 AI Travel Tip</h2>

    <p>{travel_tip}</p>

</div>
<div class="card">

    <h2>🏨 Recommended Hotels</h2>

    <ul>
    {"".join(
        f'<li>🏨 <a href="https://www.google.com/maps/search/?api=1&query={hotel}" target="_blank">{hotel}</a></li>'
        for hotel in hotel_list
    )}
    </ul>

</div>
<div class="card">

    <h2>🍴 Local Food Recommendations</h2>

    <ul>
    {"".join(
        f'<li>🍴 <a href="https://www.google.com/maps/search/?api=1&query={food}" target="_blank">{food}</a></li>'
        for food in food_list
    )}
    </ul>

</div>
<div class="card">

    <h2>🎒 Smart Packing Checklist</h2>

    <ul>
        {"".join(f"<li>{item}</li>" for item in packing_list)}
    </ul>

</div>
                <div class="card">

                    <h2>🧳 Trip Details</h2>

                    <div class="details">

                        <div class="detail-box">
                            <b>📍 Starting Location</b>
                            <p>{starting}</p>
                        </div>

                        <div class="detail-box">
                            <b>🌴 Destination</b>
                            <p>{destination.title()}</p>
                        </div>

                        <div class="detail-box">
                            <b>📅 Number of Days</b>
                            <p>{days} Days</p>
                        </div>

                        <div class="detail-box">
                            <b>🎯 Travel Style</b>
                            <p>{style}</p>
                        </div>

                    </div>

                </div>
                <div class="card">

                    <h2>🗺️ Distance Information</h2>

                    <p>{distance_info}</p>

                </div>
                <div class="card">

                    <h2>🚌 Transportation Suggestion</h2>

                    <p>{transport_suggestion}</p>

                </div>
                <div class="card">

                    <h2>💰 Estimated Transportation Cost</h2>

                    <p>{transport_cost}</p>

                </div>
                <div class="card">

                    <h2>🗓️ Day-by-Day Itinerary</h2>

                    {itinerary}
                    {summary}
                    <div class="day-card">
                        <h2>🧳 Trip Expense Tracker</h2>

                        <p>💰 Planned Budget: <b>₹{budget_amount}</b></p>

                        <label>Enter your expenses:</label><br><br>

                        <input type="number" id="expense1" placeholder="Transportation">
                        <input type="number" id="expense2" placeholder="Accommodation">
                        <input type="number" id="expense3" placeholder="Food">
                        <input type="number" id="expense4" placeholder="Activities">

                        <br><br>

                        <button onclick="calculateExpenses()">Calculate Remaining Budget</button>

                        <h3 id="expenseResult"></h3>
                    </div>

                    

                    <div class="day-card">
                        <h2>🤖 Smart Travel Recommendation</h2>
                        <p>{smart_travel_decision}</p>
                    </div>
                </div>


                <div class="card">

                    <div class="budget">

    <h2>💰 Smart Budget Breakdown</h2>

    <p><b>Total Budget: ₹{budget_amount}</b></p>

    <p>🚆 Transportation: ₹{transport}</p>

    <p>🏨 Accommodation: ₹{accommodation}</p>

    <p>🍴 Food: ₹{food}</p>

    <p>🎟️ Activities: ₹{activities}</p>

    <p>🛍️ Miscellaneous: ₹{miscellaneous}</p>

    <hr>

    <h3>💰 Total: ₹{budget_amount}</h3>

</div>

                </div>


                <div class="card">
                <div class="card">

    <h2>✨ Personalized AI Recommendation</h2>

    <p>{personalized_recommendation}</p>

</div>

                    <h2>🎉 Have a great trip!</h2>

                    <p>Your AI-generated travel plan is ready.</p>
                    <button class="print-button" onclick="window.print()">
                       📄 Download / Print Travel Plan
                    </button>

                    <a class="back" href="/">
                        ← Plan Another Trip
                    </a>

                </div>

            </div>

        </body>

        </html>
        """

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)