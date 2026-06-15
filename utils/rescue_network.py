import requests

def get_nearby_vets(lat, lon):
    query = f"""
    [out:json];
    node["amenity"="veterinary"](around:5000,{lat},{lon});
    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    try:
        response = requests.get(url, params={"data": query}, timeout=10)
        data = response.json()

        vets = []

        for element in data.get("elements", []):
            tags = element.get("tags", {})

            vets.append({
                "name": tags.get("name", "Vet Clinic"),
                "lat": element.get("lat"),
                "lon": element.get("lon")
            })

        return vets

    except Exception as e:
        print("Error fetching vets:", e)
        return []

def get_nearby_vets(location):
    # MVP static data (later we connect API / Google Maps)
    return [
        {"name": "City Pet Clinic", "contact": "9876543210", "distance": "2 km"},
        {"name": "Animal Care Hospital", "contact": "9123456780", "distance": "3.5 km"},
        {"name": "Paws Veterinary Center", "contact": "9988776655", "distance": "4 km"}
    ]


def get_nearby_ngos(location):
    return [
        {"name": "Animal Rescue Trust", "contact": "9112233445", "distance": "1.5 km"},
        {"name": "Stray Care Foundation", "contact": "9001122334", "distance": "3 km"},
        {"name": "Paw Protect NGO", "contact": "8899001122", "distance": "5 km"}
    ]
def get_nearby_vets(location):
    # MVP static data (later we connect API / Google Maps)
    return [
        {"name": "City Pet Clinic", "contact": "9876543210", "distance": "2 km"},
        {"name": "Animal Care Hospital", "contact": "9123456780", "distance": "3.5 km"},
        {"name": "Paws Veterinary Center", "contact": "9988776655", "distance": "4 km"}
    ]


def get_nearby_ngos(location):
    return [
        {"name": "Animal Rescue Trust", "contact": "9112233445", "distance": "1.5 km"},
        {"name": "Stray Care Foundation", "contact": "9001122334", "distance": "3 km"},
        {"name": "Paw Protect NGO", "contact": "8899001122", "distance": "5 km"}
    ]

