-- 1) Liste des Quartiers qui possèdent un compteur
SELECT DISTINCT UPPER(nomQuartier) nomQuartier
FROM Quartiers
INNER JOIN Compteurs ON idQuartier = unQuartier;

-- 2) Les jours qui ont exactement le même nombre de vélos
SELECT C1.uneDate Date1, C2.uneDate Date2, C1.nombresVelos
FROM Comptage_Velo C1
JOIN Comptage_Velo C2 ON C1.nombresVelos = C2.nombresVelos;

-- 3) Les paires de dates distinctes où le même nombre de vélos a été compté
SELECT DISTINCT C1.uneDate Date1, C2.uneDate Date2, C1.nombresVelos
FROM Comptage_Velo C1
LEFT JOIN Comptage_Velo C2 ON C1.nombresVelos = C2.nombresVelos AND C1.uneDate <> C2.uneDate;

-- 4) Lister toutes les dates de comptage
SELECT Date.date, Date.jour, Comptage_Velo.nombresVelos, Comptage_Velo.probabilitePresenceAnomalie
FROM Date
RIGHT JOIN Comptage_Velo ON Date.date = Comptage_Velo.uneDate;

-- 5) Tous les quartiers qui n'ont pas de compteur
SELECT idQuartier
FROM Quartiers
WHERE idQuartier NOT IN (
    SELECT DISTINCT unQuartier
    FROM Compteurs
    );


-- 6) Le nombre de vélo par compteur pris en compte uniquement le lundi
SELECT unCompteur, uneDate, nombresVelos
FROM Comptage_velo
WHERE uneDate IN (
    SELECT date
    FROM Date
    WHERE jour = 1
    );


-- 7) Les compteurs qui ne sont pas utilisés pour relever de l'information
SELECT idCompteur
FROM Compteurs
WHERE NOT EXISTS(
    SELECT unCompteur
    FROM comptage_velo
    WHERE unCompteur = idCompteur
);

-- 8) Les dates en vacances où des données ont été enregistré
SELECT date
FROM Date
WHERE vacances != 'Hors Vacances'
AND EXISTS(
    SELECT uneDate
    FROM Comptage_velo
    WHERE uneDate = date
);

-- 9) Nombre total de données sans anomalies
-- Note : on ne fait pas COUNT(probabilitePresenceAnomalie) car la ligne est tout le temps NULL
SELECT COUNT(*) totalSansAnomalie
FROM Comptage_velo
WHERE probabilitePresenceAnomalie IS NULL;

-- 10) Nombre total de vélo
SELECT SUM(nombresVelos) totalVelo
FROM Comptage_velo;

-- 11) Nombre total de vélo par date
SELECT uneDate, SUM(nombresVelos) totalVelo
FROM Comptage_velo
GROUP BY uneDate;

-- 12) Nombre total de compteurs par quartier
SELECT idQuartier, nomQuartier, COUNT(idCompteur) totalCompteur
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
GROUP BY idQuartier;

-- 13) Les quartiers qui ont au moins 3 Compteurs
SELECT idQuartier, nomQuartier, COUNT(idCompteur) totalCompteur
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
GROUP BY idQuartier
HAVING COUNT(idCompteur) >= 3;

-- 14) Les quartiers ayant eu au moins 500 vélos au total
SELECT idQuartier, nomQuartier, SUM(nombresVelos)
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
JOIN Comptage_velo ON idCompteur = unCompteur
GROUP BY idQuartier
HAVING SUM(nombresVelos) >= 500;

/* 15 et 16
-------------------------------------------------------------------------
TODO DIVISION
-------------------------------------------------------------------------
*/

-- 17) Jour de la semaine qui n'existe pas
CREATE OR REPLACE VIEW vue_jourSemaineImpossible
AS
SELECT date, jour
FROM Date
WHERE jour > 7 OR jour < 1;

SELECT * FROM vue_jourSemaineImpossible;

-- 18) Nom probabilité anomalie inconnue
CREATE OR REPLACE VIEW vue_nomProbabilitéInconnue
AS
SELECT unCompteur, uneDate, UPPER(probabilitePresenceAnomalie)
FROM Comptage_velo
WHERE UPPER(probabilitePresenceAnomalie) NOT IN ('FORT', 'MOYEN', 'FAIBLE', NULL);

SELECT * FROM vue_nomProbabilitéInconnue;

-- 19) Moyenne du nombre de vélo par quartier
CREATE OR REPLACE VIEW vue_moyenneVeloQuartier
AS
SELECT AVG(nombresVelos) AS moyenneVelo, unQuartier
FROM Comptage_Velo
JOIN Compteurs ON unCompteur = idCompteur
GROUP BY unQuartier;

-- 20) Le nombre total de pistes cyclable
CREATE OR REPLACE VIEW vue_totalAmenagementCyclable
AS
SELECT SUM(amenagementCyclable)
FROM Quartiers;

SELECT * FROM vue_totalAmenagementCyclable;
