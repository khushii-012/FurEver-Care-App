import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import pandas as pd
#import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim 
from utils.db import create_table, add_pet, get_pets
create_table()
from utils.ai import analyze_pet_health
from utils.ai import generate_food_plan
from utils.ai import analyze_rescue_case
from utils.ai import analyze_rescue_image
from utils.rescue_network import get_nearby_vets, get_nearby_ngos
from utils.location_service import find_nearby_help

from google import genai

geolocator = Nominatim(user_agent="furever_app")

API_KEY = st.secrets["API_KEY"]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FurEver Care 🐾",
    page_icon="🐶",
    layout="wide"
)

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
        "Emergency Rescue (Coming Soon)"
    ]
)

# ---------------- HOME PAGE ----------------
if menu == "Home":
    st.title("🐶 FurEver Care")
    st.subheader("Your AI Powered Pet Care Companion ❤️")

    st.markdown("""
    Welcome to **FurEver Care**, a smart AI system designed to help you take care of your pets.

    ### 🐾 Features:
    - Pet Profile Management
    - AI Health Assistant
    - Food Recommendation System
    - Vaccination Reminders
    - Emergency Animal Rescue (Coming Soon)

    ---
    🐶 *Because every pet deserves FurEver Care.*
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
        st.success(f"{name} saved successfully! 🐶")

    st.subheader("📋 Saved Pets")

    pets = get_pets()

    for pet in pets:
        st.write(f"🐶 {pet[1]} | Age: {pet[2]} | Breed: {pet[3]} | Weight: {pet[4]} kg")

# ---------------- HEALTH ASSISTANT ----------------
elif menu == "Health Assistant":
    st.title("🧠 AI Health Assistant")

    symptoms = st.text_area("Enter Symptoms")

    if st.button("Analyze", key="health_analyze_btn"):
        if symptoms.strip() == "":
            st.warning("Please enter symptoms")
        else:
            with st.spinner("AI analyzing symptoms... 🧠"):
                result = analyze_pet_health(symptoms)

            st.success("Analysis Complete 🐶")
            st.write(result)

# ---------------- FOOD RECOMMENDATION ----------------
elif menu == "Food Recommendation":
    st.title("🍲 Food Recommendation")

    breed = st.text_input("Breed")
    age = st.number_input("Age", 0, 30)
    weight = st.number_input("Weight", 0.0, 100.0)

    if st.button("Get Diet Plan", key="food_btn"):
        if breed.strip() == "":
            st.warning("Please enter breed")
        else:
            with st.spinner("Generating AI diet plan... 🍲"):
                result = generate_food_plan(breed, age, weight)

            st.success("Diet Plan Ready 🐶")
            st.write(result)
# ---------------- VACCINATION ----------------
elif menu == "Vaccination Reminder":
    st.title("💉 Vaccination Reminder")

    st.info("We will add vaccination tracker + alerts here")


def get_coordinates(location):
    loc = geolocator.geocode(location)
    if loc:
        return loc.latitude, loc.longitude
    return None, None


if "map_lat" not in st.session_state:
    st.session_state["map_lat"] = 20.5937

if "map_lon" not in st.session_state:
    st.session_state["map_lon"] = 78.9629

if "reports" not in st.session_state:
    st.session_state["reports"] = []

# ---------------- RESCUE ----------------
st.title("🚑 Emergency Animal Rescue")

st.markdown("Report injured or stray animals so help can reach them faster 🐾")

# 📸 Upload image
image = st.file_uploader("Upload Animal Photo", type=["jpg", "png", "jpeg"])

# 📍 Location input
location = st.text_input("Enter Location / Area / Landmark")

# 📝 Description
description = st.text_area("Describe the situation (injury, behavior, etc.)")

# 🚨 Submit button
if st.button("Send Rescue Alert", key="rescue_btn"):

    if location.strip() == "" or description.strip() == "":
        st.warning("Please fill all details")

    else:
        with st.spinner("AI analyzing image + situation 🧠🚑..."):

            # AI analysis
            if image:
                result = analyze_rescue_image(image, description, location)
            else:
                result = analyze_rescue_case(description, location)
              
            # 🧠 convert location to coordinates
            lat, lon = get_coordinates(location)

            # 🗺️ STORE REPORT IN SESSION STATE
            if lat is not None and lon is not None:
                st.session_state["map_lat"] = lat
                st.session_state["map_lon"] = lon


                if "reports" not in st.session_state:
                    st.session_state["reports"] = []

                st.session_state["reports"].append({
                    "lat": lat,
                    "lon": lon,
                    "description": description
                })

        # ✅ ALL OUTPUTS MUST BE INSIDE BUTTON LOGIC
        st.success("🚨 AI Rescue Report Generated")
        st.write(result)

        if image:
            st.image(image, caption="Reported Animal Image")



        if "map_lat" not in st.session_state:
          st.session_state["map_lat"] = 20.5937

        if "map_lon" not in st.session_state:
         st.session_state["map_lon"] = 78.9629
# ---------------- MAP SECTION ----------------

st.markdown("## 🗺️ Rescue Map")

m = folium.Map(
    location=[
        st.session_state["map_lat"],
        st.session_state["map_lon"]
    ],
    zoom_start=14
)

for r in st.session_state["reports"]:

    folium.Marker(
        location=[r["lat"], r["lon"]],
        popup=r["description"],
        icon=folium.Icon(color="red")
    ).add_to(m)

st_folium(m, width=900, height=500)
=======
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim 
from utils.db import create_table, add_pet, get_pets
create_table()
from utils.ai import analyze_pet_health
from utils.ai import generate_food_plan
from utils.ai import analyze_rescue_case
from utils.ai import analyze_rescue_image
from utils.rescue_network import get_nearby_vets, get_nearby_ngos
from utils.location_service import find_nearby_help

from google import genai

geolocator = Nominatim(user_agent="furever_app")


API_KEY = st.secrets["API_KEY"]
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FurEver Care 🐾",
    page_icon="🐶",
    layout="wide"
)

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
        "Emergency Rescue (Coming Soon)"
    ]
)

# ---------------- HOME PAGE ----------------
if menu == "Home":
    st.title("🐶 FurEver Care")
    st.subheader("Your AI Powered Pet Care Companion ❤️")

    st.markdown("""
    Welcome to **FurEver Care**, a smart AI system designed to help you take care of your pets.

    ### 🐾 Features:
    - Pet Profile Management
    - AI Health Assistant
    - Food Recommendation System
    - Vaccination Reminders
    - Emergency Animal Rescue (Coming Soon)

    ---
    🐶 *Because every pet deserves FurEver Care.*
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
        st.success(f"{name} saved successfully! 🐶")

    st.subheader("📋 Saved Pets")

    pets = get_pets()

    for pet in pets:
        st.write(f"🐶 {pet[1]} | Age: {pet[2]} | Breed: {pet[3]} | Weight: {pet[4]} kg")

# ---------------- HEALTH ASSISTANT ----------------
elif menu == "Health Assistant":
    st.title("🧠 AI Health Assistant")

    symptoms = st.text_area("Enter Symptoms")

    if st.button("Analyze", key="health_analyze_btn"):
        if symptoms.strip() == "":
            st.warning("Please enter symptoms")
        else:
            with st.spinner("AI analyzing symptoms... 🧠"):
                result = analyze_pet_health(symptoms)

            st.success("Analysis Complete 🐶")
            st.write(result)

# ---------------- FOOD RECOMMENDATION ----------------
elif menu == "Food Recommendation":
    st.title("🍲 Food Recommendation")

    breed = st.text_input("Breed")
    age = st.number_input("Age", 0, 30)
    weight = st.number_input("Weight", 0.0, 100.0)

    if st.button("Get Diet Plan", key="food_btn"):
        if breed.strip() == "":
            st.warning("Please enter breed")
        else:
            with st.spinner("Generating AI diet plan... 🍲"):
                result = generate_food_plan(breed, age, weight)

            st.success("Diet Plan Ready 🐶")
            st.write(result)
# ---------------- VACCINATION ----------------
elif menu == "Vaccination Reminder":
    st.title("💉 Vaccination Reminder")

    st.info("We will add vaccination tracker + alerts here")


def get_coordinates(location):
    loc = geolocator.geocode(location)
    if loc:
        return loc.latitude, loc.longitude
    return None, None


if "map_lat" not in st.session_state:
    st.session_state["map_lat"] = 20.5937

if "map_lon" not in st.session_state:
    st.session_state["map_lon"] = 78.9629

if "reports" not in st.session_state:
    st.session_state["reports"] = []

# ---------------- RESCUE ----------------
st.title("🚑 Emergency Animal Rescue")

st.markdown("Report injured or stray animals so help can reach them faster 🐾")

# 📸 Upload image
image = st.file_uploader("Upload Animal Photo", type=["jpg", "png", "jpeg"])

# 📍 Location input
location = st.text_input("Enter Location / Area / Landmark")

# 📝 Description
description = st.text_area("Describe the situation (injury, behavior, etc.)")

# 🚨 Submit button
if st.button("Send Rescue Alert", key="rescue_btn"):

    if location.strip() == "" or description.strip() == "":
        st.warning("Please fill all details")

    else:
        with st.spinner("AI analyzing image + situation 🧠🚑..."):

            # AI analysis
            if image:
                result = analyze_rescue_image(image, description, location)
            else:
                result = analyze_rescue_case(description, location)
              
            # 🧠 convert location to coordinates
            lat, lon = get_coordinates(location)

            # 🗺️ STORE REPORT IN SESSION STATE
            if lat is not None and lon is not None:
                st.session_state["map_lat"] = lat
                st.session_state["map_lon"] = lon


                if "reports" not in st.session_state:
                    st.session_state["reports"] = []

                st.session_state["reports"].append({
                    "lat": lat,
                    "lon": lon,
                    "description": description
                })

        # ✅ ALL OUTPUTS MUST BE INSIDE BUTTON LOGIC
        st.success("🚨 AI Rescue Report Generated")
        st.write(result)

        if image:
            st.image(image, caption="Reported Animal Image")



        if "map_lat" not in st.session_state:
          st.session_state["map_lat"] = 20.5937

        if "map_lon" not in st.session_state:
         st.session_state["map_lon"] = 78.9629
# ---------------- MAP SECTION ----------------

st.markdown("## 🗺️ Rescue Map")

m = folium.Map(
    location=[
        st.session_state["map_lat"],
        st.session_state["map_lon"]
    ],
    zoom_start=14
)

for r in st.session_state["reports"]:

    folium.Marker(
        location=[r["lat"], r["lon"]],
        popup=r["description"],
        icon=folium.Icon(color="red")
    ).add_to(m)

st_folium(m, width=900, height=500)

