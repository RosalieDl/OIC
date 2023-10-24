# *******************************************************
# Nom ......... : topwiki.py
# Rôle ........ : Affichage des 20 articles les plus consultés (la veille) sur wikipédia
# Auteur ...... : Rosalie Duteuil
# Version ..... : V1.1 du 20/10/2023
# Licence ..... : réalisé dans le cadre du cours Outils Collaboratifs en ligne
# Usage ....... : Pour exécuter : python3 topwiki.py
# ********************************************************/
#!/usr/bin/env python3

import requests
from plotly.graph_objs import Bar
from plotly import offline
from datetime import date

ajd = date.today()

url = "https://fr.wikipedia.org/w/api.php?action=query&list=mostviewed&pvimlimit=20&format=json"
resultat = requests.get(url).json()		# récupération du résultat au format JSON

pages = resultat['query']['mostviewed']	# accès aux données sur les 20 ressources
titres, vues = [], []

# récupération des valeurs titre et nombre de vues
for page in pages:		
	if page['ns'] == 0:			# on garde seulement les articles (namespace 0)
		titres.append(page['title'])
		vues.append(page['count'])

# construction du graphique
data = [{
	'type': 'bar',
	'x': titres,
	'y': vues,
}]

# paramétrage des légendes
agencement = {
	'title': 'Les stars du Wikipédia francophone',
	'xaxis': {'title': "Nom de l'article"},
	'yaxis': {'title': f"Nombre de vues ({ajd.strftime('%d-%m-%Y')})"},
}

fig = {'data': data, 'layout': agencement}
offline.plot(fig, filename='wikis.html')
