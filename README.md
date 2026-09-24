# simulateur-gtb-batiment
# 🏢 Jumeau Numérique Simple - Simulateur GTB / HVAC

Ce projet est un prototype de **laboratoire numérique dynamique** développé dans le cadre de ma préparation aux solutions digitales de gestion de l'énergie. Il simule le comportement thermique et aéraulique d'un bâtiment tertiaire pour illustrer les principes d'une **Gestion Technique de Bâtiment (GTB)** moderne.

## 🎯 Objectifs du Projet
* **Arbitrage Énergétique :** Optimiser le confort thermique des occupants tout en évitant les surchauffes et les consommations inutiles.
* **Qualité de l'Air Intérieur (QAI) :** Piloter la ventilation de manière intelligente en fonction du taux de confinement ($CO_2$).
* **Visualisation Data :** Offrir un tableau de bord clair, dynamique et accessible pour des profils décisionnels ou non techniques.

## 🛠️ Logique Algorithmique Implémentée
1. **Régulation Thermique (Chauffage) :** Système par hystérésis couplé à un calendrier horaire (Mode Confort à 21°C / Mode Éco à 16°C). La vanne de chauffage se module automatiquement pour atteindre la cible sans oscillations excessives.
2. **Régulation de la Ventilation (CTA) :** Ventilation modulée à la demande (*Demand-Controlled Ventilation*). La vitesse du ventilateur (de 1 à 3) s'adapte en temps réel dès que le seuil de vigilance (800 ppm) ou le seuil critique (1000 ppm) de $CO_2$ est franchi.

## 🚀 Technologies Utilisées
* **Langage :** Python 3
* **Interface Web & Data :** Streamlit
* **Environnement Cloud :** GitHub Codespaces
