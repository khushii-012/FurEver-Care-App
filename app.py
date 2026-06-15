import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

from utils.db import create_table, add_pet, get_pets
from utils.ai import (
    analyze_pet_health,
    generate_food_plan,
    analyze_rescue_case,
    analyze_rescue_image
)

create_table()

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FurEver Care 🐾",
    page_icon="🐶",
    layout="wide"
)

geolocator = Nominatim(user_agent="furever_app")

API_KEY = st.secrets.get("API_KEY", None)

# ---------------- SESSION STATE ----------------
if "map_lat" not in st.session_state:
    st.session_state["map_lat"] = 20.5937

if "map_lon" not in st.session_state:
    st.session_state["map_lon"] = 78.9629

if "reports" not in st.session_state:
    st.session_state["reports"] = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🐾 FurEver Care")

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Home",
        "Pet Profile",
        "Health Assistant",
        "Food Recommendation",
        "Vaccination Reminder",
        "Emergency Rescue"
    ],
    key="main_menu"
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("🐶 FurEver Care")
    st.subheader("Your AI Powered Pet Care Companion ❤️")

# ---------------- PET PROFILE ----------------
elif menu == "Pet Profile":
    st.title("🐾 Pet Profile")

    name = st.text_input("Pet Name")
    age = st.number_input("Age", 0, 30)
    breed = st.text_input("Breed")
    weight = st.number_input("Weight", 0.0, 100.0)

    if st.button("Save Pet", key="save_pet"):
        add_pet(name, age, breed, weight)
        st.success("Pet saved!")

    st.subheader("Saved Pets")
    for pet in get_pets():
        st.write(pet)

# ---------------- HEALTH ----------------
elif menu == "Health Assistant":
    st.title("🧠 Health Assistant")

    symptoms = st.text_area("Enter symptoms")

    if st.button("Analyze", key="health_btn"):
        if symptoms:
            result = analyze_pet_health(symptoms)
            st.write(result)
        else:
            st.warning("Enter symptoms")

# ---------------- FOOD ----------------
elif menu == "Food Recommendation":
    st.title("🍲 Food Recommendation")

    breed = st.text_input("Breed")
    age = st.number_input("Age", 0, 30)
    weight = st.number_input("Weight", 0.0, 100.0)

    if st.button("Get Diet Plan", key="food_btn"):
        if breed:
            result = generate_food_plan(breed, age, weight)
            st.write(result)
        else:
            st.warning("Enter breed")

# ---------------- VACCINATION ----------------
elif menu == "Vaccination Reminder":
    st.title("💉 Vaccination Reminder")
    st.info("Coming soon")

# ---------------- RESCUE ----------------
elif menu == "Emergency Rescue":
    st.title("🚑 Emergency Rescue")

    image = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
    location = st.text_input("Location")
    description = st.text_area("Description")

    if st.button("Send Alert", key="rescue_btn"):

        if location and description:

            if image:
                result = analyze_rescue_image(image, description, location)
            else:
                result = analyze_rescue_case(description, location)

            st.write(result)

            # fake coordinates (you already had geopy logic earlier)
            lat, lon = 20.5937, 78.9629

            st.session_state["reports"].append({
                "lat": lat,
                "lon": lon,
                "description": description
            })

            st.success("Report sent!")

        else:
            st.warning("Fill all fields")

# ---------------- MAP ----------------
st.markdown("## 🗺️ Rescue Map")

m = folium.Map(
    location=[st.session_state["map_lat"], st.session_state["map_lon"]],
    zoom_start=5
)

for r in st.session_state["reports"]:
    folium.Marker(
        [r["lat"], r["lon"]],
        popup=r["description"]
    ).add_to(m)

st_folium(m, width=900, height=500)
