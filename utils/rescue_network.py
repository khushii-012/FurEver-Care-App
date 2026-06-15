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