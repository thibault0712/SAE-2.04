-- 1) Liste des noms des quartiers qui possèdent un compteur
SELECT DISTINCT UPPER(nomQuartier) nomQuartier
FROM Quartiers
INNER JOIN Compteurs ON idQuartier = unQuartier;
/*
 nomQuartier
 CENTRE VILLE
 DERVALLIÈRES - ZOLA
 HAUTS PAVÉS - SAINT FÉLIX
 MALAKOFF - SAINT-DONATIEN
 ILE DE NANTES

 10 Tuples sélectionnés
 */

-- 2) Les dates qui ont exactement le même nombre de vélos pour le même compteur
-- ATTENTION : Requête lourde peut prendre un certain temps
SELECT DISTINCT C1.unCompteur compteur, C1.uneDate Date1, C2.uneDate Date2, C1.nombresVelos nbVelos
FROM Comptage_Velo C1
JOIN Comptage_Velo C2 ON C1.nombresVelos = C2.nombresVelos AND C1.unCompteur = C2.unCompteur
WHERE C1.uneDate < C2.uneDate;
/*
    compteur     Date1        Date2        nbVelos
    664          2020-01-04   2020-10-11   344
    664          2020-01-04   2020-12-23   344
    664          2020-01-05   2021-10-30   375
    664          2020-01-07   2020-07-02   944
    664          2020-01-07   2021-07-22   944

    164 267 tuples sélectionnés
 */

-- 3) Assignation des compteurs aux quartiers, null si aucun compteur n'est assigné à un quartier
SELECT DISTINCT nomQuartier, idCompteur
FROM Compteurs
RIGHT JOIN Quartiers ON Compteurs.unQuartier = Quartiers.idQuartier;
/*
 nomQuartier    idCompteur
 Centre Ville   664
 Centre Ville   665
 Centre Ville   666
 Centre Ville   674
 Centre Ville   675

 60 Tuples sélectionnés
 */

-- 4) Les dates durant lesquelles aucun compteur a enregistré de données
SELECT date
FROM Date
LEFT JOIN Comptage_velo ON Date.date = Comptage_velo.uneDate
WHERE unCompteur IS NULL;
/*
 date
 2021-04-30
 2022-07-31
 2022-08-31

 3 Tuples sélectionnés
 */

-- 5) Tous les quartiers qui n'ont pas de compteur
SELECT idQuartier
FROM Quartiers
WHERE idQuartier NOT IN (
    SELECT DISTINCT unQuartier
    FROM Compteurs
);
/*
 idQuartier
 2
 7
 9
 14301
 14302

 8 Tuples sélectionnés
 */

-- 6) Le nombre de vélo par compteur et date pris en compte uniquement le lundi
SELECT unCompteur, uneDate, nombresVelos
FROM Comptage_velo
WHERE uneDate IN (
    SELECT date
    FROM Date
    WHERE jour = 1
);
/*
 unCompteur     uneDate     nombresVelos
 664            2020-01-06  1019
 665            2020-01-06  882
 666            2020-01-06  254
 667            2020-01-06  2199
 668            2020-01-06  810

 7816 tuples sélectionnés
 */


-- 7) Les compteurs qui ne sont pas utilisés pour relever de l'information
SELECT idCompteur
FROM Compteurs
WHERE NOT EXISTS(
    SELECT unCompteur
    FROM comptage_velo
    WHERE unCompteur = idCompteur
);
/*
 idCompteur
 700
 701

 2 Tuples sélectionnés
 */

-- 8) Les dates en dehors des vacances avec des données qui ont été enregistrées
SELECT date
FROM Date
WHERE UPPER(vacances) != 'HORS VACANCES'
AND EXISTS(
    SELECT uneDate
    FROM Comptage_velo
    WHERE uneDate = date
);
/*
 date
 2020-01-01
 2020-01-02
 2020-01-03
 2020-01-04
 2020-01-05

 380 Tuples sélectionnés
 */

-- 9) Nombre total de données sans anomalie
-- Note : on ne fait pas COUNT(probabilitePresenceAnomalie) car la ligne est tout le temps NULL
SELECT COUNT(*) totalSansAnomalie
FROM Comptage_velo
WHERE probabilitePresenceAnomalie IS NULL;
/*
 totalSansAnomalie
 52198

 1 Tuple sélectionné
 */

-- 10) Nombre total de vélo
SELECT SUM(nombresVelos) totalVelo
FROM Comptage_velo;
/*
 totalVelo
 35191966

 1 Tuple sélectionné
 */

-- 11) Nombre total de vélo par date
SELECT uneDate, SUM(nombresVelos) totalVelo
FROM Comptage_velo
GROUP BY uneDate;
/*
 uneDate        totalVelo
 2020-01-01     7621
 2020-01-02     20385
 2020-01-03     22050
 2020-01-04     18295
 2020-01-05     14976

 1117 Tuples sélectionnés
 */

