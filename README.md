# Base de données - Comptage des vélos

## Modèle UML

```plaintext
Comptage_Velo(num_compteurs=@Compeurs.numero INT (1), date=@Date.date DATE (1), nombre_velos INT (NN), Probalite_presence_anomalie VARCHAR)

Compteur (idCompteur INT (1), idQuartier=@Quartiers.identifiant INT, libelle VARCHAR (NN))

Quartiers (identifiant INT (1), nom STRING (NN), amenagement_cyclable FLOAT (NN))

Date (date (1), jour, températureMoyenne (NN), vacances (NN))
```

## Contraintes TXT :
- Le jour_de_la_semaine est entre 1 et 7 INCLUS
- amenagement_cyclable > 0
