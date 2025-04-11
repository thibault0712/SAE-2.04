# TODO add information when one line is finished

from datetime import datetime
import csv

sqlFileGenerationContent = []
compteursCSV = []
quartiersCSV = []
quartierCompteurCSV = []
quartierLongueurPisteVeloCSV = []
temperatureCSV = []
comptageVeloCSV = []

# Convertit une date au format JJ/MM/AAAA en AAAA-MM-JJ
def convert_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")

# Lit le contenu d'un fichier CSV sans en-tête
def lire_csv(path):
    result = []

    with open(path, newline="", encoding="utf-8") as fichier:
        next(fichier) # Ignore la première ligne du fichier (permet d'éviter l'en-tête)

        for ligne in fichier:
            ligne = ligne.strip() # Enlève les \n
            ligne = ligne.replace("'", "''") # Remplace les ' par '' pour éviter les erreurs d'insertion SQL
            result.append(ligne.split(";")) # Strip pour retirer les lignes inutiles

        return result

# Transforme une colonne d'une liste en un set de données (plus rapide pour les recherches)
def colomne_to_set(liste, colonne):
    result = set()

    for i in range(0, len(liste)):
        result.add(liste[i][colonne])

    return result


#---------------------------------------------------------
#           RECUPERER LE CONTENU DES FICHIERS CSV
#---------------------------------------------------------
print("\033[1;34m[📚] Récupération du contenu des fichiers")

print("\033[0m[1/6] Récupération de \033[1;34ms204_compteurs.csv")
compteursCSV = lire_csv("Donnees\s204_compteurs.csv")

print("\033[0m[2/6] Récupération de \033[1;34ms204_quartiers.csv")
quartiersCSV = lire_csv("Donnees\s204_quartiers.csv")

print("\033[0m[3/6] Récupération de \033[1;34ms204_quartier_compteur.csv")
quartierCompteurCSV = lire_csv("Donnees\s204_quartier_compteur.csv")

print("\033[0m[4/6] Récupération de \033[1;34ms204_longueur_pistes_velo.csv")
quartierLongueurPisteVeloCSV = lire_csv("Donnees\s204_longueur_pistes_velo.csv")

print("\033[0m[5/6] Récupération de \033[1;34ms204_comptageVelo.csv")
comptageVeloCSV = lire_csv("Donnees\s204_comptageVelo.csv")

print("\033[0m[6/6] Récupération de \033[1;34ms204_temperature.csv")
temperatureCSV = lire_csv("Donnees\s204_temperature.csv")


#---------------------------------------------------------
#            ECRITURE DES LIGNES D'INSERTIONS
#---------------------------------------------------------
print("\n\033[1;34m[✏️] Ecriture des lignes d'insertions pour toutes les tables")

# Insertion de toutes les lignes permettant de vider toutes les tables
print("\033[0m[1/5] Insertion de toutes les lignes permettant de vider toutes les tables")
sqlFileGenerationContent.append("DELETE FROM Comptage_Velo;")
sqlFileGenerationContent.append("DELETE FROM Compteurs;")
sqlFileGenerationContent.append("DELETE FROM Quartiers;")
sqlFileGenerationContent.append("DELETE FROM Date;")


# Insertion de toutes les données pour la table Date
# Date (date DATE (1), jour INT (NN), temperatureMoyenne FLOAT (NN), vacances VARCHAR (NN))
print("\033[0m[2/5] Insertion de toutes les données pour la table \033[1;34mDate \033[1;33m(le processus peut prendre plusieurs minutes)")
sqlFileGenerationContent.append("\n-- Insertion dans la table Date")
for i in range(0, len(comptageVeloCSV)):
    temperaturetrouvee = False
    j = 0

    tableDate = ["", -1, -1, ""] # Date (date DATE (1), jour INT (NN), temperatureMoyenne FLOAT (NN), vacances VARCHAR (NN))

    tableDate[0] = convert_date(comptageVeloCSV[i][1]) # date DATE (1) 
    tableDate[1] = int(comptageVeloCSV[i][4])          # jour INT (NN)

    # Trouve et verifie si une temperature existe bien pour une certaine date, si rien a été trouvé on n'insert pas la requete
    while j < len(temperatureCSV) and not temperaturetrouvee:
        if temperatureCSV[j][0] == tableDate[0]:
            tableDate[2] = float(temperatureCSV[j][1].replace(",", ".")) # temperatureMoyenne FLOAT (NN)
            temperaturetrouvee = True
        j = j + 1

    tableDate[3] = comptageVeloCSV[i][5]       # vacances VARCHAR (NN)

    sqlFileGenerationContent.append((
        f"INSERT INTO Date (date, jour, temperatureMoyenne, vacances) VALUES ('{tableDate[0]}', {tableDate[1]}, {tableDate[2]}, '{tableDate[3]}');"
    ))


