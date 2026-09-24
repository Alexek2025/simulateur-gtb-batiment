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

# --- NOUVELLES VARIABLES DE PERFORMANCE (KPI) ---
if "kwh_consumed" not in st.session_state:
    st.session_state.kwh_consumed = 0.0
if "euros_saved" not in st.session_state:
    st.session_state.euros_saved = 0.0

# --- LOGIQUE ALGORITHMIQUE DE L'AUTOMATE ---
target_temp = target_occupied if is_occupied else target_unoccupied

# 1. Régulation Chauffage (Hystérésis)
if st.session_state.temp < (target_temp - hysteresis):
    st.session_state.valve = min(100.0, st.session_state.valve + 20.0) 
elif st.session_state.temp > (target_temp + hysteresis):
    st.session_state.valve = max(0.0, st.session_state.valve - 25.0)  

# 2. Régulation Ventilation (CTA via niveau CO2)
if not is_occupied:
    st.session_state.cta = 0
else:
    if st.session_state.co2 > 1000:
        st.session_state.cta = 3  
    elif st.session_state.co2 > 800:
        st.session_state.cta = 2  
    else:
        st.session_state.cta = 1  

# --- AFFICHAGE DE LA SUPERVISION (IHM) ---

# Métriques de fonctionnement
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Température Actuelle", f"{st.session_state.temp:.1f} °C", f"Consigne: {target_temp}°C", delta_color="off")
col2.metric("💨 Qualité de l'air (CO2)", f"{st.session_state.co2} ppm", "Seuil max: 1000 ppm", delta_color="inverse")
col3.metric("🔥 Vanne de Chauffage", f"{st.session_state.valve} %")
col4.metric("🌀 Vitesse CTA / Ventilo", f"Vitesse {st.session_state.cta}")

# Graphique d'historique
st.session_state.history_temp.append(st.session_state.temp)
if len(st.session_state.history_temp) > 20: 
    st.session_state.history_temp.pop(0)

st.subheader("📈 Évolution de la température en temps réel")
st.line_chart(st.session_state.history_temp)

# --- SECTION DES KPI ÉNERGÉTIQUES ET FINANCIERS ---
st.write("---")
st.subheader("📊 Indicateurs de Performance Énergétique (KPI)")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

# Calcul de la puissance instantanée estimée (ex: une chaudière de 50 kW max)
current_power_kw = (st.session_state.valve / 100.0) * 50.0
col_kpi1.metric("⚡ Appel de Puissance Chauffage", f"{current_power_kw:.1f} kW")
col_kpi2.metric("🔋 Énergie Cumulée Consommée", f"{st.session_state.kwh_consumed:.2f} kWh")
col_kpi3.metric("💶 Économies Financières Estimées", f"{st.session_state.euros_saved:.2f} €", "Grâce au mode Éco/Hystérésis", delta_color="normal")

# --- SIMULATION DE LA PHYSIQUE DU BÂTIMENT ---
st.write("---")
if st.button("🔄 Injecter 1 minute de temps (Simuler une étape)"):
    # Physique thermique
    st.session_state.temp += (st.session_state.valve * 0.008) - 0.15
    
    # Physique CO2
    if is_occupied:
        st.session_state.co2 += random.choice([-20, 50, 120])
    else:
        st.session_state.co2 += random.choice([-100, -50, 10])
    st.session_state.co2 = max(400, min(st.session_state.co2, 1500))
    
    # --- CALCULS ENERGIE (1 minute = 1/60ème d'heure) ---
    # Énergie consommée pendant cette minute
    st.session_state.kwh_consumed += current_power_kw * (1 / 60)
    
    # Simulation des économies : si on est en mode éco (la nuit) ou si la vanne est coupée à 0%, 
    # on économise par rapport à un bâtiment "à l'ancienne" qui chaufferait à 100% tout le temps
    if not is_occupied or st.session_state.valve == 0:
        # On estime qu'on économise l'équivalent de 35 kW de chauffage non consommé, valorisé à 0.15€ le kWh
        saved_this_minute = 35.0 * (1 / 60)
        st.session_state.euros_saved += saved_this_minute * 0.15
    
    st.rerun()
