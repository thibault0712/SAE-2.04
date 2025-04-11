# Base de données - Comptage des vélos

## Script python
Afin d'insérer les données csv vers la base de donnée nous avons fait le choix de développer un script qui se charge de convertir et de vérifier tous les fichiers CSV vers un fichier d'insertion de données SQL. Une fois le fichier SQL généré il faut l'exécuter pour insérer les données.  

### Lancement du script
```python 
python .\S2.04_Script_convertion_CSV_vers_SQL.py
```
un fichier sql intitulé **S2.04_Insertion_données.sql** a été généré. Il ne reste plus qu'à l'exécuter. 

### Elements importants sur le script
- Afin d'avoir un script assez rapide, nous avons utilisé les **set()** de python pour savoir si une donnée existe bien ou non dans les fichiers CSV cela est plus rapide qu'utiliser des tableaux. 
- Le script se charge automatiquement de retirer tous les problèmes possible des fichiers excel comme des références impossibles ou encore des clefs primaires en double (même date et même quantité de vélo).

## Modèle UML

### Schéma relationnel 
```plaintext
Comptage_Velo(unCompteur=@Compeurs.idCompteur INT (1), uneDate=@Date.date DATE (1), nombreVelos INT (NN), probalitePresenceAnomalie VARCHAR)

Compteurs (idCompteur INT (1), unQuartier=@Quartiers.identifiant INT, localisation VARCHAR (NN))

Quartiers (idQuartier INT (1), nomQuartier VARCHAR (NN), amenagementCyclable FLOAT (NN))

Date (date DATE (1), jour INT (NN), temperatureMoyenne FLOAT (NN), vacances VARCHAR (NN))
```

### Contraintes TXT :
- Le jour_de_la_semaine est entre 1 et 7 INCLUS
- amenagement_cyclable > 0
- La probabilité d'une anomalie est soit Fort | Moyen | Faible ou Rien