# Insertion de toutes les données pour la table Quartiers
# Quartiers (idQuartier INT (1), nomQuartier VARCHAR (NN), amenagementCyclable FLOAT (NN))
print("\033[0m[3/5] Insertion de toutes les données pour la table \033[1;34mQuartiers")
sqlFileGenerationContent.append("-- Insertion dans la table Quartiers")
for i in range(0, len(quartiersCSV)):
    longueurTrouvee = False
    j = 0

    tableQuartiers = [-1, "", -1] # Quartiers (idQuartier INT (1), nomQuartier VARCHAR (NN), amenagementCyclable FLOAT (NN))

    tableQuartiers[0] = int(quartiersCSV[i][0])    # idQuartier INT (1)
    tableQuartiers[1] = quartiersCSV[i][1]         # nomQuartier VARCHAR (NN)

    # Trouve et vérifie si le quartier possède bien une donnée pour la longueur piste cyclable, si rien on n'insere pas la requete
    while j<len(quartierLongueurPisteVeloCSV) and not longueurTrouvee:
        if quartierLongueurPisteVeloCSV[j][0] == quartiersCSV[i][0]:
            tableQuartiers[2] = float(quartierLongueurPisteVeloCSV[j][1].replace(",", ".")) # amenagementCyclable FLOAT (NN)
            longueurTrouvee = True
        j = j + 1

    sqlFileGenerationContent.append(
        f"INSERT INTO Quartiers (idQuartier, nomQuartier, amenagementCyclable) VALUES ({tableQuartiers[0]}, '{tableQuartiers[1]}', {tableQuartiers[2]});"
    )


# Insertion de toutes les données pour la table Compteurs
# Compteurs (idCompteur INT (1), unQuartier=@Quartiers.identifiant INT, localisation VARCHAR (NN))
print("\033[0m[4/5] Insertion de toutes les données pour la table \033[1;34mCompteurs")
sqlFileGenerationContent.append("-- Insertion dans la table Compteurs")
dataSetIdQuartiers = colomne_to_set(quartierCompteurCSV, 0) # Set de tous les idQuartiers. On utilise un set pour une recherche plus rapide
for i in range(0, len(compteursCSV)):
    quartierTrouve = False
    j = 0

    tableCompteurs = [-1, -1, ""] # Compteurs (idCompteur INT (1), unQuartier=@Quartiers.identifiant INT, localisation VARCHAR (NN))

    tableCompteurs[0] = int(compteursCSV[i][0]) # idCompteur INT (1)
    
    # On ajoute et vérifie que le compteur possède bien un quartier, si il ne possède pas de quartier rien ne sera insere
    while j<len(quartierCompteurCSV) and not quartierTrouve:
        if quartierCompteurCSV[j][0] == compteursCSV[i][0] and quartierCompteurCSV[j][1].strip() != "":
            tableCompteurs[1] = int(quartierCompteurCSV[j][1].strip()) # unQuartier=@Quartiers.identifiant INT
            quartierTrouve = True
        j = j + 1

    tableCompteurs[2] = compteursCSV[i][1] # localisation VARCHAR (NN)

    # Si un quartier pour le compteur a été trouvé alors on ajoute la donnee.
    if quartierTrouve:
        sqlFileGenerationContent.append(
            f"INSERT INTO Compteurs (idCompteur, unQuartier, localisation) VALUES ({tableCompteurs[0]}, {tableCompteurs[1]}, '{tableCompteurs[2]}');"
        )


