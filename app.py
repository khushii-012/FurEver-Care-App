import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from datetime import date
import base64
from io import BytesIO

from utils.db import (
    create_table, add_pet, get_pets, delete_pet,
    add_vaccination, get_vaccinations,
    add_missing_pet, get_missing_pets, mark_pet_found,
    add_rescue_report, get_rescue_reports
)
from utils.ai import analyze_pet_health, generate_food_plan, analyze_rescue_case, analyze_rescue_image
from utils.rescue_network import get_nearby_vets, get_nearby_ngos

# ---------------- INIT ----------------
create_table()
geolocator = Nominatim(user_agent="furever_app")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FurEver Care 🐾", page_icon="🐾", layout="wide")

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

/* Dark background */
.stApp {
    background: #0F0A1E !important;
}

/* Hide default streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1A0F35 !important;
    border-right: 1px solid #2A1F4A !important;
}
[data-testid="stSidebar"] * {
    color: #C0A0E0 !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stSidebar"] .stSelectbox label {
    color: #FF3CAC !important;
    font-weight: 800 !important;
    font-size: 13px !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #2A1F4A !important;
    border: 1px solid #3A2F5A !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #1E1235 !important;
    border: 1px solid #3A2F5A !important;
    color: white !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #FF3CAC !important;
    box-shadow: 0 0 0 2px rgba(255,60,172,0.2) !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stNumberInput label,
.stSelectbox label, .stFileUploader label, .stDateInput label {
    color: #A080C0 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #FF3CAC, #7B2FFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,60,172,0.4) !important;
}

/* Form submit button */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #FF3CAC, #7B2FFF) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    width: 100% !important;
    padding: 12px !important;
}

