# Nom ......... : vues.py
# Rôle ........ : Affichage des consultations quotidienne d'un article dans les 2 mois
# Auteur ...... : Rosalie Duteuil
# Version ..... : V1.1 du 20/10/2023
# Licence ..... : réalisé dans le cadre du cours Outils Collaboratifs en ligne
# Usage ....... : Pour exécuter : python3 vues.py
# ********************************************************/
#!/usr/bin/env python3

import requests
from plotly import offline

titre = "Prix_Nobel"
url = "https://fr.wikipedia.org/w/api.php?"
params = {
	'action': 'query',			
	'prop': 'pageviews|info',	# modules utilisés (info pour l'url)
	'pvipdays': 60,				# nombre de jours
	'inprop': 'url',			# ajout des URL dans les informations
	'titles': titre,
	'format': 'json'
}

resultat = requests.get(url, params=params).json() 	# récupération du résultat au format JSON

# accès aux informations sur la page en question
infos = resultat['query']['pages']		
infos = next(iter(infos.values()))

dates, vues = [], []

# récupération des valeurs date et nombre de vues
for jour, nb_vues in infos['pageviews'].items():
	dates.append(jour)
	vues.append(nb_vues)

# construction du graphique
data = [{
	'type': 'scatter',
	'x': dates,
	'y': vues,
	'mode': 'markers+lines',
}]

# paramétrage des légendes
agencement = {
	'title': f"Popularité de l'article <a href='{infos['fullurl']}'>{infos['title']}</a>",
	'xaxis': {'title': "Date"},
	'yaxis': {'title': "Nombre de vues"},
}

fig = {'data': data, 'layout': agencement}
offline.plot(fig, filename='vues.html')