# Insertion de toutes les données pour la table Comptage_Velo
# Comptage_Velo(unCompteur=@Compeurs.idCompteur INT (1), uneDate=@Date.date DATE (1), nombreVelos INT (NN), probalitePresenceAnomalie VARCHAR)
print("\033[0m[5/5] Insertion de toutes les données pour la table \033[1;34mComptage_Velo \033[1;33m(le processus peut prendre une minute)")
sqlFileGenerationContent.append("-- Insertion dans la table Comptage_Velo")
dataSetTemperatureDate = colomne_to_set(temperatureCSV, 0) # Set de toutes les dates de temperature. On utilise un set pour une recherche plus rapide
dataSetIdCompteurs = colomne_to_set(compteursCSV, 0) # Set de tous les idCompteurs. On utilise un set pour une recherche plus rapide
dataSetPrimaryKey = set()
for i in range (0, len(comptageVeloCSV)):

    tableComptageVelo = [-1, "", -1, ""] # Comptage_Velo(unCompteur=@Compeurs.idCompteur INT (1), uneDate=@Date.date DATE (1), nombreVelos INT (NN), probalitePresenceAnomalie VARCHAR)

    # Vérifie si unCompteur existe bien dans la liste des id des compteurs. Si il existe on insère la donnée sinon rien
    if comptageVeloCSV[i][0] in dataSetIdCompteurs:
        tableComptageVelo[0] = int(comptageVeloCSV[i][0]) # unCompteur=@Compeurs.idCompteur INT
    else:
        continue # On passe directement à la prochaine itération de la boucle

    # Vérifie si uneDate existe bien dans la liste des des dates de Date. Si il existe on insère la donnée sinon rien
    if convert_date(comptageVeloCSV[i][1]) in dataSetTemperatureDate:
        tableComptageVelo[1] = convert_date(comptageVeloCSV[i][1]) # uneDate=@Date.date DATE
    else:
        continue # On passe directement à la prochaine itération de la boucle

    tableComptageVelo[2] = int(comptageVeloCSV[i][2]) # nombreVelos INT

    # Insère NULL pour probabilitePresenceAnomalie si la case est vide sinon on envoie le contenu de la case
    if comptageVeloCSV[i][3] == "":
        tableComptageVelo[3] = "NULL" # probalitePresenceAnomalie VARCHAR
    else:
        tableComptageVelo[3] = comptageVeloCSV[i][3] # probalitePresenceAnomalie VARCHAR

    # Si il existe déjà les données avec la même clef on insère rien (il y a certaines données qui sont exactement les mêmes dans le excel pour une date et un nombre de vélo donné)
    if(str(tableComptageVelo[0]) + str(tableComptageVelo[1]) not in dataSetPrimaryKey):
        if comptageVeloCSV[i][3] == "":
            # Quand 3ème colonne = NULL on ne met pas de ""
            sqlFileGenerationContent.append(
                f"INSERT INTO Comptage_Velo (unCompteur, uneDate, nombresVelos, probabilitePresenceAnomalie) VALUES ({tableComptageVelo[0]}, '{tableComptageVelo[1]}', {tableComptageVelo[2]}, {tableComptageVelo[3]});"
            )
        else:
            #Quand 3ème colonne != NULL on met ""
            sqlFileGenerationContent.append(
                f"INSERT INTO Comptage_Velo (unCompteur, uneDate, nombresVelos, probabilitePresenceAnomalie) VALUES ({tableComptageVelo[0]}, '{tableComptageVelo[1]}', {tableComptageVelo[2]}, '{tableComptageVelo[3]}');"
            )
        dataSetPrimaryKey.add(str(tableComptageVelo[0]) + str(tableComptageVelo[1]))


#---------------------------------------------------------
#                GENERATION DU FICHIER SQL
#---------------------------------------------------------
print("\n\033[1;34m[⚡] Engeristrement du fichier")
# Supprimer les doublons si il y en a
sqlFileGenerationContent = list(dict.fromkeys(sqlFileGenerationContent))

# Sauvegarde dans un fichier SQL
with open("S2.04_Insertion_données.sql", "w", encoding="utf-8") as f:
    f.writelines("\n".join(sqlFileGenerationContent) + "\n")

print("\n\033[1;34m[✅] S2.04_Insertion_données.sql généré avec succès, exécuter le fichier pour insérer les données dans la base de données.")