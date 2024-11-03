import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Configuration de la page
st.set_page_config(page_title="Tableau de bord des ventes", page_icon=":bar_chart:", layout="wide")

# Style personnalisé pour ajuster la mise en page et améliorer l'apparence
st.markdown("""
    <style>
        div.block-container {
            margin-top: 40px;
            max-width: 95%;
        }
        .st-metric {
            text-align: center;
        }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Define a dictionary for all states in the dataset with full name, latitude, and longitude
state_info = {
    "AL": {"full_name": "Alabama", "latitude": 32.3182, "longitude": -86.9023},
    "AK": {"full_name": "Alaska", "latitude": 64.2008, "longitude": -149.4937},
    "AZ": {"full_name": "Arizona", "latitude": 34.0489, "longitude": -111.0937},
    "AR": {"full_name": "Arkansas", "latitude": 35.2010, "longitude": -91.8318},
    "CA": {"full_name": "California", "latitude": 36.7783, "longitude": -119.4179},
    "CO": {"full_name": "Colorado", "latitude": 39.5501, "longitude": -105.7821},
    "CT": {"full_name": "Connecticut", "latitude": 41.6032, "longitude": -73.0877},
    "DE": {"full_name": "Delaware", "latitude": 38.9108, "longitude": -75.5277},
    "FL": {"full_name": "Florida", "latitude": 27.9944, "longitude": -81.7603},
    "GA": {"full_name": "Georgia", "latitude": 32.1656, "longitude": -82.9001},
    "HI": {"full_name": "Hawaii", "latitude": 19.8968, "longitude": -155.5828},
    "ID": {"full_name": "Idaho", "latitude": 44.0682, "longitude": -114.7420},
    "IL": {"full_name": "Illinois", "latitude": 40.6331, "longitude": -89.3985},
    "IN": {"full_name": "Indiana", "latitude": 40.2672, "longitude": -86.1349},
    "IA": {"full_name": "Iowa", "latitude": 41.8780, "longitude": -93.0977},
    "KS": {"full_name": "Kansas", "latitude": 39.0119, "longitude": -98.4842},
    "KY": {"full_name": "Kentucky", "latitude": 37.8393, "longitude": -84.2700},
    "LA": {"full_name": "Louisiana", "latitude": 30.9843, "longitude": -91.9623},
    "ME": {"full_name": "Maine", "latitude": 45.2538, "longitude": -69.4455},
    "MD": {"full_name": "Maryland", "latitude": 39.0458, "longitude": -76.6413},
    "MA": {"full_name": "Massachusetts", "latitude": 42.4072, "longitude": -71.3824},
    "MI": {"full_name": "Michigan", "latitude": 44.3148, "longitude": -85.6024},
    "MN": {"full_name": "Minnesota", "latitude": 46.7296, "longitude": -94.6859},
    "MS": {"full_name": "Mississippi", "latitude": 32.3547, "longitude": -89.3985},
    "MO": {"full_name": "Missouri", "latitude": 37.9643, "longitude": -91.8318},
    "MT": {"full_name": "Montana", "latitude": 46.8797, "longitude": -110.3626},
    "NE": {"full_name": "Nebraska", "latitude": 41.4925, "longitude": -99.9018},
    "NV": {"full_name": "Nevada", "latitude": 38.8026, "longitude": -116.4194},
    "NH": {"full_name": "New Hampshire", "latitude": 43.1939, "longitude": -71.5724},
    "NJ": {"full_name": "New Jersey", "latitude": 40.0583, "longitude": -74.4057},
    "NM": {"full_name": "New Mexico", "latitude": 34.5199, "longitude": -105.8701},
    "NY": {"full_name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    "NC": {"full_name": "North Carolina", "latitude": 35.7596, "longitude": -79.0193},
    "ND": {"full_name": "North Dakota", "latitude": 47.5515, "longitude": -101.0020},
    "OH": {"full_name": "Ohio", "latitude": 40.4173, "longitude": -82.9071},
    "OK": {"full_name": "Oklahoma", "latitude": 35.0078, "longitude": -97.0929},
    "OR": {"full_name": "Oregon", "latitude": 43.8041, "longitude": -120.5542},
    "PA": {"full_name": "Pennsylvania", "latitude": 41.2033, "longitude": -77.1945},
    "RI": {"full_name": "Rhode Island", "latitude": 41.5801, "longitude": -71.4774},
    "SC": {"full_name": "South Carolina", "latitude": 33.8361, "longitude": -81.1637},
    "SD": {"full_name": "South Dakota", "latitude": 43.9695, "longitude": -99.9018},
    "TN": {"full_name": "Tennessee", "latitude": 35.5175, "longitude": -86.5804},
    "TX": {"full_name": "Texas", "latitude": 31.9686, "longitude": -99.9018},
    "UT": {"full_name": "Utah", "latitude": 39.3200, "longitude": -111.0937},
    "VT": {"full_name": "Vermont", "latitude": 44.5588, "longitude": -72.5778},
    "VA": {"full_name": "Virginia", "latitude": 37.4316, "longitude": -78.6569},
    "WA": {"full_name": "Washington", "latitude": 47.7511, "longitude": -120.7401},
    "WV": {"full_name": "West Virginia", "latitude": 38.5976, "longitude": -80.4549},
    "WI": {"full_name": "Wisconsin", "latitude": 43.7844, "longitude": -88.7879},
    "WY": {"full_name": "Wyoming", "latitude": 43.0759, "longitude": -107.2903},
    "DC": {"full_name": "District of Columbia", "latitude": 38.9072, "longitude": -77.0369},
}

# URL GitHub pour le fichier Superstore.csv
url_github = "https://raw.githubusercontent.com/MARAMATA/Streamlit_project/master/Superstore_filtered.csv"

# 1. Chargement du fichier de données
fichier = st.file_uploader("📁 Charger le fichier de données des ventes", type=["csv", "txt", "xlsx", "xls"])

def charger_dataframe(fichier, chemin=None, url=None):
    """Fonction pour charger le dataframe depuis un fichier, un chemin local ou une URL."""
    try:
        # Charger depuis le fichier uploadé
        if fichier:
            if fichier.name.endswith('.csv'):
                df = pd.read_csv(fichier)
            elif fichier.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(fichier)
            elif fichier.name.endswith('.txt'):
                df = pd.read_csv(fichier, delimiter="\t")

        # Charger depuis le fichier local
        elif chemin:
            df = pd.read_csv(chemin)

        # Charger depuis l'URL GitHub si `url` est fourni
        elif url:
            df = pd.read_csv(url)

        # Vérifier et essayer d'autres délimiteurs si nécessaire
        if len(df.columns) == 1:
            df = pd.read_csv(fichier or chemin or url, delimiter=';')
        if len(df.columns) == 1:
            df = pd.read_csv(fichier or chemin or url, delimiter='\t')
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None

# Charger le jeu de données
df = charger_dataframe(fichier, "Superstore_filtered.csv", url=url_github)

# Vérification du chargement des données avant de continuer
if df is not None:
    # Mettre en majuscule la première lettre de chaque colonne
    df.columns = [col.capitalize() for col in df.columns]

    # Afficher l'aperçu des données
    st.write("Aperçu des données :", df.head())

    # Vérifier la colonne 'State' pour ajouter des informations de géolocalisation
    if 'State' in df.columns:
        df["State_complet"] = df["State"].map(lambda x: state_info.get(x, {}).get("full_name", ""))
        df["Latitude"] = df["State"].map(lambda x: state_info.get(x, {}).get("latitude", None))
        df["Longitude"] = df["State"].map(lambda x: state_info.get(x, {}).get("longitude", None))
    else:
        st.error("La colonne 'State' est manquante dans le fichier de données.")

    # Nettoyage des données
    df.drop_duplicates(inplace=True)

    # Conversion de la date de commande en format datetime
    if "Order_date" in df.columns:
        df["Order_date"] = pd.to_datetime(df["Order_date"], errors='coerce')
    else:
        st.error("La colonne 'Order_date' est manquante dans le fichier de données.")
else:
    st.error("Impossible de charger les données.")

# 3. Sélection des dates en dehors de la barre latérale
st.header("Sélection de la période")
col1, col2 = st.columns(2)

with col1:
    date_debut = pd.to_datetime(st.date_input("Date de début", df["Order_date"].min()).strftime('%Y-%m-%d'))

with col2:
    date_fin = pd.to_datetime(st.date_input("Date de fin", df["Order_date"].max()).strftime('%Y-%m-%d'))

# Filtrer le dataframe en fonction de la période sélectionnée
df = df[(df["Order_date"] >= date_debut) & (df["Order_date"] <= date_fin)].copy()

# 4. Filtres interactifs dans la barre latérale
st.sidebar.header("Filtres")

# Filtre pour la région
region_selectionnee = st.sidebar.multiselect("Sélectionner la région", options=df["Region"].unique())

# Filtrer les états en fonction de la région sélectionnée
if region_selectionnee:
    df = df[df["Region"].isin(region_selectionnee)]
etats_disponibles = df["State_complet"].unique()

# Filtre pour l'état
etat_selectionne = st.sidebar.multiselect("Sélectionner l'état", options=sorted(etats_disponibles))

# Filtrer les villes en fonction de l'état sélectionné
if etat_selectionne:
    df = df[df["State_complet"].isin(etat_selectionne)]
villes_disponibles = df["City"].unique()

# Filtre pour la ville
ville_selectionnee = st.sidebar.multiselect("Sélectionner la ville", options=sorted(villes_disponibles))

# Mise à jour automatique des régions et états basés sur la sélection des villes
if ville_selectionnee:
    df_ville = df[df["City"].isin(ville_selectionnee)]
    etat_selectionne = df_ville["State_complet"].unique().tolist()
    region_selectionnee = df_ville["Region"].unique().tolist()
elif etat_selectionne and not ville_selectionnee:
    df_etat = df[df["State_complet"].isin(etat_selectionne)]
    region_selectionnee = df_etat["Region"].unique().tolist()

# Afficher les sélections pour la Région, l'État, et la Ville
st.sidebar.write("Région(s) sélectionnée(s) :", ", ".join(region_selectionnee) if region_selectionnee else "Aucune")
st.sidebar.write("État(s) sélectionné(s) :", ", ".join(etat_selectionne) if etat_selectionne else "Aucun")
st.sidebar.write("Ville(s) sélectionnée(s) :", ", ".join(ville_selectionnee) if ville_selectionnee else "Aucune")

# Filtrer le dataframe en fonction des sélections finales
df_filtre = df[
    (df["Region"].isin(region_selectionnee) if region_selectionnee else df["Region"].notna()) &
    (df["State_complet"].isin(etat_selectionne) if etat_selectionne else df["State_complet"].notna()) &
    (df["City"].isin(ville_selectionnee) if ville_selectionnee else df["City"].notna())
]

# 5. KPIs : Nombre total de ventes, clients uniques, et commandes
st.title("Tableau de bord des ventes")

if "Cust_id" in df_filtre.columns and "Order_id" in df_filtre.columns and "Total" in df_filtre.columns:
    ventes_totales = df_filtre["Total"].sum()
    clients_uniques = df_filtre["Cust_id"].nunique()
    commandes_totales = df_filtre["Order_id"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Ventes totales", f"{ventes_totales:,.2f} $")
    col2.metric("Clients uniques", clients_uniques)
    col3.metric("Commandes totales", commandes_totales)

# 6. Ventes par catégorie (Diagramme en barres)
if "Category" in df_filtre.columns:
    st.subheader("Ventes par catégorie")
    ventes_par_categorie = df_filtre.groupby("Category")["Total"].sum().reset_index()
    fig_categorie = px.bar(ventes_par_categorie, x="Category", y="Total", text="Total",
                           color="Category", template="plotly_white", title="Ventes par catégorie")
    fig_categorie.update_layout(showlegend=False, xaxis_title="Catégorie", yaxis_title="Ventes")
    st.plotly_chart(fig_categorie, use_container_width=True)

# 7. Ventes par région (Diagramme circulaire)
if "Region" in df_filtre.columns:
    st.subheader("Répartition des ventes par région")
    fig_region = px.pie(df_filtre, values="Total", names="Region", hole=0.5, template="plotly_dark",
                        title="Répartition des ventes par région")
    fig_region.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_region, use_container_width=True)

# 8. Top 10 des clients (Diagramme en barres)
if "Full_name" in df_filtre.columns:
    st.subheader("Top 10 des clients par ventes")
    top_clients = df_filtre.groupby("Full_name")["Total"].sum().nlargest(10).reset_index()
    fig_top_clients = px.bar(top_clients, x="Full_name", y="Total", text="Total",
                             color="Total", template="plotly_white", title="Top 10 des clients")
    fig_top_clients.update_layout(showlegend=False, xaxis_title="Clients", yaxis_title="Ventes")
    st.plotly_chart(fig_top_clients, use_container_width=True)

# 9. Distribution de l'âge des clients (Histogramme)
if "Age" in df_filtre.columns:
    st.subheader("Distribution de l'âge des clients")
    fig_age = px.histogram(df_filtre, x="Age", nbins=20, template="plotly_white",
                           title="Distribution de l'âge des clients")
    fig_age.update_layout(xaxis_title="Âge", yaxis_title="Nombre de clients")
    st.plotly_chart(fig_age, use_container_width=True)

# 10. Distribution par genre (Diagramme en barres)
if "Gender" in df_filtre.columns:
    st.subheader("Répartition des clients par genre")
    genre_dist = df_filtre["Gender"].value_counts().reset_index()
    genre_dist.columns = ["Genre", "Count"]
    fig_genre = px.bar(genre_dist, x="Genre", y="Count", text="Count",
                       color="Genre", template="plotly_white", title="Répartition par genre")
    fig_genre.update_layout(showlegend=False, xaxis_title="Genre", yaxis_title="Nombre de clients")
    st.plotly_chart(fig_genre, use_container_width=True)

# 11. Tendance des ventes mensuelles (Courbe)
if "Order_date" in df_filtre.columns:
    st.subheader("Tendance des ventes mensuelles")
    df_filtre["Mois_annee"] = df_filtre["Order_date"].dt.to_period("M").astype(str)
    ventes_mensuelles = df_filtre.groupby("Mois_annee")["Total"].sum().reset_index()
    fig_ventes_mensuelles = px.line(ventes_mensuelles, x="Mois_annee", y="Total",
                                    template="plotly_white", title="Tendance mensuelle des ventes")
    fig_ventes_mensuelles.update_layout(xaxis_title="Mois-Annee", yaxis_title="Ventes")
    st.plotly_chart(fig_ventes_mensuelles, use_container_width=True)

# 12. Ventes par état (Carte géographique)
if "Latitude" in df_filtre.columns and "Longitude" in df_filtre.columns:
    st.subheader("Carte des ventes par état")
    fig_map = px.scatter_geo(df_filtre, lat="Latitude", lon="Longitude", color="Total",
                             hover_name="State_complet", size="Total", template="plotly_white",
                             title="Ventes par état", projection="natural earth")
    st.plotly_chart(fig_map, use_container_width=True)

