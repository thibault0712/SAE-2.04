# Base de données - Comptage des vélos

## Modèle UML

```plaintext
Comptage_Velo
-------------
- num_compteurs : INT (FK -> Compteurs.numero)
- date : DATE (FK -> Date.date)
- nombre_velos : INT (NN)
- Probalite_presence_anomalie : VARCHAR

Compteur
-------------
- idCompteur : INT (PK)
- idQuartier : INT (FK -> Quartiers.identifiant)
- libelle : VARCHAR (NN)

Quartiers
-------------
- identifiant : INT (PK)
- nom : STRING (NN)
- amenagement_cyclable : FLOAT (NN)

Date
-------------
- date : DATE (PK)
- jour : INT
- températureMoyenne : FLOAT (NN)
- vacances : BOOLEAN (NN)
```

## Contraintes

- `jour` doit être compris entre 1 et 7 inclus.
- `amenagement_cyclable` doit être strictement supérieur à 0.
