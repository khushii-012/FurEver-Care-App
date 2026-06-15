<<<<<<< HEAD
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="furever-care-app")

# convert place → coordinates
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        return None
    except:
        return None


# sample real-world rescue points (you can expand later or replace with API)
RESCUE_POINTS = [
    {"name": "City Pet Clinic", "type": "vet", "coords": (21.1458, 79.0882)},
    {"name": "Animal Care Hospital", "type": "vet", "coords": (21.1500, 79.0900)},
    {"name": "Stray Animal NGO", "type": "ngo", "coords": (21.1400, 79.0950)},
    {"name": "Paws Rescue Center", "type": "ngo", "coords": (21.1550, 79.1000)},
]


# find nearest help
def find_nearby_help(location):
    user_coords = get_coordinates(location)

    if not user_coords:
        return None

    results = []

    for place in RESCUE_POINTS:
        distance = geodesic(user_coords, place["coords"]).km
        results.append({
            "name": place["name"],
            "type": place["type"],
            "distance": round(distance, 2)
        })

    # sort by closest first
    results.sort(key=lambda x: x["distance"])

=======
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="furever-care-app")

# convert place → coordinates
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        return None
    except:
        return None


# sample real-world rescue points (you can expand later or replace with API)
RESCUE_POINTS = [
    {"name": "City Pet Clinic", "type": "vet", "coords": (21.1458, 79.0882)},
    {"name": "Animal Care Hospital", "type": "vet", "coords": (21.1500, 79.0900)},
    {"name": "Stray Animal NGO", "type": "ngo", "coords": (21.1400, 79.0950)},
    {"name": "Paws Rescue Center", "type": "ngo", "coords": (21.1550, 79.1000)},
]


# find nearest help
def find_nearby_help(location):
    user_coords = get_coordinates(location)

    if not user_coords:
        return None

    results = []

    for place in RESCUE_POINTS:
        distance = geodesic(user_coords, place["coords"]).km
        results.append({
            "name": place["name"],
            "type": place["type"],
            "distance": round(distance, 2)
        })

    # sort by closest first
    results.sort(key=lambda x: x["distance"])

>>>>>>> 79aed5a (FurEver Care project)
    return results