import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

from utils.db import create_table, add_pet, get_pets
from utils.ai import analyze_pet_health, generate_food_plan, analyze_rescue_case, analyze_rescue_image
from utils.rescue_network import get_nearby_vets, get_nearby_ngos

# ---------------- INIT ----------------
create_table()
geolocator = Nominatim(user_agent="furever_app")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FurEver Care 🐾",
    page_icon="🐶",
    layout="wide"
)

# ---------------- HELPERS ----------------
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return None, None

# ---------------- SESSION STATE ----------------
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
        "🏠 Home",
        "🐾 Pet Profile",
        "🧠 Health Assistant",
        "🍲 Food Recommendation",
        "💉 Vaccination Reminder",
        "🚨 Emergency Rescue"
    ]
)

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.title("🐶 FurEver Care")
    st.subheader("Your AI Powered Pet Care Companion ❤️")
    st.markdown("""
    Welcome to **FurEver Care** — because every fur deserves care.

    **Features:**
    - 🐾 Pet Profile Management
    - 🧠 AI Health Assistant
    - 🍲 Smart Food Recommendation
    - 💉 Vaccination Reminder
    - 🚨 Emergency Animal Rescue
    """)

# ---------------- PET PROFILE ----------------
elif menu == "🐾 Pet Profile":
    st.title("🐾 Pet Profile")

    with st.form("pet_form"):
        name   = st.text_input("Pet Name")
        age    = st.number_input("Age (years)", 0, 30)
        breed  = st.text_input("Breed")
        weight = st.number_input("Weight (kg)", 0.0, 100.0)
        submit = st.form_submit_button("Save Pet")

    if submit:
        if name.strip() and breed.strip():
            add_pet(name, age, breed, weight)
            st.success(f"✅ {name} saved successfully!")
        else:
            st.warning("Please fill in Pet Name and Breed.")

    st.subheader("📋 Saved Pets")
    pets = get_pets()
    if pets:
        for p in pets:
            st.write(f"**{p[1]}** | Age: {p[2]} yrs | Breed: {p[3]} | Weight: {p[4]} kg")
    else:
        st.info("No pets saved yet.")

# ---------------- HEALTH ASSISTANT ----------------
elif menu == "🧠 Health Assistant":
    st.title("🧠 AI Health Assistant")
    st.caption("Describe your pet's symptoms and AI will analyze them.")

    symptoms = st.text_area("Enter Symptoms", placeholder="e.g. vomiting, not eating, lethargic...")

    if st.button("Analyze Symptoms"):
        if symptoms.strip():
            with st.spinner("Analyzing symptoms..."):
                result = analyze_pet_health(symptoms)
            st.markdown("### 🩺 Analysis Result")
            st.write(result)
            st.warning("⚠️ This is AI guidance only. Always consult a real vet for medical decisions.")
        else:
            st.warning("Please enter symptoms first.")

# ---------------- FOOD RECOMMENDATION ----------------
elif menu == "🍲 Food Recommendation":
    st.title("🍲 Food Recommendation")
    st.caption("Get a personalized diet plan for your pet.")

    breed  = st.text_input("Breed", placeholder="e.g. Labrador, Persian Cat")
    age    = st.number_input("Age (years)", 0, 30)
    weight = st.number_input("Weight (kg)", 0.0, 100.0)

    if st.button("Generate Diet Plan"):
        if breed.strip():
            with st.spinner("Creating personalized food plan..."):
                result = generate_food_plan(breed, age, weight)
            st.markdown("### 🥗 Your Pet's Diet Plan")
            st.write(result)
        else:
            st.warning("Please enter breed.")

