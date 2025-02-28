import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import base64

# ------------------------- UI PRINCIPALE -------------------------
st.set_page_config(page_title="MY DATA APP", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: black;'>MY DATA APP 🚀</h1>
""", unsafe_allow_html=True)

st.markdown("""
Cette application permet de :
- 📌 Scraper des données sur plusieurs pages
- 📥 Télécharger les données collectées
- 📝 Remplir un formulaire d’évaluation

*Sources des données :*  
🔗 [Expat-Dakar](https://www.expat-dakar.com/)  
🔗 [CoinAfrique](https://sn.coinafrique.com/)
""")

st.markdown("---")

# ------------------------- FONCTION DE SCRAPING VETEMENTS ENFANTS (Code1) -------------------------
def scrape_vetements_enfants(pages=1):
    all_data = []
    for page in range(1, pages + 1):
        url = f'https://sn.coinafrique.com/categorie/vetements-enfants?page={page}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        conteneurs = soup.find_all('div', class_="col s6 m4 l3")
        
        for conteneur in conteneurs:
            try:
                type_habits = conteneur.find('p', class_="ad__card-description").text.strip()
                prix_fcfa = conteneur.find('p', class_="ad__card-price").text.replace('CFA', '').strip()
                adresse = conteneur.find('p', class_="ad__card-location").text.replace('location_on', '').strip()
                image_lien = conteneur.find('img', class_="ad__card-img")['src']
                
                all_data.append([type_habits, prix_fcfa, adresse, image_lien])
            except AttributeError:
                pass
    
    df = pd.DataFrame(all_data, columns=["Type de vêtement", "Prix (FCFA)", "Localisation", "Image"])
    return df

# ------------------------- FONCTION DE SCRAPING CHAUSSURES ENFANTS (Code2) -------------------------
def scrape_chaussures_enfants(pages=1):
    all_data = []
    for page in range(1, pages + 1):
        url = f'https://sn.coinafrique.com/categorie/chaussures-enfants?page={page}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        conteneurs = soup.find_all('div', class_="col s6 m4 l3")
        
        for conteneur in conteneurs:
            try:
                type_chaussure = conteneur.find('p', class_="ad__card-description").text.strip()
                prix_fcfa = conteneur.find('p', class_="ad__card-price").text.replace('CFA', '').strip()
                adresse = conteneur.find('p', class_="ad__card-location").text.replace('location_on', '').strip()
                img = conteneur.find('img', class_="ad__card-img")['src']
                
                all_data.append([type_chaussure, prix_fcfa, adresse, img])
            except AttributeError:
                pass
    
    df = pd.DataFrame(all_data, columns=["Type de chaussure", "Prix (FCFA)", "Localisation", "Image"])
    return df

# ------------------------- INTERFACE DE SCRAPING -------------------------
st.subheader("🔍 Scraper des données")
option = st.selectbox("Sélectionner la catégorie à scraper", ["Vêtements Enfants - CoinAfrique", "Chaussures Enfants - CoinAfrique"])
n_pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=500, value=1)

if st.button("Lancer le scraping"):
    if option == "Vêtements Enfants - CoinAfrique":
        data = scrape_vetements_enfants(n_pages)
    else:
        data = scrape_chaussures_enfants(n_pages)

    st.write(data)
    
    # Sauvegarde des données
    csv_file = "scraped_data.csv"
    data.to_csv(csv_file, index=False)
    st.success("Scraping terminé avec succès !")

    # Ajout du bouton de téléchargement
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file}">📥 Télécharger les données</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("---")

# ------------------------- FORMULAIRES D'ÉVALUATION -------------------------
st.subheader("📝 Évaluer l'application")
st.text("Vos commentaires sont précieux !")

# Formulaires d'évaluation via Kobo et Google Forms
st.markdown("""
- Formulaire d’évaluation **Kobo**: [Formulaire Kobo](https://ee.kobotoolbox.org/x/vvtCsbTS)
- Formulaire d’évaluation **Google Forms**: [Formulaire Google](https://docs.google.com/forms/d/e/1FAIpQLSfAhRhgY_NdD-whGncXVRIow9YHAZVIJhRL39v8GYuG2M7L3Q/viewform?usp=dialog)
""")

# ------------------------- STYLE -------------------------
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)
