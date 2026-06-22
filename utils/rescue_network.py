import requests


def get_nearby_vets(lat, lon):
    """
    Fetch nearby vets using OpenStreetMap Overpass API.
    Falls back to static data if API fails.
    """
    try:
        query = f"""
[out:json];
node["amenity"="veterinary"](around:5000,{lat},{lon});
out;
"""
        url = "https://overpass-api.de/api/interpreter"
        response = requests.get(url, params={"data": query}, timeout=10)
        data = response.json()

        vets = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            vets.append({
                "name": tags.get("name", "Vet Clinic"),
                "lat": element.get("lat"),
                "lon": element.get("lon"),
                "contact": tags.get("phone", "N/A")
            })

        # ✅ FIX 2: Agar API se kuch mila toh return karo, warna fallback
        if vets:
            return vets

    except Exception as e:
        print(f"Overpass API error: {e}")

    # Fallback static data
    return [
        {"name": "City Pet Clinic", "contact": "9876543210", "lat": lat + 0.01, "lon": lon + 0.01},
        {"name": "Animal Care Hospital", "contact": "9123456780", "lat": lat - 0.01, "lon": lon + 0.02},
        {"name": "Paws Veterinary Center", "contact": "9988776655", "lat": lat + 0.02, "lon": lon - 0.01},
    ]


def get_nearby_ngos(lat, lon):
    """
    Returns nearby animal rescue NGOs.
    Currently static — can be replaced with a real NGO database later.
    """
    return [
        {"name": "Animal Rescue Trust", "contact": "9112233445", "lat": lat + 0.015, "lon": lon - 0.015},
        {"name": "Stray Care Foundation", "contact": "9001122334", "lat": lat - 0.02, "lon": lon + 0.01},
        {"name": "Paw Protect NGO", "contact": "8899001122", "lat": lat + 0.025, "lon": lon + 0.025},
    ]