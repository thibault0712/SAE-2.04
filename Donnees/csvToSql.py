# TODO add information when one line is finished
# TODO Doc
# TODO rename dateTemp

from datetime import datetime
import csv

sqlFileGenerationContent = []
compteurCSV = []
quartierCSV = []
quartierCompteurCSV = []
quartierLongueurPisteCSV = []
dateTempCSV = []
comptageVeloCSV = []

def convert_date(date_str):
    """Convertit une date au format JJ/MM/AAAA en AAAA-MM-JJ"""
    return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")


sqlFileGenerationContent.append("DELETE FROM Comptage_Velo;")
sqlFileGenerationContent.append("DELETE FROM Compteurs;")
sqlFileGenerationContent.append("DELETE FROM Quartiers;")
sqlFileGenerationContent.append("DELETE FROM Date;")

# Read the data
with open("s204_compteurs.csv", newline="", encoding="utf-8") as fichier:
    next(fichier)  # Ignore la première ligne du fichier (permet d'éviter l'entête)
    for ligne in fichier:
        compteur = ligne.split(";")
        compteurCSV.append(compteur)


with open("s204_quartiers.csv", newline="", encoding="utf-8") as fichier:
    next(fichier)  # Ignore la première ligne du fichier (permet d'éviter l'entête)
    for ligne in fichier:
        quartier = ligne.split(";")
        quartierCSV.append(quartier)


with open("s204_quartier_compteur.csv", newline="", encoding="utf-8") as fichier:
    next(fichier)  # Ignore la première ligne du fichier (permet d'éviter l'entête)
    for ligne in fichier:
        quartier_compteur = ligne.split(";")
        quartierCompteurCSV.append(quartier_compteur)


with open("s204_longueur_pistes_velo.csv", newline="", encoding="utf-8") as fichier:
    next(fichier)  # Ignore la première ligne du fichier (permet d'éviter l'entête)
    for ligne in fichier:
        longueur_piste_velo = ligne.split(";")
        quartierLongueurPisteCSV.append(longueur_piste_velo)


with open("s204_comptageVelo.csv", newline="", encoding="utf-8") as fichier:
    next(fichier)  # Ignore la première ligne du fichier (permet d'éviter l'entête)
    for ligne in fichier:
        comptage_velo = ligne.split(";")
        comptageVeloCSV.append(comptage_velo)

with open("s204_temperature.csv", newline="", encoding="utf-8") as fichier:
    next(fichier)  # Ignore la première ligne du fichier (permet d'éviter l'entête)
    for ligne in fichier:
        temperature = ligne.split(";")
        dateTempCSV.append(temperature)



sqlFileGenerationContent.append("-- Insertion dans la table Date")

for i in range(0, len(comptageVeloCSV)):
    temperaturetrouvee = False
    j = 0

    tableDate = ["", -1, -1, ""] # Date (date DATE (1), jour INT (NN), temperatureMoyenne FLOAT (NN), vacances VARCHAR (NN))

    tableDate[0] = convert_date(comptageVeloCSV[i][1]) # date DATE (1) 
    tableDate[1] = int(comptageVeloCSV[i][4])          # jour INT (NN)

    # Trouve et verifie si une temperature existe bien pour une certaine date, si rien a été trouvé on n'insert pas la requete
    while j < len(dateTempCSV) and not temperaturetrouvee:
        if dateTempCSV[j][0] == tableDate[0]:
            tableDate[2] = float(dateTempCSV[j][1].replace(",", ".").strip()) # temperatureMoyenne FLOAT (NN)
            temperaturetrouvee = True
        j = j + 1

    tableDate[3] = comptageVeloCSV[i][5].strip()       # vacances VARCHAR (NN)

    # Une temperature a ete trouvé on peut donc inserer les donnees de tableData
    if temperaturetrouvee:
        sqlFileGenerationContent.append((
            f'INSERT INTO Date (date, jour, temperatureMoyenne, vacances) VALUES ("{tableDate[0]}", {tableDate[1]}, {tableDate[2]}, "{tableDate[3]}");'
        ))



sqlFileGenerationContent.append("-- Insertion dans la table Quartiers")