# ---------------- VACCINATION REMINDER ----------------
elif menu == "💉 Vaccination Reminder":
    st.title("💉 Vaccination Reminder")
    st.caption("Track and manage your pet's vaccination schedule.")

    with st.form("vax_form"):
        pet_name  = st.text_input("Pet Name")
        vaccine   = st.selectbox("Vaccine", [
            "Rabies", "Distemper", "Parvovirus", "Hepatitis",
            "Leptospirosis", "Bordetella", "Other"
        ])
        last_date = st.date_input("Last Vaccination Date")
        next_date = st.date_input("Next Due Date")
        vet_name  = st.text_input("Vet Name (optional)")
        save_vax  = st.form_submit_button("Save Reminder")

    if save_vax:
        if pet_name.strip():
            if "vaccinations" not in st.session_state:
                st.session_state.vaccinations = []
            st.session_state.vaccinations.append({
                "pet": pet_name,
                "vaccine": vaccine,
                "last": str(last_date),
                "next": str(next_date),
                "vet": vet_name
            })
            st.success(f"✅ Reminder saved! {pet_name}'s {vaccine} is due on {next_date}.")
        else:
            st.warning("Please enter pet name.")

    st.subheader("📋 Saved Reminders")
    vaccs = st.session_state.get("vaccinations", [])
    if vaccs:
        for v in vaccs:
            st.write(f"**{v['pet']}** | {v['vaccine']} | Next due: {v['next']}")
    else:
        st.info("No reminders saved yet.")

# ---------------- EMERGENCY RESCUE ----------------
elif menu == "🚨 Emergency Rescue":
    st.title("🚑 Emergency Animal Rescue")
    st.caption("Report an injured animal and find nearby help.")

    image       = st.file_uploader("Upload Animal Photo (optional)", type=["jpg", "png", "jpeg"])
    location    = st.text_input("Location", placeholder="e.g. Andheri West, Mumbai")
    description = st.text_area("Describe the Situation", placeholder="e.g. dog hit by car, bleeding from leg...")

    if st.button("🚨 Send Rescue Alert"):
        if not location.strip() or not description.strip():
            st.warning("Please fill in both Location and Description.")
        else:
            with st.spinner("Analyzing rescue situation..."):
                if image:
                    result = analyze_rescue_image(image, description, location)
                else:
                    result = analyze_rescue_case(description, location)

            st.markdown("### 🧠 AI Rescue Analysis")
            st.write(result)

            if image:
                st.image(image, caption="Uploaded Animal Photo", width=400)

            lat, lon = get_coordinates(location)
            if lat is None:
                lat, lon = st.session_state.map_lat, st.session_state.map_lon
                st.warning("⚠️ Could not find exact coordinates. Using approximate location.")

            st.session_state.reports.append({"lat": lat, "lon": lon, "description": description})
            st.session_state.map_lat = lat
            st.session_state.map_lon = lon
            st.success("✅ Report submitted!")

    # Nearby help section
    if st.session_state.reports:
        lat = st.session_state.map_lat
        lon = st.session_state.map_lon

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏥 Nearby Vets")
            vets = get_nearby_vets(lat, lon)
            for v in vets:
                st.write(f"📍 **{v['name']}** | 📞 {v.get('contact', 'N/A')}")

        with col2:
            st.subheader("🤝 Nearby NGOs")
            ngos = get_nearby_ngos(lat, lon)
            for n in ngos:
                st.write(f"📍 **{n['name']}** | 📞 {n.get('contact', 'N/A')}")

    # Map
    st.markdown("### 🗺️ Rescue Map")
    m = folium.Map(
        location=[st.session_state.map_lat, st.session_state.map_lon],
        zoom_start=13
    )

    for r in st.session_state.reports:
        folium.Marker(
            [r["lat"], r["lon"]],
            popup=r["description"],
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(m)

    if st.session_state.reports:
        try:
            vets = get_nearby_vets(st.session_state.map_lat, st.session_state.map_lon)
            for v in vets:
                if v.get("lat") and v.get("lon"):
                    folium.Marker(
                        [v["lat"], v["lon"]],
                        popup=v["name"],
                        icon=folium.Icon(color="green", icon="plus-sign")
                    ).add_to(m)
        except:
            pass

    st_folium(m, width=900, height=500)