/* Alerts */
.stSuccess { background: rgba(0,200,83,0.15) !important; border: 1px solid rgba(0,200,83,0.3) !important; border-radius: 12px !important; color: #00C853 !important; }
.stWarning { background: rgba(255,179,0,0.15) !important; border: 1px solid rgba(255,179,0,0.3) !important; border-radius: 12px !important; }
.stError   { background: rgba(255,60,172,0.15) !important; border: 1px solid rgba(255,60,172,0.3) !important; border-radius: 12px !important; }
.stInfo    { background: rgba(123,47,255,0.15) !important; border: 1px solid rgba(123,47,255,0.3) !important; border-radius: 12px !important; color: #C0A0E0 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #FF3CAC !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: #1E1235 !important;
    border: 2px dashed #3A2F5A !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

/* Date input */
.stDateInput > div > div > input {
    background: #1E1235 !important;
    border: 1px solid #3A2F5A !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F0A1E; }
::-webkit-scrollbar-thumb { background: #3A2F5A; border-radius: 3px; }

/* Divider */
hr { border-color: #2A1F4A !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return None, None

def img_to_base64(img_bytes):
    return base64.b64encode(img_bytes).decode()

def hero_banner(title, subtitle, emoji):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1A0F35,#2A1050);border-radius:20px;
                padding:28px 28px 20px;margin-bottom:24px;position:relative;overflow:hidden;
                border:1px solid #3A2F5A;">
        <div style="position:absolute;width:180px;height:180px;border-radius:50%;
                    background:#FF3CAC;opacity:0.1;top:-60px;right:-40px;"></div>
        <div style="position:absolute;width:120px;height:120px;border-radius:50%;
                    background:#7B2FFF;opacity:0.12;bottom:-30px;right:80px;"></div>
        <div style="font-size:40px;margin-bottom:8px;">{emoji}</div>
        <div style="color:white;font-size:24px;font-weight:900;letter-spacing:-0.5px;">{title}</div>
        <div style="color:#8060A0;font-size:13px;margin-top:4px;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def stat_cards(stats):
    cols = st.columns(len(stats))
    colors = ["#FF3CAC", "#7B2FFF", "#00F5FF", "#FFB300", "#00C853"]
    for i, (col, (icon, num, label)) in enumerate(zip(cols, stats)):
        c = colors[i % len(colors)]
        col.markdown(f"""
        <div style="background:linear-gradient(135deg,{c}15,{c}30);border:1px solid {c}44;
                    border-radius:16px;padding:16px 12px;text-align:center;">
            <div style="font-size:26px;">{icon}</div>
            <div style="color:white;font-size:24px;font-weight:900;">{num}</div>
            <div style="color:#8070B0;font-size:11px;margin-top:2px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

def feature_card(icon, title, sub, color):
    return f"""
    <div style="background:{color}18;border:1px solid {color}44;border-radius:16px;
                padding:16px 14px;cursor:pointer;position:relative;overflow:hidden;height:100%;">
        <div style="position:absolute;font-size:48px;opacity:0.08;bottom:-8px;right:-4px;transform:rotate(15deg)">{icon}</div>
        <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
        <div style="color:white;font-size:13px;font-weight:800;">{title}</div>
        <div style="color:#8070B0;font-size:11px;margin-top:4px;">{sub}</div>
    </div>
    """

def section_title(text):
    st.markdown(f"""
    <div style="color:white;font-size:17px;font-weight:900;margin:20px 0 12px;
                display:flex;align-items:center;gap:8px;">{text}
        <div style="flex:1;height:1px;background:linear-gradient(90deg,#3A2F5A,transparent);margin-left:8px;"></div>
    </div>
    """, unsafe_allow_html=True)

def back_nav(current_page):
    """Show a top navigation bar with back to home + quick links"""
    st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)
    cols = st.columns([1, 1, 1, 1, 4])
    with cols[0]:
        if st.button("🏠 Home", key=f"back_home_{current_page}", use_container_width=True):
            go_to("🏠 Home")
    with cols[1]:
        if st.button("🐶 Pets", key=f"back_pets_{current_page}", use_container_width=True):
            go_to("🐶 Pet Profile")
    with cols[2]:
        if st.button("🚨 Rescue", key=f"back_rescue_{current_page}", use_container_width=True):
            go_to("🚨 Emergency Rescue")
    with cols[3]:
        if st.button("🛒 Shop", key=f"back_shop_{current_page}", use_container_width=True):
            go_to("🛒 Pet Shop")
    st.markdown("<hr style='border-color:#2A1F4A;margin:10px 0 16px'>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "map_lat" not in st.session_state:
    st.session_state.map_lat = 20.5937
if "map_lon" not in st.session_state:
    st.session_state.map_lon = 78.9629
if "reports" not in st.session_state:
    st.session_state.reports = []

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
<div style="text-align:center;padding:16px 0 20px;">
    <div style="font-size:36px;">🐾</div>
    <div style="color:white;font-size:18px;font-weight:900;letter-spacing:-0.5px;">FurEver Care</div>
    <div style="color:#6040A0;font-size:11px;margin-top:2px;">Every fur deserves forever love ✨</div>
</div>
<hr style="border-color:#2A1F4A;margin-bottom:16px;">
""", unsafe_allow_html=True)

MENU_OPTIONS = [
    "🏠 Home",
    "🐶 Pet Profile",
    "🧠 Health Assistant",
    "🍗 Food Planner",
    "💉 Vaccination",
    "🚨 Emergency Rescue",
    "🔍 Missing Pet",
    "🛒 Pet Shop"
]

# Navigation via buttons — set active_menu, sidebar follows
if "active_menu" not in st.session_state:
    st.session_state["active_menu"] = "🏠 Home"

def go_to(page):
    st.session_state["active_menu"] = page

# Sidebar selectbox — stays in sync with active_menu
selected = st.sidebar.selectbox(
    "🐾 Navigate",
    MENU_OPTIONS,
    index=MENU_OPTIONS.index(st.session_state["active_menu"])
)
# If user manually clicks sidebar, update active_menu
if selected != st.session_state["active_menu"]:
    st.session_state["active_menu"] = selected

menu = st.session_state["active_menu"]

st.sidebar.markdown("""
<hr style="border-color:#2A1F4A;margin:16px 0 12px;">
<div style="color:#5040A0;font-size:11px;text-align:center;padding-bottom:8px;">
    Made with ❤️ for pets everywhere
</div>
""", unsafe_allow_html=True)

# ================================================================
#  HOME
# ================================================================
if menu == "🏠 Home":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1A0F35,#2A1050);border-radius:20px;
                padding:32px 28px 24px;margin-bottom:24px;position:relative;overflow:hidden;
                border:1px solid #3A2F5A;">
        <div style="position:absolute;width:220px;height:220px;border-radius:50%;
                    background:#FF3CAC;opacity:0.1;top:-70px;right:-50px;"></div>
        <div style="position:absolute;width:150px;height:150px;border-radius:50%;
                    background:#7B2FFF;opacity:0.12;top:10px;right:70px;"></div>
        <div style="position:absolute;width:100px;height:100px;border-radius:50%;
                    background:#00F5FF;opacity:0.07;bottom:-20px;left:50px;"></div>
        <div style="color:#A080C0;font-size:14px;margin-bottom:4px;">Good day! 🌟</div>
        <div style="color:white;font-size:30px;font-weight:900;letter-spacing:-1px;">Welcome to FurEver Care</div>
        <div style="color:#7B60B0;font-size:14px;margin-top:6px;">Tails are wagging, time to check in! 🐾</div>
    </div>
    """, unsafe_allow_html=True)

    pets = get_pets()
    vaccinations = get_vaccinations()
    reports = get_rescue_reports()
    missing = get_missing_pets()

    stat_cards([
        ("🐾", len(pets), "My Pets"),
        ("💉", len(vaccinations), "Vaccines"),
        ("🚨", len(reports), "Rescues"),
        ("🔍", len(missing), "Missing"),
    ])

    section_title("✨ What do you need today?")

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(feature_card("🚑","Emergency Rescue","Report & get help fast","#FF3CAC"), unsafe_allow_html=True)
        if st.button("🚑 Emergency Rescue", key="home_rescue", use_container_width=True):
            go_to("🚨 Emergency Rescue")
    with c2:
        st.markdown(feature_card("🔍","Missing Pet","Find your lost baby","#FFB300"), unsafe_allow_html=True)
        if st.button("🔍 Missing Pet", key="home_missing", use_container_width=True):
            go_to("🔍 Missing Pet")
    with c3:
        st.markdown(feature_card("🛒","Pet Shop","Food · toys · treats","#00C853"), unsafe_allow_html=True)
        if st.button("🛒 Pet Shop", key="home_shop", use_container_width=True):
            go_to("🛒 Pet Shop")

    st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

    # Row 2
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown(feature_card("🩺","AI Health Check","Symptoms → diagnosis","#7B2FFF"), unsafe_allow_html=True)
        if st.button("🩺 Health Check", key="home_health", use_container_width=True):
            go_to("🧠 Health Assistant")
    with c5:
        st.markdown(feature_card("🍗","Food Planner","Smart diet plan","#00F5FF"), unsafe_allow_html=True)
        if st.button("🍗 Food Planner", key="home_food", use_container_width=True):
            go_to("🍗 Food Planner")
    with c6:
        st.markdown(feature_card("💊","Vaccination","Never miss a shot","#FF7000"), unsafe_allow_html=True)
        if st.button("💉 Vaccination", key="home_vax", use_container_width=True):
            go_to("💉 Vaccination")

    if pets:
        section_title("🐶 My Fur Babies")
        cols = st.columns(min(len(pets), 3))
        for i, pet in enumerate(pets[:3]):
            pid, name, age, breed, weight, photo, species = pet[0], pet[1], pet[2], pet[3], pet[4], pet[5] if len(pet)>5 else None, pet[6] if len(pet)>6 else 'dog'
            emoji = "🐶" if species == "dog" else "🐱" if species == "cat" else "🐾"
            with cols[i % 3]:
                if photo:
                    b64 = img_to_base64(photo)
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #3A2F5A;border-radius:16px;padding:14px;text-align:center;">
                        <img src="data:image/jpeg;base64,{b64}" style="width:70px;height:70px;border-radius:50%;object-fit:cover;border:3px solid #FF3CAC;margin-bottom:8px;">
                        <div style="color:white;font-size:15px;font-weight:800;">{name}</div>
                        <div style="color:#8060A0;font-size:12px;">{breed} · {age} yrs · {weight}kg</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #3A2F5A;border-radius:16px;padding:14px;text-align:center;">
                        <div style="font-size:42px;margin-bottom:6px;">{emoji}</div>
                        <div style="color:white;font-size:15px;font-weight:800;">{name}</div>
                        <div style="color:#8060A0;font-size:12px;">{breed} · {age} yrs · {weight}kg</div>
                    </div>
                    """, unsafe_allow_html=True)

    if reports:
        section_title("🚨 Recent Rescue Alerts")
        sev_colors = {"Low": "#00C853", "Medium": "#FFB300", "High": "#FF3CAC", "Critical": "#FF3CAC"}
        for r in reports[:3]:
            sev = r[3] if len(r) > 3 else "Unknown"
            c = sev_colors.get(sev, "#8070B0")
            st.markdown(f"""
            <div style="background:#1E1235;border:1px solid #2A1F4A;border-radius:14px;
                        padding:14px 16px;display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                <div style="width:40px;height:40px;border-radius:12px;background:{c}22;
                            display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">🐕</div>
                <div style="flex:1;">
                    <div style="color:white;font-size:13px;font-weight:700;">{r[1]}</div>
                    <div style="color:#6050A0;font-size:11px;margin-top:2px;">{r[6] if len(r)>6 else ''}</div>
                </div>
                <span style="background:{c}22;color:{c};border:1px solid {c}44;
                             font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;">{sev}</span>
            </div>
            """, unsafe_allow_html=True)

# ================================================================
#  PET PROFILE
# ================================================================
elif menu == "🐶 Pet Profile":
    hero_banner("Pet Profile", "Add and manage your fur babies 🐾", "🐶")
    back_nav("petprofile")

    tab1, tab2 = st.tabs(["➕ Add Pet", "📋 My Pets"])

    with tab1:
        with st.form("pet_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name    = st.text_input("Pet Name", placeholder="e.g. Bruno")
                breed   = st.text_input("Breed", placeholder="e.g. Labrador")
                species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
            with col2:
                age    = st.number_input("Age (years)", 0, 30, value=1)
                weight = st.number_input("Weight (kg)", 0.0, 150.0, value=5.0)
                photo  = st.file_uploader("Pet Photo 📷", type=["jpg","jpeg","png"])

            submitted = st.form_submit_button("🐾 Save Pet")

        if submitted:
            if name.strip() and breed.strip():
                photo_bytes = photo.read() if photo else None
                add_pet(name, age, breed, weight, photo_bytes, species)
                st.success(f"✅ {name} added successfully!")
                if st.button("🏠 Back to Home", key="back_home_pet"):
                    go_to("🏠 Home")
            else:
                st.warning("Please fill in name and breed.")

    with tab2:
        pets = get_pets()
        if not pets:
            st.markdown("""
            <div style="text-align:center;padding:40px;color:#6050A0;">
                <div style="font-size:48px;margin-bottom:12px;">🐾</div>
                <div style="font-size:16px;font-weight:700;">No pets yet!</div>
                <div style="font-size:13px;margin-top:4px;">Add your first fur baby above.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for pet in pets:
                pid   = pet[0]
                name  = pet[1]
                age   = pet[2]
                breed = pet[3]
                weight= pet[4]
                photo = pet[5] if len(pet) > 5 else None
                species = pet[6] if len(pet) > 6 else "dog"
                emoji = "🐶" if species=="dog" else "🐱" if species=="cat" else "🐦" if species=="bird" else "🐰" if species=="rabbit" else "🐾"

                col1, col2 = st.columns([1, 4])
                with col1:
                    if photo:
                        b64 = img_to_base64(photo)
                        st.markdown(f'<img src="data:image/jpeg;base64,{b64}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #FF3CAC;">', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="font-size:52px;text-align:center;">{emoji}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #3A2F5A;border-radius:14px;padding:14px 16px;">
                        <div style="color:white;font-size:16px;font-weight:800;">{name} {emoji}</div>
                        <div style="color:#8060A0;font-size:12px;margin-top:4px;">
                            🐾 {breed} &nbsp;|&nbsp; 🎂 {age} years &nbsp;|&nbsp; ⚖️ {weight} kg &nbsp;|&nbsp; 🏷️ {species}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🗑️ Delete", key=f"del_{pid}"):
                        delete_pet(pid)
                        st.rerun()
                st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

# ================================================================
#  HEALTH ASSISTANT
# ================================================================
elif menu == "🧠 Health Assistant":
    hero_banner("AI Health Assistant", "Describe symptoms — AI will analyze 🩺", "🧠")
    back_nav("health")

    symptoms = st.text_area("Describe your pet's symptoms",
        placeholder="e.g. My dog is vomiting, not eating since 2 days, seems lethargic...",
        height=120)

    if st.button("🩺 Analyze Symptoms"):
        if symptoms.strip():
            with st.spinner("AI is analyzing your pet's symptoms..."):
                result = analyze_pet_health(symptoms)
            st.markdown("""
            <div style="background:#1E1235;border:1px solid #7B2FFF44;border-radius:16px;padding:20px;margin-top:16px;">
                <div style="color:#FF3CAC;font-size:14px;font-weight:800;margin-bottom:10px;">🩺 AI Analysis Result</div>
            """, unsafe_allow_html=True)
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)
            st.warning("⚠️ This is AI guidance only. Always consult a licensed veterinarian for medical decisions.")
        else:
            st.warning("Please describe your pet's symptoms first.")

# ================================================================
#  FOOD PLANNER
# ================================================================
elif menu == "🍗 Food Planner":
    hero_banner("AI Food Planner", "Get a personalized diet plan for your pet 🥗", "🍗")
    back_nav("food")

    col1, col2, col3 = st.columns(3)
    with col1:
        breed = st.text_input("Breed", placeholder="e.g. Labrador")
    with col2:
        age = st.number_input("Age (years)", 0, 30, value=2)
    with col3:
        weight = st.number_input("Weight (kg)", 0.0, 150.0, value=10.0)

    if st.button("🥗 Generate Diet Plan"):
        if breed.strip():
            with st.spinner("Creating your pet's personalized food plan..."):
                result = generate_food_plan(breed, age, weight)
            st.markdown("""
            <div style="background:#1E1235;border:1px solid #00F5FF44;border-radius:16px;padding:20px;margin-top:16px;">
                <div style="color:#00F5FF;font-size:14px;font-weight:800;margin-bottom:10px;">🥗 Diet Plan</div>
            """, unsafe_allow_html=True)
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter breed.")

# ================================================================
#  VACCINATION
# ================================================================
elif menu == "💉 Vaccination":
    hero_banner("Vaccination Tracker", "Never miss your pet's important shots 💉", "💉")
    back_nav("vax")

    tab1, tab2 = st.tabs(["➕ Add Reminder", "📋 All Reminders"])

    with tab1:
        with st.form("vax_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                pet_name  = st.text_input("Pet Name", placeholder="e.g. Bruno")
                vaccine   = st.selectbox("Vaccine", [
                    "Rabies", "Distemper", "Parvovirus", "Hepatitis",
                    "Leptospirosis", "Bordetella", "FVRCP (Cats)", "FeLV (Cats)", "Other"
                ])
            with col2:
                last_date = st.date_input("Last Vaccination Date")
                next_date = st.date_input("Next Due Date")
                vet_name  = st.text_input("Vet Name (optional)")

            save = st.form_submit_button("💉 Save Reminder")

        if save:
            if pet_name.strip():
                add_vaccination(pet_name, vaccine, str(last_date), str(next_date), vet_name)
                st.success(f"✅ Reminder saved! {pet_name}'s {vaccine} due on {next_date}")
            else:
                st.warning("Please enter pet name.")

    with tab2:
        vaccs = get_vaccinations()
        if not vaccs:
            st.info("No vaccination reminders yet.")
        else:
            today = date.today()
            for v in vaccs:
                try:
                    due = date.fromisoformat(v[4])
                    days_left = (due - today).days
                    if days_left < 0:
                        badge_color = "#FF3CAC"
                        badge = "⚠️ Overdue"
                    elif days_left <= 7:
                        badge_color = "#FFB300"
                        badge = f"⏰ Due in {days_left}d"
                    else:
                        badge_color = "#00C853"
                        badge = f"✅ {days_left} days left"
                except:
                    badge_color = "#8070B0"
                    badge = "📅 Scheduled"

                st.markdown(f"""
                <div style="background:#1E1235;border:1px solid #2A1F4A;border-radius:14px;
                            padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px;">
                    <div style="font-size:28px;">💉</div>
                    <div style="flex:1;">
                        <div style="color:white;font-size:14px;font-weight:800;">{v[1]} — {v[2]}</div>
                        <div style="color:#6050A0;font-size:12px;margin-top:2px;">
                            Last: {v[3]} &nbsp;|&nbsp; Next: {v[4]}
                            {"&nbsp;|&nbsp; Vet: " + v[5] if v[5] else ""}
                        </div>
                    </div>
                    <span style="background:{badge_color}22;color:{badge_color};border:1px solid {badge_color}44;
                                 font-size:11px;padding:4px 12px;border-radius:20px;font-weight:700;white-space:nowrap;">{badge}</span>
                </div>
                """, unsafe_allow_html=True)

# ================================================================
#  EMERGENCY RESCUE
# ================================================================
elif menu == "🚨 Emergency Rescue":
    from utils.ai import generate_rescue_report
    import json

    hero_banner("Emergency Animal Rescue", "Report injured animals — get help immediately 🚑", "🚨")
    back_nav("rescue")

    # ---- FORM ----
    col1, col2 = st.columns([1, 1])
    with col1:
        image       = st.file_uploader("📷 Upload Animal Photo (optional)", type=["jpg","jpeg","png"])
        location    = st.text_input("📍 Location", placeholder="e.g. VR Mall Nagpur")
        description = st.text_area("📝 Describe the Situation",
            placeholder="e.g. Dog hit by car, bleeding from leg...", height=100)

        if st.button("🚨 Send Rescue Alert"):
            if not location.strip() or not description.strip():
                st.warning("Please fill in location and description.")
            else:
                with st.spinner("🧠 AI analyzing rescue situation..."):
                    if image:
                        result = analyze_rescue_image(image, description, location)
                    else:
                        result = analyze_rescue_case(description, location)

                # Extract severity
                severity = "Medium"
                rl = result.lower()
                if "critical" in rl: severity = "Critical"
                elif "high" in rl:   severity = "High"
                elif "low" in rl:    severity = "Low"

                # Store in session
                st.session_state["rescue_result"]   = result
                st.session_state["rescue_severity"] = severity
                st.session_state["rescue_location"] = location
                st.session_state["rescue_desc"]     = description

                # Geocode location
                lat, lon = get_coordinates(location)
                if lat is None:
                    lat, lon = 21.1458, 79.0882  # Nagpur fallback
                    st.warning("⚠️ Could not pinpoint exact location — using approximate.")

                st.session_state.reports.append({"lat": lat, "lon": lon, "description": description})
                st.session_state.map_lat = lat
                st.session_state.map_lon = lon

                # Fetch real vets from OSM
                with st.spinner("🗺️ Finding nearby vet hospitals..."):
                    try:
                        import requests as req
                        query = f"""
[out:json];
(
  node["amenity"="veterinary"](around:5000,{lat},{lon});
  node["amenity"="animal_shelter"](around:5000,{lat},{lon});
);
out body;
"""
                        osm_resp = req.get(
                            "https://overpass-api.de/api/interpreter",
                            params={"data": query}, timeout=15
                        )
                        osm_data = osm_resp.json()
                        real_vets = []
                        for el in osm_data.get("elements", []):
                            tags = el.get("tags", {})
                            real_vets.append({
                                "name": tags.get("name", "Vet Clinic"),
                                "lat": el.get("lat"),
                                "lon": el.get("lon"),
                                "phone": tags.get("phone", "N/A"),
                                "type": tags.get("amenity", "veterinary")
                            })
                        st.session_state["real_vets"] = real_vets
                    except:
                        st.session_state["real_vets"] = []

                add_rescue_report(location, description, severity, lat, lon, str(date.today()))
                st.success("✅ Rescue report submitted!")

    with col2:
        # Show AI result
        if "rescue_result" in st.session_state:
            sev = st.session_state["rescue_severity"]
            sev_color = {"Critical":"#FF3CAC","High":"#FF7000","Medium":"#FFB300","Low":"#00C853"}.get(sev,"#8070B0")

            st.markdown(f"""
            <div style="background:#1E1235;border:1px solid {sev_color}55;border-radius:16px;padding:16px;margin-bottom:12px;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
                    <div style="color:{sev_color};font-size:14px;font-weight:800;">🧠 AI Rescue Analysis</div>
                    <span style="background:{sev_color}22;color:{sev_color};border:1px solid {sev_color}44;
                                 font-size:11px;padding:3px 12px;border-radius:20px;font-weight:700;">{sev}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.write(st.session_state["rescue_result"])

            # ---- DOWNLOAD REPORT BUTTON ----
            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
            if st.button("📄 Generate & Download Report"):
                with st.spinner("Generating rescue report..."):
                    report_text = generate_rescue_report(
                        st.session_state["rescue_desc"],
                        st.session_state["rescue_location"],
                        st.session_state["rescue_result"]
                    )
                st.download_button(
                    label="⬇️ Download Report (.txt)",
                    data=report_text,
                    file_name=f"rescue_report_{date.today()}.txt",
                    mime="text/plain"
                )

    # ---- NEARBY HELP ----
    if st.session_state.reports:
        section_title("🏥 Nearby Vet Hospitals & NGOs")
        real_vets = st.session_state.get("real_vets", [])

        if real_vets:
            v_col, n_col = st.columns(2)
            with v_col:
                st.markdown('<div style="color:#00F5FF;font-size:13px;font-weight:700;margin-bottom:8px;">🏥 Real Vet Hospitals Nearby</div>', unsafe_allow_html=True)
                for v in real_vets[:5]:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #00F5FF33;border-radius:10px;padding:10px 12px;margin-bottom:6px;">
                        <div style="color:white;font-weight:700;font-size:13px;">📍 {v['name']}</div>
                        <div style="color:#6050A0;font-size:11px;">📞 {v.get('phone','N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            with n_col:
                st.markdown('<div style="color:#FF3CAC;font-size:13px;font-weight:700;margin-bottom:8px;">🤝 NGOs</div>', unsafe_allow_html=True)
                ngos = get_nearby_ngos(st.session_state.map_lat, st.session_state.map_lon)
                for n in ngos[:5]:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #FF3CAC33;border-radius:10px;padding:10px 12px;margin-bottom:6px;">
                        <div style="color:white;font-weight:700;font-size:13px;">📍 {n['name']}</div>
                        <div style="color:#6050A0;font-size:11px;">📞 {n.get('contact','N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # fallback static
            v_col, n_col = st.columns(2)
            with v_col:
                st.markdown('<div style="color:#00F5FF;font-size:13px;font-weight:700;margin-bottom:8px;">🏥 Nearby Vets</div>', unsafe_allow_html=True)
                for v in get_nearby_vets(st.session_state.map_lat, st.session_state.map_lon)[:3]:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #00F5FF33;border-radius:10px;padding:10px 12px;margin-bottom:6px;">
                        <div style="color:white;font-weight:700;">📍 {v['name']}</div>
                        <div style="color:#6050A0;font-size:11px;">📞 {v.get('contact','N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            with n_col:
                st.markdown('<div style="color:#FF3CAC;font-size:13px;font-weight:700;margin-bottom:8px;">🤝 NGOs</div>', unsafe_allow_html=True)
                for n in get_nearby_ngos(st.session_state.map_lat, st.session_state.map_lon)[:3]:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #FF3CAC33;border-radius:10px;padding:10px 12px;margin-bottom:6px;">
                        <div style="color:white;font-weight:700;">📍 {n['name']}</div>
                        <div style="color:#6050A0;font-size:11px;">📞 {n.get('contact','N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ---- MAP with location search + zoom ----
    section_title("🗺️ Live Rescue Map")

    map_search = st.text_input("🔍 Search location on map", placeholder="e.g. VR Mall Nagpur",
                                key="map_search_input")
    if st.button("📍 Find on Map", key="map_search_btn"):
        slat, slon = get_coordinates(map_search)
        if slat:
            st.session_state.map_lat = slat
            st.session_state.map_lon = slon
            st.success(f"✅ Found: {map_search}")
        else:
            st.warning("Location not found. Try being more specific.")

    # Build map
    zoom = 15 if st.session_state.reports else 12
    m = folium.Map(
        location=[st.session_state.map_lat, st.session_state.map_lon],
        zoom_start=zoom,
        tiles="CartoDB dark_matter"
    )

    # Red markers — rescue reports
    for r in st.session_state.reports:
        folium.Marker(
            [r["lat"], r["lon"]],
            popup=folium.Popup(r["description"], max_width=200),
            tooltip="🚨 Rescue Report",
            icon=folium.Icon(color="red", icon="exclamation-sign", prefix="glyphicon")
        ).add_to(m)

    # Green markers — real OSM vets
    real_vets = st.session_state.get("real_vets", [])
    for v in real_vets:
        if v.get("lat") and v.get("lon"):
            folium.Marker(
                [v["lat"], v["lon"]],
                popup=folium.Popup(f"🏥 {v['name']}<br>📞 {v.get('phone','N/A')}", max_width=200),
                tooltip=f"🏥 {v['name']}",
                icon=folium.Icon(color="green", icon="plus-sign", prefix="glyphicon")
            ).add_to(m)

    # Blue circle — search radius
    if st.session_state.reports:
        folium.Circle(
            location=[st.session_state.map_lat, st.session_state.map_lon],
            radius=5000,
            color="#00F5FF",
            fill=True,
            fill_opacity=0.05,
            popup="5km search radius"
        ).add_to(m)

    st_folium(m, width=None, height=500, use_container_width=True)

    st.markdown("""
    <div style="background:#1E1235;border:1px solid #2A1F4A;border-radius:12px;padding:12px 16px;
                margin-top:8px;font-size:12px;color:#6050A0;text-align:center;">
        🔴 Red = Rescue Report &nbsp;|&nbsp; 🟢 Green = Vet Hospital &nbsp;|&nbsp; 🔵 Blue circle = 5km radius
    </div>
    """, unsafe_allow_html=True)

# ================================================================
#  MISSING PET
# ================================================================
elif menu == "🔍 Missing Pet":
    hero_banner("Missing Pet Finder", "Report a lost pet or help find someone's fur baby 🔍", "🔍")
    back_nav("missing")

    tab1, tab2 = st.tabs(["📢 Report Missing Pet", "🗺️ All Missing Pets"])

    with tab1:
        with st.form("missing_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                pet_name = st.text_input("Pet Name", placeholder="e.g. Tommy")
                species  = st.selectbox("Species", ["dog","cat","bird","rabbit","other"])
                breed    = st.text_input("Breed", placeholder="e.g. Golden Retriever")
                color    = st.text_input("Color / Markings", placeholder="e.g. Golden with white patch on chest")
            with col2:
                location = st.text_input("Last Seen Location", placeholder="e.g. Koregaon Park, Pune")
                contact  = st.text_input("Your Contact Number", placeholder="e.g. 9876543210")
                desc     = st.text_area("Additional Description", placeholder="Collar color, any special marks...", height=80)
                photo    = st.file_uploader("Pet Photo 📷", type=["jpg","jpeg","png"])

            submit = st.form_submit_button("📢 Report Missing Pet")

        if submit:
            if pet_name.strip() and location.strip() and contact.strip():
                photo_bytes = photo.read() if photo else None
                add_missing_pet(pet_name, species, breed, color, location, contact, desc, photo_bytes, str(date.today()))
                st.success(f"✅ {pet_name} reported! Community has been alerted.")
                st.balloons()
            else:
                st.warning("Please fill in pet name, location, and contact number.")

    with tab2:
        missing = get_missing_pets()
        if not missing:
            st.markdown("""
            <div style="text-align:center;padding:40px;color:#6050A0;">
                <div style="font-size:48px;margin-bottom:12px;">🔍</div>
                <div style="font-size:16px;font-weight:700;">No missing pet reports!</div>
                <div style="font-size:13px;margin-top:4px;">Great news — all pets are home safe 🐾</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for pet in missing:
                pid      = pet[0]
                p_name   = pet[1]
                p_species= pet[2]
                p_breed  = pet[3]
                p_color  = pet[4]
                p_loc    = pet[5]
                p_contact= pet[6]
                p_desc   = pet[7]
                p_photo  = pet[8]
                p_date   = pet[9]

                col1, col2 = st.columns([1, 4])
                with col1:
                    if p_photo:
                        b64 = img_to_base64(p_photo)
                        st.markdown(f'<img src="data:image/jpeg;base64,{b64}" style="width:90px;height:90px;border-radius:14px;object-fit:cover;border:3px solid #FFB300;">', unsafe_allow_html=True)
                    else:
                        emoji = "🐶" if p_species=="dog" else "🐱" if p_species=="cat" else "🐾"
                        st.markdown(f'<div style="font-size:56px;text-align:center;">{emoji}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background:#1E1235;border:1px solid #FFB30044;border-radius:14px;padding:14px 16px;">
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                            <span style="color:white;font-size:16px;font-weight:800;">{p_name}</span>
                            <span style="background:#FFB30022;color:#FFB300;border:1px solid #FFB30044;
                                         font-size:10px;padding:2px 10px;border-radius:20px;font-weight:700;">MISSING</span>
                        </div>
                        <div style="color:#8060A0;font-size:12px;line-height:1.8;">
                            🐾 {p_breed or p_species} &nbsp;|&nbsp; 🎨 {p_color or 'N/A'}<br>
                            📍 Last seen: <b style="color:#C0A0E0">{p_loc}</b><br>
                            📞 Contact: <b style="color:#C0A0E0">{p_contact}</b><br>
                            📅 Reported: {p_date}
                            {"<br>📝 " + p_desc if p_desc else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"✅ Mark as Found", key=f"found_{pid}"):
                        mark_pet_found(pid)
                        st.success(f"🎉 {p_name} marked as found!")
                        st.rerun()
                st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)

# ================================================================
#  PET SHOP
# ================================================================
elif menu == "🛒 Pet Shop":
    hero_banner("Mini Pet Shop", "Everything your fur baby needs 🛒", "🛒")
    back_nav("shop")

    PRODUCTS = [
        {"name": "Royal Canin Adult Dog Food", "category": "Food 🍗", "price": 1299, "emoji": "🥩", "desc": "Complete nutrition for adult dogs, 3kg pack", "tag": "Bestseller"},
        {"name": "Whiskas Cat Food Tuna", "category": "Food 🍗", "price": 450, "emoji": "🐟", "desc": "Tuna flavoured wet cat food, 12 pouches", "tag": "Popular"},
        {"name": "Interactive Rope Toy", "category": "Toys 🧸", "price": 299, "emoji": "🪢", "desc": "Durable cotton rope toy for dogs", "tag": "Fun"},
        {"name": "Feather Wand Cat Toy", "category": "Toys 🧸", "price": 199, "emoji": "🪶", "desc": "Retractable feather wand for cats", "tag": "New"},
        {"name": "Neem Pet Shampoo", "category": "Grooming 🛁", "price": 349, "emoji": "🧴", "desc": "Anti-tick neem shampoo, 250ml", "tag": "Organic"},
        {"name": "Dematting Brush", "category": "Grooming 🛁", "price": 499, "emoji": "🪮", "desc": "Professional grooming brush for all breeds", "tag": "Must Have"},
        {"name": "Orthopedic Pet Bed", "category": "Accessories 🛏️", "price": 1899, "emoji": "🛏️", "desc": "Memory foam bed, medium size", "tag": "Comfort"},
        {"name": "Stainless Steel Bowl Set", "category": "Accessories 🛏️", "price": 349, "emoji": "🥣", "desc": "Food + water bowl set, easy to clean", "tag": "Durable"},
        {"name": "Puppy Vitamin Drops", "category": "Health 💊", "price": 599, "emoji": "💊", "desc": "Multi-vitamin drops for puppies under 6 months", "tag": "Vet Approved"},
        {"name": "Calming Anxiety Treats", "category": "Health 💊", "price": 799, "emoji": "🌿", "desc": "Natural chamomile calming treats, 30 pcs", "tag": "Natural"},
        {"name": "Reflective Dog Collar", "category": "Accessories 🛏️", "price": 249, "emoji": "📿", "desc": "Safety reflective collar, adjustable", "tag": "Safety"},
        {"name": "Cat Litter Premium", "category": "Accessories 🛏️", "price": 699, "emoji": "🪣", "desc": "Odour control clumping litter, 5kg", "tag": "Odour Free"},
    ]

    categories = ["All"] + list(dict.fromkeys([p["category"] for p in PRODUCTS]))
    selected_cat = st.selectbox("Filter by Category", categories)

    filtered = PRODUCTS if selected_cat == "All" else [p for p in PRODUCTS if p["category"] == selected_cat]

    tag_colors = {
        "Bestseller": "#FF3CAC", "Popular": "#7B2FFF", "Fun": "#00C853",
        "New": "#00F5FF", "Organic": "#00C853", "Must Have": "#FFB300",
        "Comfort": "#7B2FFF", "Durable": "#00F5FF", "Vet Approved": "#FF3CAC",
        "Natural": "#00C853", "Safety": "#FFB300", "Odour Free": "#00F5FF"
    }

    cols = st.columns(3)
    for i, product in enumerate(filtered):
        tc = tag_colors.get(product["tag"], "#8070B0")
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#1E1235;border:1px solid #2A1F4A;border-radius:16px;
                        padding:18px 16px;margin-bottom:12px;position:relative;overflow:hidden;">
                <div style="position:absolute;font-size:60px;opacity:0.07;bottom:-8px;right:-4px;">{product['emoji']}</div>
                <div style="font-size:36px;margin-bottom:10px;">{product['emoji']}</div>
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;">
                    <div style="color:white;font-size:13px;font-weight:800;line-height:1.3;">{product['name']}</div>
                    <span style="background:{tc}22;color:{tc};border:1px solid {tc}44;
                                 font-size:9px;padding:2px 7px;border-radius:20px;font-weight:700;white-space:nowrap;">{product['tag']}</span>
                </div>
                <div style="color:#6050A0;font-size:11px;margin-top:5px;line-height:1.4;">{product['desc']}</div>
                <div style="color:#A080C0;font-size:10px;margin-top:4px;">{product['category']}</div>
                <div style="color:#FF3CAC;font-size:18px;font-weight:900;margin-top:10px;">₹{product['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"🛒 Add to Cart", key=f"cart_{i}")

    st.markdown("""
    <div style="background:#1E1235;border:1px solid #3A2F5A;border-radius:14px;
                padding:16px;text-align:center;margin-top:8px;color:#6050A0;font-size:13px;">
        🚚 Free delivery on orders above ₹999 &nbsp;|&nbsp; 🔄 Easy 7-day returns &nbsp;|&nbsp; 💳 COD available
    </div>
    """, unsafe_allow_html=True)