# Nom ......... : apicao.py
# Rôle ........ : API de consultation des données d'aéroports
# Auteur ...... : Rosalie Duteuil
# Version ..... : V1.1 du 21/10/2023
# Licence ..... : réalisé dans le cadre du cours Outils Collaboratifs en ligne
# Usage ....... : Pour exécuter : uvicorn apicao:app --reload
# ********************************************************/

from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel
import json


class airport(BaseModel):
	State_Name: str
	ICAO_Code: str
	Location_Name: str
	Lat: str
	Long: str
	IATA_Code: str


app = FastAPI()

# création de la base de données
client = MongitaClientDisk()
db = client.db 						
airports = db.airports

# remplissage de la base de données depuis le fichier JSON
with open(r"code.json") as f:
	contents = json.loads(f.read())
airports.insert_many(contents)


@app.get("/")
async def root():
	return {"Message": "Bonjour et bienvenue !"}


# Recherche d'un aéroport par son code OACI
@app.get("/airports/{airport_code}")
async def get_airport_by_code(airport_code: str):
	if airports.count_documents({"ICAO_Code": airport_code}) > 0:
		airport = airports.find_one({"ICAO_Code": airport_code})
		return {key: airport[key] for key in airport if key != "_id"}
	raise HTTPException(status_code=404, detail=f"Aucun aéroport avec le code {airport_code} dans la base")


# Affichage de tous les aéroports (/airports) ou de tous ceux d'un pays (/airports?country=...)
@app.get("/airports")
async def get_airport_by_country(country: str = None):
	if country is None:
		result = airports.find({})
	elif airports.count_documents({"State_Name": country}) > 0:
		result = airports.find({"State_Name": country})
	else:
		raise HTTPException(status_code=404, detail=f"Aucun aéroport de {country} dans la base")
	return [
		{key: airport[key] for key in airport if key != "_id"}
		for airport in result
	]


# Ajout d'un aéroport
@app.post("/airports")
async def post_airport(airport: airport):
	airports.insert_one(airport.dict())
	return airport


# Mise à jour des informations sur un aéroport
@app.put("/airports/{airport_code}")
async def update_airport(airport_code: str, airport: airport):
	if airports.count_documents({"ICAO_Code": airport_code}) > 0:
		airports.replace_one({"id": airport_code}, airport.dict())
		return airport
	raise HTTPException(status_code=404, detail=f"Aucun aéroport avec le code {airport_code} dans la base")


# Suppression d'un aéroport
@app.delete("/airports/{airport_code}")
async def delete_airport(airport_code: str):
	delete_result = airports.delete_one({"ICAO_Code": airport_code})
	if delete_result.deleted_count == 0:
		raise HTTPException(status_code=404, detail=f"Aucun aéroport avec le code {airport_code} n'existe dans la base")
	return {"OK": True}
