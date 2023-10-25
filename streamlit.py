# Nom ......... : streamlit.py
# Rôle ........ : Petite application streamlit (édition EXIF, affichage de POI(s))
# Auteur ...... : Rosalie Duteuil
# Version ..... : V1.1 du 23/10/2023
# Licence ..... : réalisé dans le cadre du cours Outils Collaboratifs en ligne
# Usage ....... : Pour exécuter : streamlit run streamlit.py
# ********************************************************/

import streamlit as st
from exif import Image
import ast, folium
from streamlit_folium import st_folium

st.title('OIC - Chapitre 4')
st.divider()

# 1 - Affichage de l'image + formulaire d'édition EXIF

img_url = "./woody.jpg"
with open(img_url, 'rb') as img:	# Lecture de l'image
	image = Image(img)

st.image(image.get_file())		# Affichage de l'image
tags = image.list_all()			# Récupération des noms des attributs EXIF définis pour cette image

# for données in tags:
# 	st.write(données, " : ", image[données], f" ({type(image[données])})")

# Modifie la valeur d'une métadonnée de l'image
def update_attr(tag: str, value):
	if tag in ['gps_latitude', 'gps_longitude']:	# conversion des coordonnées (reçues du formulaire en str
		value = ast.literal_eval(value)				# mais attendues comme des tuples)
	try:											# mise à jour de la métadonnée
		image[tag] = value
		# st.success(f"Mise à jour de {tag} réussie.")
	except ValueError:								# message d'erreur en cas de format invalide
		st.error(f"{tag} : saisie invalide (type attendu {type(image[tag])})")


# Mise à jour de l'ensemble des métadonnées saisies dans le formulaire
def update():
	for donnée in tags:							# parcours des métadonnées modifiables
		x = getattr(st.session_state, donnée)	# inspection des données issues du formulaire
		if x != "":								# si saisie utilisateur :
			update_attr(donnée, x)				# mise à jour de la donnée
	with open(img_url, 'wb') as new_image:		# enregistrement de l'image avec les nouvelles données
		new_image.write(image.get_file())


# Formulaire de modification des métadonnées
with st.expander("Modifier les métadonnées"):		# dans un menu dépliant
	with st.form("exif", clear_on_submit=True):		
		for donnée in tags:							# création d'un champ par métadonnée
			st.text_input(donnée, key=donnée, placeholder=image[donnée])

		submit = st.form_submit_button("Confirmer", on_click=update())
	if submit: 
		st.rerun()			# pour mise à jour des valeurs dans le formulaire


# 3 - Affichage des coordonnées GPS de la photo


# conversion de coordonnées d'un format <(degrés, minutes, secondes), direction> vers décimal
def DMS2DD(coord, direction):
	dd = coord[0] + (coord[1]/60) + (coord[2]/3600)
	if (direction == "S" or direction == "W"):
		dd = -dd
	return(dd)


# conversion des coordonnées en décimal
lat = DMS2DD(image.gps_latitude, image.gps_latitude_ref)
lon = DMS2DD(image.gps_longitude, image.gps_longitude_ref)

coord = [{'lat': lat, 'lon': lon}]
st.map(coord)	# affichage de la carte


# 4 - Affichage des POI(s) reliés

st.divider()
st.subheader("Lieux visités")

# sélection du fond de carte
tiles = st.radio(
		"Choix du fond de carte :",
		["OpenStreetMap", "Stamen Terrain", "CartoDB dark_matter", "Stamen Watercolor"],
		horizontal=True
		)

# création de la carte
m = folium.Map(
	location=(lat, lon), 
	zoom_start=3, 
	tiles=tiles,
	width=500,
	heigth=100
)

lieux = {
	"Gent": (51.05260, 3.72738),
	"Gallway": (53.28490, -9.02767),
	"Gimsoya": (68.33650, 14.09302),
	"Leipzig": (51.33945, 12.38990),
	"Tbilisi": (41.73794, 44.78761),
	"La-Palud-sur-Verdon": (43.77990, 6.34179),
	"Visselhövede": (52.98568, 9.58045),
}

# création des marqueurs (POI)
for nom, coordonnées in lieux.items():
	folium.Marker(
		location=coordonnées,
		popup=nom,
		icon=folium.Icon(icon="cloud", color="red"),
	).add_to(m)

# ajout de segments entre les différents points
folium.Polygon(
    locations=lieux.values(),
    color="teal",
    weight=2,
).add_to(m)

# affichage de la carte
st_data = st_folium(m, 	width=700)
