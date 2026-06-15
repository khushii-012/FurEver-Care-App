import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

from utils.db import create_table, add_pet, get_pets

from utils.ai import analyze_pet_health, generate_food_plan, analyze_rescue_case, analyze_rescue_image
from utils.rescue_network import get_nearby_vets, get_nearby_ngos
from utils.location_service import find_nearby_help

create_table()

geolocator = Nominatim(user_agent="furever_app")

# ---------------- PAGE CONFIG ----------------

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


API_KEY = st.secrets["API_KEY"]

# ---------------- USER LOCATION (FALLBACK) ----------------
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return None, None

# ---------------- SESSION STATE INIT ----------------
if "map_lat" not in st.session_state:
    st.session_state.map_lat = 20.5937

if "map_lon" not in st.session_state:
    st.session_state.map_lon = 78.9629

if "reports" not in st.session_state:
    st.session_state.reports = []

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

    st.markdown("""
    Welcome to **FurEver Care**

    - Pet Profile Management  
    - AI Health Assistant  
    - Food Recommendation  
    - Emergency Rescue System  

    🐶 Because every pet deserves care.
    """)

# ---------------- PET PROFILE ----------------
elif menu == "Pet Profile":
    st.title("🐾 Pet Profile")

    name = st.text_input("Pet Name")
    age = st.number_input("Age", 0, 30)
    breed = st.text_input("Breed")
    weight = st.number_input("Weight (kg)", 0.0, 100.0)

    if st.button("Save Pet"):
        add_pet(name, age, breed, weight)
        st.success("Pet saved successfully 🐶")

    st.subheader("Saved Pets")
    pets = get_pets()

    for p in pets:
        st.write(f"{p[1]} | Age {p[2]} | Breed {p[3]} | {p[4]} kg")

# ---------------- HEALTH ----------------
elif menu == "Health Assistant":
    st.title("🧠 AI Health Assistant")

    symptoms = st.text_area("Enter Symptoms")

    if st.button("Analyze", key="health_btn"):
        if symptoms.strip():
            with st.spinner("Analyzing..."):
                result = analyze_pet_health(symptoms)
            st.success("Done")
            st.write(result)
        else:
            st.warning("Enter symptoms")

# ---------------- FOOD ----------------
elif menu == "Food Recommendation":
    st.title("🍲 Food Recommendation")

    breed = st.text_input("Breed")
    age = st.number_input("Age", 0, 30)
    weight = st.number_input("Weight", 0.0, 100.0)

    if st.button("Get Plan"):
        if breed.strip():
            with st.spinner("Generating diet plan..."):
                result = generate_food_plan(breed, age, weight)
            st.success("Ready")
            st.write(result)
        else:
            st.warning("Enter breed")

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

    st.title("🚑 Emergency Animal Rescue")

    image = st.file_uploader("Upload Animal Photo", type=["jpg", "png", "jpeg"])
    location = st.text_input("Enter Location")
    description = st.text_area("Describe Situation")

    if st.button("Send Rescue Alert", key="rescue_btn"):

        if location.strip() == "" or description.strip() == "":
            st.warning("Fill all details")

        else:
            with st.spinner("Processing rescue report 🧠"):

                if image:
                    result = analyze_rescue_image(image, description, location)
                else:
                    result = analyze_rescue_case(description, location)

                lat, lon = get_coordinates(location)

                if lat is None or lon is None:
                    lat, lon = st.session_state.map_lat, st.session_state.map_lon

                st.session_state.reports.append({
                    "lat": lat,
                    "lon": lon,
                    "description": description
                })

                st.session_state.map_lat = lat
                st.session_state.map_lon = lon

            st.success("Report Generated 🚨")
            st.write(result)

            if image:
                st.image(image)

    # ---------------- MAP (INSIDE RESCUE ONLY) ----------------
    st.markdown("## 🗺️ Rescue Map")

    m = folium.Map(
        location=[st.session_state.map_lat, st.session_state.map_lon],
        zoom_start=13
    )

    # USER REPORTS (RED)
    for r in st.session_state.reports:
        folium.Marker(
            [r["lat"], r["lon"]],
            popup=r["description"],
            icon=folium.Icon(color="red")
        ).add_to(m)

    # VETS (GREEN)
    try:
        vets = get_nearby_vets(
            st.session_state.map_lat,
            st.session_state.map_lon
        )

        for v in vets:
            folium.Marker(
                [v["lat"], v["lon"]],
                popup=v["name"],
                icon=folium.Icon(color="green")
            ).add_to(m)

    except:
        st.warning("Vet data not available")

    st_folium(m, width=900, height=500)

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

