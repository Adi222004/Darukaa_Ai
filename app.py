import streamlit as st
import requests

st.set_page_config(page_title="Darukaa Watershed AI", layout="wide")
st.title("💧 Darukaa.Earth Watershed Restoration Intelligence")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user1"

with st.sidebar:
    st.header("🌊 Watershed Metrics")
    st.write("Provide data for multi-metric reasoning.")

    region = st.text_input("Region", "semi-arid")
    water_ph = st.number_input("Water pH", 0.0, 14.0, 5.5)
    turbidity = st.number_input("Turbidity (NTU)", 0.0, 200.0, 35.0)
    do = st.number_input("Dissolved Oxygen (mg/L)", 0.0, 14.0, 4.0)
    upstream = st.text_input("Upstream Land Use", "agricultural")
    aquatic_species = st.number_input("Aquatic Species Richness", 0, 1000, 8)
    pollution = st.selectbox("Pollution Level", ["low", "medium", "high"], index=2)
    buffer_width = st.number_input("Riparian Buffer Width (m)", 0.0, 100.0, 5.0)
    rainfall = st.number_input("Rainfall (mm/year)", 0.0, 5000.0, 600.0)

    if st.button("Send Structured Data"):
        structured = {
            "region": region,
            "water_ph": water_ph,
            "turbidity_ntu": turbidity,
            "dissolved_oxygen_mgl": do,
            "upstream_land_use": upstream,
            "aquatic_species_richness": aquatic_species,
            "pollution_level": pollution,
            "riparian_buffer_width_m": buffer_width,
            "rainfall_mm": rainfall
        }
        response = requests.post("http://localhost:8000/chat", json={
            "user_id": st.session_state.user_id,
            "message": "Here is my watershed data.",
            "structured_data": structured
        })
        st.session_state.messages.append({"role": "assistant", "content": response.json()["response"]})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Describe your watershed..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = requests.post("http://localhost:8000/chat", json={
        "user_id": st.session_state.user_id,
        "message": prompt
    })
    answer = response.json()["response"]
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)