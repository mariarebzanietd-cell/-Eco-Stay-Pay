# ====================================================================
# Eco-Stay & Pay - Version Finale avec Photos + Double Mode
# Master Data Management & BI (ESGEN)
# ====================================================================

import streamlit as st
import pandas as pd
import re
from datetime import datetime, date

st.set_page_config(page_title="Eco-Stay & Pay", page_icon="🌿", layout="wide")

# --- CSS PROFESSIONNEL ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%);
        padding: 30px 40px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(27, 67, 50, 0.3);
    }
    .header-title {
        color: #ffffff !important;
        font-family: Georgia, serif;
        font-weight: 800;
        margin: 0;
        font-size: 36px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    .header-subtitle {
        color: #d8f3dc;
        font-size: 14px;
        margin-top: 8px;
        font-style: italic;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 3px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #666;
        font-weight: 600;
        font-size: 15px;
        padding: 14px 24px;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #1B4332;
        background: rgba(27, 67, 50, 0.12);
        border-bottom: 4px solid #1B4332;
    }
    .stButton > button {
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #1B4332 !important;
        box-shadow: 0 0 0 3px rgba(27, 67, 50, 0.1) !important;
    }
    .stDateInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e63946, #c1121f) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(230, 57, 70, 0.4) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c1121f, #9d0208) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(230, 57, 70, 0.6) !important;
    }
    h2, h3 {
        color: #1B4332 !important;
        font-family: Georgia, serif !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'hotels' not in st.session_state:
    st.session_state['hotels'] = [
        {"name": "Hôtel Azur", "city": "Nice", "lat": 43.7102, "lon": 7.2620, "price": 189, "type": "Hôtel", "image": "https://images.pexels.com/photos/258154/pexels-photo-258154.jpeg?auto=compress&cs=tinysrgb&w=800"},
        {"name": "Maison Lumière", "city": "Paris", "lat": 48.8566, "lon": 2.3522, "price": 139, "type": "Appartement", "image": "https://images.pexels.com/photos/14426182/pexels-photo-14426182.jpeg"},
        {"name": "Le Grand Rivage", "city": "Biarritz", "lat": 43.4832, "lon": -1.5586, "price": 229, "type": "Villa", "image": "https://images.pexels.com/photos/20007359/pexels-photo-20007359.jpeg"},
        {"name": "Eco Oasis Resort", "city": "Tipaza", "lat": 36.5912, "lon": 2.4431, "price": 120, "type": "Maison d'hôte", "image": "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=800"},
        {"name": "Villa Méditerranée", "city": "Alger", "lat": 36.7525, "lon": 3.0420, "price": 250, "type": "Villa", "image": "https://images.pexels.com/photos/1029599/pexels-photo-1029599.jpeg?auto=compress&cs=tinysrgb&w=800"},
        {"name": "Maison du Lac", "city": "Constantine", "lat": 36.3650, "lon": 6.6147, "price": 95, "type": "Maison d'hôte", "image": "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg?auto=compress&cs=tinysrgb&w=800"},
    ]

if 'reservations' not in st.session_state:
    st.session_state['reservations'] = [
        {'id': 1, 'hotel': 'Maison Lumière (Paris)', 'nom': 'Alice Martin', 'email': 'alice@mail.com', 'telephone': '0612345678', 'chambre': 'Chambre Classique', 'personnes': 2, 'montant': 139.0, 'arrivee': '2026-10-15', 'depart': '2026-10-18', 'statut': 'Validé', 'timestamp': '2026-10-01 09:00'},
        {'id': 2, 'hotel': 'Hôtel Azur (Nice)', 'nom': 'Karim Benali', 'email': 'karim@mail.com', 'telephone': '0698765432', 'chambre': 'Chambre Jardin', 'personnes': 4, 'montant': 756.0, 'arrivee': '2026-10-20', 'depart': '2026-10-24', 'statut': 'Validé', 'timestamp': '2026-10-01 10:00'},
        {'id': 3, 'hotel': 'Le Grand Rivage (Biarritz)', 'nom': 'Sarah Connor', 'email': 'sarah@mail.com', 'telephone': '0611223344', 'chambre': 'Chambre Océan', 'personnes': -1, 'montant': 687.0, 'arrivee': '2026-10-22', 'depart': '2026-10-20', 'statut': 'Anomalie', 'timestamp': '2026-10-01 11:00'},
        {'id': 4, 'hotel': 'Maison Lumière (Paris)', 'nom': None, 'email': 'inconnu', 'telephone': '', 'chambre': 'Chambre Classique', 'personnes': 2, 'montant': 278.0, 'arrivee': '2026-10-25', 'depart': '2026-10-28', 'statut': 'Anomalie', 'timestamp': '2026-10-02 08:00'},
    ]

if 'mode_strict' not in st.session_state:
    st.session_state['mode_strict'] = True

# --- EN-TÊTE ---
st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🌿 Eco-Stay & Pay</h1>
        <p class="header-subtitle">Plateforme de Réservation Hôtelière & Gouvernance des Données</p>
    </div>
""", unsafe_allow_html=True)

# Boutons S'inscrire / Connexion
col_btn_insc, col_btn_conn = st.columns(2)
with col_btn_insc:
    if st.button("✨ S'inscrire", key="btn_insc", type="primary"):
        st.session_state['show_modal'] = 'inscription'
with col_btn_conn:
    if st.button("🔐 Connexion", key="btn_conn"):
        st.session_state['show_modal'] = 'connexion'

if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = None

if st.session_state['show_modal'] == 'inscription':
    @st.dialog("✨ S'inscrire")
    def modal_inscription():
        with st.form("form_inscription"):
            st.markdown("### 📝 Créer un compte")
            nom = st.text_input("Nom complet", placeholder="Ex: Maria Rebzani")
            email = st.text_input("Adresse e-mail", placeholder="Ex: maria@mail.com")
            tel = st.text_input("Téléphone", placeholder="Ex: 0612345678")
            mdp = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Créer mon compte", type="primary")
            if submit:
                st.success(f"✅ Bienvenue {nom} !")
                st.session_state['show_modal'] = None
                st.rerun()
    modal_inscription()

if st.session_state['show_modal'] == 'connexion':
    @st.dialog("🔐 Connexion")
    def modal_connexion():
        with st.form("form_connexion"):
            st.markdown("### 🔐 Se connecter")
            email = st.text_input("Adresse e-mail", placeholder="Votre e-mail")
            mdp = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", type="primary")
            if submit:
                st.success("✅ Connexion réussie !")
                st.session_state['show_modal'] = None
                st.rerun()
    modal_connexion()

# --- SIDEBAR ---
st.sidebar.markdown("## 🔗 Lien du Site")
st.sidebar.info("**URL :** `http://localhost:8508/`")

import qrcode
from PIL import Image
import io

qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data("http://localhost:8508/")
qr.make(fit=True)
img = qr.make_image(fill_color="#1B4332", back_color="white")
buf = io.BytesIO()
img.save(buf, format="PNG")
buf.seek(0)
st.sidebar.image(buf, caption="Scannez pour accéder au site", width=200)

st.sidebar.markdown("---")
st.sidebar.markdown("## ⚙️ Mode de Fonctionnement")
mode_toggle = st.sidebar.toggle("🔒 Mode Strict", value=st.session_state['mode_strict'])
st.session_state['mode_strict'] = mode_toggle

if mode_toggle:
    st.sidebar.success("✅ **Mode STRICT** activé\n\nLes erreurs sont bloquées à la source.")
else:
    st.sidebar.warning("⚠️ **MODE SIMULATION** activé\n\nLes anomalies sont enregistrées et détectées.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 8 Dimensions")
st.sidebar.markdown("""1. **Completeness** : Champs vides
2. **Accuracy** : Valeurs aberrantes
3. **Uniqueness** : Doublons
4. **Consistency** : Dates logiques
5. **Validity** : Format email
6. **Timeliness** : Fraîcheur
7. **Integrity** : Référentiel
8. **Reliability** : Score global""")

# --- FONCTIONS D'AUDIT ---
def calculer_metriques(df):
    if len(df) == 0:
        return {}
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    completude = {}
    for champ in ['nom', 'email', 'telephone']:
        completude[champ] = int(df[champ].isna().sum() + (df[champ] == "").sum())
    
    accuracy = int((df['personnes'] <= 0).sum() + (df['montant'] < 0).sum())
    uniqueness = int(df.duplicated(subset=['id']).sum())
    
    consistency = 0
    for _, row in df.iterrows():
        try:
            if row['arrivee'] >= row['depart']:
                consistency += 1
        except:
            consistency += 1
    
    validity = int((~df['email'].apply(lambda x: bool(re.match(pattern, str(x))) if pd.notna(x) else False)).sum())
    
    maintenant = datetime.now()
    fresh = 0
    for _, row in df.iterrows():
        try:
            ts = datetime.strptime(str(row['timestamp']), '%Y-%m-%d %H:%M')
            if (maintenant - ts).days <= 30:
                fresh += 1
        except:
            pass
    
    integrity_ok = df['id'].notna().all()
    
    df_temp = df.copy()
    df_temp['erreurs'] = 0
    for champ in ['nom', 'email', 'telephone']:
        df_temp['erreurs'] += (df_temp[champ].isna() | (df_temp[champ] == "")).astype(int)
    df_temp['erreurs'] += (df_temp['personnes'] <= 0).astype(int)
    df_temp['erreurs'] += (df_temp['montant'] < 0).astype(int)
    for idx, row in df_temp.iterrows():
        try:
            if row['arrivee'] >= row['depart']:
                df_temp.at[idx, 'erreurs'] += 1
        except:
            df_temp.at[idx, 'erreurs'] += 1
    df_temp['erreurs'] += (~df_temp['email'].apply(lambda x: bool(re.match(pattern, str(x))) if pd.notna(x) else False)).astype(int)
    
    lignes_ok = (df_temp['erreurs'] == 0).sum()
    reliability = round((lignes_ok / len(df_temp)) * 100, 1)
    
    return {'completude': completude, 'accuracy': accuracy, 'uniqueness': uniqueness, 'consistency': consistency, 'validity': validity, 'timeliness': fresh, 'integrity_ok': integrity_ok, 'reliability': reliability}

# --- ONGLETS ---
tab_site, tab_map, tab_audit, tab_nettoyage = st.tabs(["🏨 Guide des Hôtels", "🗺️ Carte", "📊 Audit & Dashboard", "🧹 Nettoyage"])

with tab_site:
    st.markdown("""
        <div style="background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg?auto=compress&cs=tinysrgb&w=1600'); background-size: cover; background-position: center; padding: 80px 60px; border-radius: 16px; margin-bottom: 30px;">
            <div style="background: rgba(255,255,255,0.95); border-radius: 20px; padding: 50px; max-width: 700px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                <p style="color: #2e7d32; font-size: 0.85rem; font-weight: 600; margin-bottom: 15px;">🌿 Expérience Luxueuse & Durable</p>
                <h1 style="color: #1a1a2e; font-size: 2.8rem; font-weight: 800; margin-bottom: 15px;">The Best Eco-Luxury Hotels.</h1>
                <p style="color: #555; font-size: 1.1rem;">Réservez votre séjour neutre en carbone dans les plus beaux resorts côtiers.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    villes = ["Toutes"] + list(set([h['city'] for h in st.session_state['hotels']]))
    col_ville, col_btn = st.columns([3, 1])
    with col_ville:
        ville_choisie = st.selectbox("📍 Villes populaires", villes)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔎 Rechercher", type="primary"):
            st.session_state['ville_recherchee'] = ville_choisie

    st.markdown("### 🌟 Nos Plus Belles Adresses")
    hotels_filtres = st.session_state['hotels']
    ville_active = st.session_state.get('ville_recherchee', ville_choisie)
    if ville_active != "Toutes":
        hotels_filtres = [h for h in hotels_filtres if h['city'] == ville_active]
    
    cols = st.columns(3)
    for i, hotel in enumerate(hotels_filtres):
        with cols[i % 3]:
            st.markdown(f"""<div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <img src="{hotel['image']}" style="width: 100%; height: 180px; object-fit: cover;">
                <div style="padding: 20px;"><h4 style="margin: 0 0 5px 0;">{hotel['name']}</h4>
                <p style="margin: 0 0 5px 0; color: #666; font-size: 0.9rem;">📍 {hotel['city']} | 🌿 {hotel['type']}</p>
                <p style="margin: 0 0 15px 0; color: #003580; font-weight: 700;">À partir de {hotel['price']} € / nuit</p></div></div>""", unsafe_allow_html=True)
            if st.button(f"🛏️ Réserver", key=f"hotel_{i}"):
                st.session_state['hotel_selectionne'] = hotel
                st.rerun()

    if 'hotel_selectionne' in st.session_state and st.session_state['hotel_selectionne']:
        hotel_sel = st.session_state['hotel_selectionne']
        @st.dialog(f"🛏️ Réserver : {hotel_sel['name']}")
        def modal_reservation():
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1B4332, #2D6A4F); padding: 15px 20px; border-radius: 10px; margin-bottom: 20px; color: white;">
                <h3 style="margin: 0; color: white;">{hotel_sel['name']}</h3>
                <p style="margin: 5px 0 0 0; color: #b7e4c7; font-size: 14px;">📍 {hotel_sel['city']} | 💰 {hotel_sel['price']} € / nuit</p></div>""", unsafe_allow_html=True)
            with st.form("form_modal"):
                st.markdown("#### 👤 Informations Client")
                col1, col2 = st.columns(2)
                with col1:
                    nom = st.text_input("Nom complet *", placeholder="Ex: Maria Rebzani")
                    email = st.text_input("Adresse e-mail *", placeholder="Ex: maria@mail.com")
                with col2:
                    telephone = st.text_input("Téléphone *", placeholder="Ex: 0612345678")
                st.markdown("#### 🛏️ Chambre & Séjour")
                col3, col4 = st.columns(2)
                with col3:
                    chambre = st.selectbox("Type de chambre *", ["Chambre Standard", "Chambre Supérieure", "Suite"])
                    personnes = st.number_input("Nombre de personnes *", min_value=1, value=2)
                with col4:
                    arrivee = st.date_input("Date d'arrivée *", date(2026, 11, 1))
                    depart = st.date_input("Date de départ *", date(2026, 11, 3))
                st.markdown("#### 💳 Paiement")
                col5, col6 = st.columns(2)
                with col5:
                    paiement = st.selectbox("Mode de paiement *", ["Carte Bancaire", "Espèces", "Virement", "PayPal"])
                with col6:
                    montant = st.number_input("Montant (€) *", min_value=0.0, value=150.0)
                st.markdown("---")
                submit = st.form_submit_button("✅ Enregistrer la réservation", type="primary")
            if submit:
                erreurs = []
                if st.session_state['mode_strict']:
                    if not nom or nom.strip() == "": erreurs.append("❌ **Completeness** : Le nom est obligatoire.")
                    if not email or "@" not in email: erreurs.append("❌ **Validity** : E-mail invalide.")
                    if not telephone or telephone.strip() == "": erreurs.append("❌ **Completeness** : Téléphone obligatoire.")
                    if personnes <= 0: erreurs.append("❌ **Accuracy** : Personnes > 0.")
                    if arrivee >= depart: erreurs.append("❌ **Consistency** : Départ après arrivée.")
                    if erreurs:
                        st.error("🚫 **Réservation bloquée** :")
                        for err in erreurs: st.markdown(err)
                    else:
                        st.session_state['reservations'].append({'id': len(st.session_state['reservations'])+1, 'hotel': hotel_sel['name'], 'nom': nom, 'email': email, 'telephone': telephone, 'chambre': chambre, 'personnes': personnes, 'montant': montant, 'arrivee': str(arrivee), 'depart': str(depart), 'statut': 'Validé', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')})
                        st.success("✅ Réservation enregistrée !")
                        st.session_state['hotel_selectionne'] = None
                        st.rerun()
                else:
                    statut = 'Validé'
                    if not nom: statut = 'Anomalie'
                    if "@" not in str(email): statut = 'Anomalie'
                    if not telephone: statut = 'Anomalie'
                    if personnes <= 0: statut = 'Anomalie'
                    if arrivee >= depart: statut = 'Anomalie'
                    st.session_state['reservations'].append({'id': len(st.session_state['reservations'])+1, 'hotel': hotel_sel['name'], 'nom': nom if nom else None, 'email': email, 'telephone': telephone, 'chambre': chambre, 'personnes': personnes, 'montant': montant, 'arrivee': str(arrivee), 'depart': str(depart), 'statut': statut, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')})
                    if statut == 'Anomalie': st.warning("⚠️ Réservation avec anomalies.")
                    else: st.success("✅ Réservation enregistrée !")
                    st.session_state['hotel_selectionne'] = None
                    st.rerun()
        modal_reservation()

    st.markdown("---")
    st.markdown("### 📋 Mes Réservations")
    if st.button("👁️ Voir les réservations", key="voir_reservations"):
        @st.dialog("📋 Liste des Réservations")
        def modal_reservations():
            df = pd.DataFrame(st.session_state['reservations'])
            st.dataframe(df)
        modal_reservations()

with tab_map:
    st.markdown("## 🗺️ Localisation des Hôtels")
    import folium
    from streamlit_folium import st_folium
    m = folium.Map(location=[40, 5], zoom_start=5)
    type_colors = {"Hôtel": "blue", "Villa": "green", "Appartement": "orange", "Maison d'hôte": "purple"}
    for hotel in st.session_state['hotels']:
        folium.Marker(location=[hotel['lat'], hotel['lon']], popup=folium.Popup(f"<b>{hotel['name']}</b><br>📍 {hotel['city']}<br>💰 {hotel['price']}€/nuit", max_width=200), tooltip=hotel['name'], icon=folium.Icon(color=type_colors.get(hotel['type'], "blue"), icon="home", prefix="fa")).add_to(m)
    st_folium(m, width=1200, height=500)

with tab_audit:
    df = pd.DataFrame(st.session_state['reservations'])
    st.markdown("""<h2 style='color: #1B4332; font-weight: 800; font-family: Georgia, serif;'>📊 Audit des 8 Dimensions de Qualité</h2><p style='color: #666;'>Surveillance en temps réel de la qualité des données.</p>""", unsafe_allow_html=True)
    if len(df) == 0:
        st.info("Aucune donnée à auditer.")
    else:
        metriques = calculer_metriques(df)
        st.progress(metriques['reliability']/100, text=f"Indice de Confiance Global : {metriques['reliability']}%")
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("1. Completeness", f"{sum(metriques['completude'].values())} vide(s)", delta="Champs vides" if sum(metriques['completude'].values()) > 0 else "Parfait", delta_color="inverse")
        with col2: st.metric("2. Accuracy", f"{metriques['accuracy']} err.", delta="Valeurs aberrantes" if metriques['accuracy'] > 0 else "Parfait", delta_color="inverse")
        with col3: st.metric("3. Uniqueness", f"{metriques['uniqueness']} doublon(s)", delta="Doublons" if metriques['uniqueness'] > 0 else "Parfait", delta_color="inverse")
        with col4: st.metric("4. Consistency", f"{metriques['consistency']} err.", delta="Dates incohérentes" if metriques['consistency'] > 0 else "Parfait", delta_color="inverse")
        col5, col6, col7, col8 = st.columns(4)
        with col5: st.metric("5. Validity", f"{metriques['validity']} err.", delta="Format invalide" if metriques['validity'] > 0 else "Parfait", delta_color="inverse")
        with col6: st.metric("6. Timeliness", f"{metriques['timeliness']} récente(s)", delta="Frais", delta_color="normal")
        with col7: st.metric("7. Integrity", "OK ✓" if metriques['integrity_ok'] else "Erreur")
        with col8: st.metric("8. Reliability", f"{metriques['reliability']}%", delta="Indice de confiance", delta_color="normal" if metriques['reliability'] >= 80 else "inverse")
        st.markdown("---")
        st.markdown("### 📋 Données brutes")
        st.dataframe(df)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger (CSV)", data=csv_data, file_name='rapport_audit.csv', mime='text/csv')

with tab_nettoyage:
    st.markdown("### 🧹 Nettoyage des Données")
    df = pd.DataFrame(st.session_state['reservations'])
    st.dataframe(df)
    if st.button("🚀 Lancer le nettoyage"):
        df_clean = df.drop_duplicates(subset=['id'], keep='first')
        df_clean = df_clean[df_clean['nom'].notna()].copy()
        df_clean['personnes'] = df_clean['personnes'].apply(lambda x: 1 if x <= 0 else x)
        df_clean['montant'] = df_clean['montant'].apply(lambda x: 0.0 if x < 0 else x)
        def corriger(row):
            try:
                da = datetime.strptime(str(row['arrivee']), '%Y-%m-%d')
                dd = datetime.strptime(str(row['depart']), '%Y-%m-%d')
                if dd <= da: row['depart'] = str(da + pd.Timedelta(days=1)); row['statut'] = 'Corrigé'
                else: row['statut'] = 'Validé'
            except: pass
            return row
        df_clean = df_clean.apply(corriger, axis=1)
        st.session_state['reservations'] = df_clean.to_dict('records')
        st.success(f"✅ Nettoyage terminé !")
        st.dataframe(df_clean)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Eco-Stay & Pay © 2026 — Master Data Management & BI (ESGEN)</p>", unsafe_allow_html=True)
