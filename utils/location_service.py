from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="furever-care-app")


def get_coordinates(location):
    """Convert a place name to (lat, lon) coordinates."""
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None


# Static rescue points (expandable later)
RESCUE_POINTS = [
    {"name": "City Pet Clinic", "type": "vet", "coords": (21.1458, 79.0882)},
    {"name": "Animal Care Hospital", "type": "vet", "coords": (21.1500, 79.0900)},
    {"name": "Stray Animal NGO", "type": "ngo", "coords": (21.1400, 79.0950)},
    {"name": "Paws Rescue Center", "type": "ngo", "coords": (21.1550, 79.1000)},
]


def find_nearby_help(location):
    """Find nearest vets and NGOs from a given location string."""
    user_coords = get_coordinates(location)

    if not user_coords:
        return None

    results = []
    for place in RESCUE_POINTS:
        distance = geodesic(user_coords, place["coords"]).km
        results.append({
            "name": place["name"],
            "type": place["type"],
            "distance": round(distance, 2),
            "lat": place["coords"][0],
            "lon": place["coords"][1],
        })

    results.sort(key=lambda x: x["distance"])
    return results  # ✅ FIX 3: return statement pehle missing tha