-- 12) Nombre total de compteurs par quartier
SELECT idQuartier, nomQuartier, COUNT(idCompteur) totalCompteur
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
GROUP BY idQuartier;
/*
 idQuartier nomQuartier                 totalCompteur
 1          Centre Ville                22
 3          Dervallières - Zola         1
 4          Hauts Pavés - Saint Félix   4
 5          Malakoff - Saint-Donatien   9
 6          Ile de Nantes               6

 10 Tuples sélectionnés
 */

-- 13) Les quartiers qui ont au moins 3 Compteurs
SELECT idQuartier, nomQuartier, COUNT(idCompteur) totalCompteur
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
GROUP BY idQuartier
HAVING COUNT(idCompteur) >= 3;
/*
 idQuartier     nomQuartier                 totalCompteur
 1              Centre Ville                22
 4              Hauts Pavés - Saint Félix   4
 5              Malakoff - Saint-Donatien   9
 6              Ile de Nantes               6

 4 Tuples sélectionnés
 */

-- 14) Les quartiers ayant eu au moins 500000 vélos au total
SELECT idQuartier, nomQuartier, SUM(nombresVelos) totalVelo
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
JOIN Comptage_velo ON idCompteur = unCompteur
GROUP BY idQuartier
HAVING SUM(nombresVelos) >= 500000;
/*
 idQuartier  nomQuartier                 totalVelo
 1           Centre Ville                20084046
 3           Dervallières - Zola         848031
 4           Hauts Pavés - Saint Félix   2163205
 5           Malakoff - Saint-Donatien   2618402
 6           Ile de Nantes               6106186

 7 Tuples sélectionnés
 */

-- 15) Les compteurs qui ont récupéré les données pour tous les jours supérieur à 20°
SELECT DISTINCT c1.unCompteur
FROM Comptage_velo c1
WHERE NOT EXISTS(
    SELECT date
    FROM Date
    WHERE temperatureMoyenne > 20
    EXCEPT
    SELECT c2.uneDate
    FROM Comptage_velo c2
    WHERE c1.unCompteur = c2.unCompteur
);
/*
 unCompteur
 664
 665
 666
 667
 668

 48 tuples sélectionnés
 */

-- 16) Les compteurs qui récupèrent des informations uniquement pour tous les weekends
SELECT DISTINCT c1.unCompteur
FROM Comptage_velo c1
WHERE NOT EXISTS(
    SELECT date
    FROM Date
    WHERE jour = 6 OR jour = 7
    EXCEPT
    SELECT c2.uneDate
    FROM Comptage_velo c2
    WHERE c1.unCompteur = c2.unCompteur
) AND NOT EXISTS(
    SELECT c2.uneDate
    FROM Comptage_velo c2
    WHERE c1.unCompteur = c2.unCompteur
    EXCEPT
    SELECT date
    FROM Date
    WHERE jour = 6 OR jour = 7
);
/*
 0 tuple trouvé
 */

-- 17) VUE des compteurs avec des données négatifs enregistrés
CREATE OR REPLACE VIEW vue_nbVeloNegatif
AS
SELECT unCompteur, nombresVelos
FROM Comptage_velo
WHERE nombresVelos < 0;

SELECT * FROM vue_nbVeloNegatif;
/*
    unCompteur  nombresVelos
    674         -6
    674         -4
    675         -6
    675         -4
    682         -2

    14 Tuples sélectionnés
 */

-- 18) VUE des quartiers sans compteur
CREATE OR REPLACE VIEW vue_quartiersSansCompteur
AS
SELECT DISTINCT idQuartier
FROM Quartiers
WHERE idQuartier NOT IN (
    SELECT DISTINCT unQuartier
    FROM Compteurs
);

SELECT * FROM vue_quartiersSansCompteur;
/*
 idQuartier
 2
 7
 9
 14301
 14302

 8 tuples sélectionnés
 */

-- 19) Moyenne du nombre de vélos par quartier
CREATE OR REPLACE VIEW vue_moyenneVeloQuartier
AS
SELECT unQuartier, AVG(nombresVelos) moyenneVelo
FROM Comptage_Velo
JOIN Compteurs ON unCompteur = idCompteur
GROUP BY unQuartier;

SELECT * FROM vue_moyenneVeloQuartier;
/*
 unQuartier     moyenneVelo
 1              817.2884
 3              759.2041
 4              484.1551
 5              260.4598
 6              911.0991

 9 Tuples sélectionnés
 */

-- 20) Taille totale piste cyclable
CREATE OR REPLACE VIEW vue_totalAmenagementCyclable
AS
SELECT SUM(amenagementCyclable) tailleTotale
FROM Quartiers;

SELECT * FROM vue_totalAmenagementCyclable;
/*
 tailleTotale
 329131.51416015625

 1 Tuple sélectionné
 */
