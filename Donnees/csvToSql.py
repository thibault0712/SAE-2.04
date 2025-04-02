from datetime import datetime
import csv

def convert_date(date_str):
    """Convertit une date au format JJ/MM/AAAA en AAAA-MM-JJ"""
    return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")

sql_statements = []

compteurCSV = []
quartierCSV = []
quartierCompteurCSV = []
quartierLongueurPisteCSV = []
dateTempCSV = []
comptageVeloCSV = []

with open("s204_compteurs.csv", newline="", encoding="utf-8") as fichier:
    cpt = 0
    for ligne in fichier:
        print(ligne)
        if cpt != 0:
            print("test")
            compteur = ligne.split(";")
            compteurCSV.append(compteur)
            
        cpt = cpt+1

with open("s204_quartiers.csv", newline="", encoding="utf-8") as fichier:
    cpt = 0
    for ligne in fichier:
        print(ligne)
        if cpt != 0:
            quartier = ligne.split(";")
            quartierCSV.append(quartier)
            
        cpt = cpt+1

with open("s204_quartier_compteur.csv", newline="", encoding="utf-8") as fichier:
    cpt = 0
    for ligne in fichier:
        print(ligne)
        if cpt != 0:
            quartier_compteur = ligne.split(";")
            quartierCompteurCSV.append(quartier_compteur)
            
        cpt = cpt+1

with open("s204_longueur_pistes_velo.csv", newline="", encoding="utf-8") as fichier:
    cpt = 0
    for ligne in fichier:
        print(ligne)
        if cpt != 0:
            longueur_piste_velo = ligne.split(";")
            quartierLongueurPisteCSV.append(longueur_piste_velo)

        cpt = cpt+1

with open("s204_comptageVelo.csv", newline="", encoding="utf-8") as fichier:
    cpt = 0
    for ligne in fichier:
        print(ligne)
        if cpt != 0:
            comptage_velo = ligne.split(";")
            comptageVeloCSV.append(comptage_velo)

        cpt = cpt+1

with open("s204_temperature.csv", newline="", encoding="utf-8") as fichier:
    cpt = 0
    for ligne in fichier:
        print(ligne)
        if cpt != 0:
            temperature = ligne.split(";")
            dateTempCSV.append(temperature)

        cpt = cpt+1


sql_statements.append("-- Insertion dans la table Date")

for i in range(0, len(comptageVeloCSV)):
    leTrucAAdd = ["", None, 0, ""]
    leTrucAAdd[0] = convert_date(comptageVeloCSV[i][1])
    leTrucAAdd[1] = None
    leTrucAAdd[2] = int(comptageVeloCSV[i][4])
    leTrucAAdd[3] = comptageVeloCSV[i][5].strip()

    temptrouvee = False
    j = 0

    while j<len(dateTempCSV) and not temptrouvee:
        if dateTempCSV[j][0] == leTrucAAdd[0]:
            leTrucAAdd[1] = float(dateTempCSV[j][1].replace(",", ".").strip())
            temptrouvee = True
        j = j+1

    sql_statements.append(
        f"INSERT INTO Date (date, jour, temperatureMoyenne, vacances) VALUES ('{leTrucAAdd[0]}', {leTrucAAdd[2]}, {leTrucAAdd[1]}, '{leTrucAAdd[3]}');"
    )
    print(sql_statements[-1])

sql_statements.append("-- Insertion dans la table Quartiers")

for i in range(0, len(quartierCSV)):
    leTrucAAdd = [0, "", 0]
    leTrucAAdd[0] = int(quartierCSV[i][0])
    leTrucAAdd[1] = quartierCSV[i][1].strip()

    j = 0
    longTrouvee = False

    while j<len(quartierLongueurPisteCSV) and not longTrouvee:
        if quartierLongueurPisteCSV[j][0] == quartierCSV[j][0]:
            leTrucAAdd[2] = float(quartierLongueurPisteCSV[j][1].replace(",", ".").strip())
            longTrouvee = True
        j = j+1

    if longTrouvee:
        sql_statements.append(
            f"INSERT INTO Quartiers (idQuartier, nomQuartier, amenagementCyclable) VALUES ({leTrucAAdd[0]}, '{leTrucAAdd[1]}', {leTrucAAdd[2]});"
        )
        print(sql_statements[-1])
    else:
        print("longueur de piste non trouvé pour le quartier " + leTrucAAdd[1])

sql_statements.append("-- Insertion dans la table Compteurs")

for i in range(0, len(compteurCSV)):
    leTrucAAdd = [0, None, ""]
    leTrucAAdd[0] = int(compteurCSV[i][0])
    leTrucAAdd[1] = None
    leTrucAAdd[2] = compteurCSV[i][1].strip()

    quartierTrouvee = False
    j = 0
    while j<len(quartierCompteurCSV) and not quartierTrouvee:
        if quartierCompteurCSV[j][0] == compteurCSV[j][0]:
            leTrucAAdd[1] = int(quartierCompteurCSV[j][1])
            quartierTrouvee = True
        j = j+1

    sql_statements.append(
        f"INSERT INTO Compteurs (idCompteur, unQuartier, localisation) VALUES ({leTrucAAdd[0]}, {leTrucAAdd[1]}, '{leTrucAAdd[2]}');"
    )
    print(sql_statements[-1])

sql_statements.append("-- Insertion dans la table Comptage_Velo")

for i in range (0, len(comptageVeloCSV)):
    leTrucAAdd = [0, "", 0, ""]
    leTrucAAdd[0] = int(comptageVeloCSV[i][0])
    leTrucAAdd[1] = convert_date(comptageVeloCSV[i][1])
    leTrucAAdd[2] = int(comptageVeloCSV[i][2])
    leTrucAAdd[3] = comptageVeloCSV[i][3]

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
        sql_statements.append(
            f"INSERT INTO Comptage_Velo (unCompteur, date, nombresVelos, probabilitePresenceAnomalie) VALUES ({leTrucAAdd[0]}, '{leTrucAAdd[1]}', {leTrucAAdd[2]}, '{leTrucAAdd[3]}');"
        )
        print(sql_statements[-1])
    else:
        print("Erreur avec les donnée, Date ou compteur manquant pour le comptage " + str(leTrucAAdd[0]) + " " + str(leTrucAAdd[1]))

sql_statements = list(dict.fromkeys(sql_statements))

# Sauvegarde dans un fichier SQL
with open("insert_data.sql", "w", encoding="utf-8") as f:
    f.writelines("\n".join(sql_statements) + "\n")

print("Script SQL généré avec succès dans insert_data.sql")