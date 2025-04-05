# Base de données - Comptage des vélos

## Modèle UML

```plaintext
Comptage_Velo(unCompteur=@Compeurs.idCompteur INT (1), une_date=@Date.date DATE (1), nombre_velos INT (NN), Probalite_presence_anomalie VARCHAR)

Compteurs (idCompteur INT (1), unQuartier=@Quartiers.identifiant INT, localisation VARCHAR (NN))

Quartiers (idQuartier INT (1), nomQuartier VARCHAR (NN), amenagementCyclable FLOAT (NN))

Date (date DATE (1), jour INT, temperatureMoyenne FLOAT (NN), vacances VARCHAR (NN))
```

## Contraintes TXT :
- Le jour_de_la_semaine est entre 1 et 7 INCLUS
- amenagement_cyclable > 0
- La probabilité d'une anomalie est soit Fort | Moyen | Faible ou Rien

## TODO
- Verif si OK suppression plusieurs data quand quartierCompteurCSV[j][1] != "":
- Régler les prb de None 
