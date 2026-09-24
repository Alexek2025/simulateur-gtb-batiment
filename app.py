import streamlit as st
import time
import random

# Configuration de la page Streamlit
st.set_page_config(page_title="Simulateur GTB / HVAC", layout="wide")
st.title("🏢 Tableau de Bord - Simulateur GTB du Bâtiment")

# --- PARAMÈTRES (Barre latérale) ---
st.sidebar.header("⚙️ Configuration des Consignes")
target_occupied = st.sidebar.slider("Consigne Mode Occupé (°C)", 18.0, 25.0, 21.0, 0.5)
target_unoccupied = st.sidebar.slider("Consigne Mode Éco (°C)", 14.0, 19.0, 16.0, 0.5)
hysteresis = 0.5

st.sidebar.header("🗓️ État de l'Immeuble")
occupancy_mode = st.sidebar.selectbox("Planning Horaire", ["Occupé (Journée)", "Inoccupé (Nuit/WE)"])
is_occupied = occupancy_mode == "Occupé (Journée)"

# --- INITIALISATION DES VARIABLES GLOBALES (Session State) ---
if "temp" not in st.session_state:
    st.session_state.temp = 18.5
if "co2" not in st.session_state:
    st.session_state.co2 = 600
if "valve" not in st.session_state:
    st.session_state.valve = 0.0
if "cta" not in st.session_state:
    st.session_state.cta = 0
if "history_temp" not in st.session_state:
    st.session_state.history_temp = []

# --- LOGIQUE ALGORITHMIQUE DE L'AUTOMATE ---
target_temp = target_occupied if is_occupied else target_unoccupied

# 1. Régulation Chauffage (Hystérésis)
if st.session_state.temp < (target_temp - hysteresis):
    st.session_state.valve = min(100.0, st.session_state.valve + 20.0) # On ouvre la vanne
elif st.session_state.temp > (target_temp + hysteresis):
    st.session_state.valve = max(0.0, st.session_state.valve - 25.0)  # On ferme la vanne

# 2. Régulation Ventilation (CTA via niveau CO2)
if not is_occupied:
    st.session_state.cta = 0
else:
    if st.session_state.co2 > 1000:
        st.session_state.cta = 3  # Vitesse Max
    elif st.session_state.co2 > 800:
        st.session_state.cta = 2  # Vitesse Moyenne
    else:
        st.session_state.cta = 1  # Vitesse Nominale

# --- AFFICHAGE DE LA SUPERVISION (IHM) ---

# Métriques principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Température Actuelle", f"{st.session_state.temp:.1f} °C", f"Consigne: {target_temp}°C", delta_color="off")
col2.metric("💨 Qualité de l'air (CO2)", f"{st.session_state.co2} ppm", "Seuil max: 1000 ppm", delta_color="inverse")
col3.metric("🔥 Vanne de Chauffage", f"{st.session_state.valve} %")
col4.metric("🌀 Vitesse CTA / Ventilo", f"Vitesse {st.session_state.cta}")

# Graphique d'historique
st.session_state.history_temp.append(st.session_state.temp)
if len(st.session_state.history_temp) > 20: # Limiter à 20 points
    st.session_state.history_temp.pop(0)

st.subheader("📈 Évolution de la température en temps réel")
st.line_chart(st.session_state.history_temp)

# --- SIMULATION DE LA PHYSIQUE DU BÂTIMENT ---
st.write("---")
if st.button("🔄 Injecter 1 minute de temps (Simuler une étape)"):
    # Pertes thermiques naturelles du bâtiment (-0.15°C) vs apport de la vanne
    st.session_state.temp += (st.session_state.valve * 0.008) - 0.15
    
    # Évolution aléatoire du CO2 selon la présence humaine
    if is_occupied:
        st.session_state.co2 += random.choice([-20, 50, 120])
    else:
        st.session_state.co2 += random.choice([-100, -50, 10])
    
    # Limites physiques
    st.session_state.co2 = max(400, min(st.session_state.co2, 1500))
    
    # Forcer le rafraîchissement
    st.rerun()