for i in range(0, len(quartierCSV)):
    j = 0
    longueurTrouvee = False

    tableQuartiers = [-1, "", -1] # Quartiers (idQuartier INT (1), nomQuartier VARCHAR (NN), amenagementCyclable FLOAT (NN))

    tableQuartiers[0] = int(quartierCSV[i][0])    # idQuartier INT (1)
    tableQuartiers[1] = quartierCSV[i][1].strip() # nomQuartier VARCHAR (NN)

    # Trouve et vérifie si le quartier possède bien une donnée pour la longueur piste cyclable, si rien on n'insere pas la requete
    while j<len(quartierLongueurPisteCSV) and not longueurTrouvee:
        if quartierLongueurPisteCSV[j][0] == quartierCSV[i][0]:
            tableQuartiers[2] = float(quartierLongueurPisteCSV[j][1].replace(",", ".").strip()) # amenagementCyclable FLOAT (NN)
            longueurTrouvee = True
        j = j + 1

    # Si une longueur de piste a été trouvée on peut insérer la donnée
    if longueurTrouvee:
        sqlFileGenerationContent.append(
            f"INSERT INTO Quartiers (idQuartier, nomQuartier, amenagementCyclable) VALUES ({tableQuartiers[0]}, '{tableQuartiers[1]}', {tableQuartiers[2]});"
        )



sqlFileGenerationContent.append("-- Insertion dans la table Compteurs")

for i in range(0, len(compteurCSV)):
    quartierTrouve = False
    j = 0

    tableCompteurs = [-1, -1, ""] # Compteurs (idCompteur INT (1), unQuartier=@Quartiers.identifiant INT, localisation VARCHAR (NN))

    tableCompteurs[0] = int(compteurCSV[i][0]) # idCompteur INT (1)
    
    # On ajoute et vérifie que le compteur possède bien un quartier, si il ne possède pas de quartier rien ne sera insere
    while j<len(quartierCompteurCSV) and not quartierTrouve:
        if quartierCompteurCSV[j][0] == compteurCSV[i][0] and quartierCompteurCSV[j][1].strip() != "":
            tableCompteurs[1] = int(quartierCompteurCSV[j][1].strip()) # unQuartier=@Quartiers.identifiant INT
            quartierTrouve = True
        j = j + 1

    tableCompteurs[2] = compteurCSV[i][1].strip() # localisation VARCHAR (NN)

    # Si un quartier pour le compteur a été trouvé alors on ajoute la donnee.
    if quartierTrouve:
        sqlFileGenerationContent.append(
            f'INSERT INTO Compteurs (idCompteur, unQuartier, localisation) VALUES ({tableCompteurs[0]}, {tableCompteurs[1]}, "{tableCompteurs[2]}");'
        )


sqlFileGenerationContent.append("-- Insertion dans la table Comptage_Velo")

for i in range (0, len(comptageVeloCSV)):
    leTrucAAdd = [0, "", 0, ""]
    leTrucAAdd[0] = int(comptageVeloCSV[i][0])
    leTrucAAdd[1] = convert_date(comptageVeloCSV[i][1])
    leTrucAAdd[2] = int(comptageVeloCSV[i][2])
    leTrucAAdd[3] = comptageVeloCSV[i][3]

    if comptageVeloCSV[i][3] == "":
        leTrucAAdd[3] = 'NULL'

    OKCompteur = False
    j = 0
    while j<len(compteurCSV) and not OKCompteur:
        if leTrucAAdd[0] == int(compteurCSV[j][0]):
            OKCompteur = True
        j = j+1
    OKDate = False
    j = 0
    while j<len(dateTempCSV) and not OKDate:
        if leTrucAAdd[1] == dateTempCSV[j][0]:
            OKDate = True
        j = j+1
    print("OKDate " + str(OKDate) + " OKCompteur " + str(OKCompteur))
    if(OKDate and OKCompteur):
        if comptageVeloCSV[i][3] == "":
            #Quand 3ème colonne = NULL on ne met pas de ""
            sqlFileGenerationContent.append(
                f"INSERT INTO Comptage_Velo (unCompteur, uneDate, nombresVelos, probabilitePresenceAnomalie) VALUES ({leTrucAAdd[0]}, '{leTrucAAdd[1]}', {leTrucAAdd[2]}, {leTrucAAdd[3]});"
            )
        else:
            #Quand 3ème colonne != NULL on met ""
            sqlFileGenerationContent.append(
                f"INSERT INTO Comptage_Velo (unCompteur, uneDate, nombresVelos, probabilitePresenceAnomalie) VALUES ({leTrucAAdd[0]}, '{leTrucAAdd[1]}', {leTrucAAdd[2]}, '{leTrucAAdd[3]}');"
            )
        print(sqlFileGenerationContent[-1])
    else:
        print("Erreur avec les donnée, Date ou compteur manquant pour le comptage " + str(leTrucAAdd[0]) + " " + str(leTrucAAdd[1]))

sqlFileGenerationContent = list(dict.fromkeys(sqlFileGenerationContent))

# Sauvegarde dans un fichier SQL
with open("insert_data.sql", "w", encoding="utf-8") as f:
    f.writelines("\n".join(sqlFileGenerationContent) + "\n")

print("Script SQL généré avec succès dans insert_data.sql")