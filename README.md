# Base de données - Comptage des vélos

## Modèle UML

```plaintext
Comptage_Velo(num_compteurs=@Compeurs.numero INT (1), une_date=@Date.date DATE (1), nombre_velos INT (NN), Probalite_presence_anomalie VARCHAR)

Compteur (idCompteur INT (1), idQuartier=@Quartiers.identifiant INT, libelle VARCHAR (NN))

Quartiers (identifiant INT (1), nom VARCHAR (NN), amenagement_cyclable FLOAT (NN))

Date (date DATE (1), jour INT, températureMoyenne FLOAT (NN), vacances VARCHAR (NN))
```

## Contraintes TXT :
- Le jour_de_la_semaine est entre 1 et 7 INCLUS
- amenagement_cyclable > 0
- La probabilité d'une anomalie est soit Fort | Moyen | Faible ou Rien
- Les vacances sont soit 1 -> Vrai ou 0 -> Faux
