-- Nombre total de données sans anomalies
-- Note : on ne fait pas COUNT(probabilitePresenceAnomalie) car la ligne est tout le temps NULL
SELECT COUNT(*) totalSansAnomalie
FROM Comptage_velo
WHERE probabilitePresenceAnomalie IS NULL;

-- Nombre total de vélo
SELECT SUM(nombresVelos) totalVelo
FROM Comptage_velo;

-- Nombre total de vélo par date
SELECT date, SUM(nombresVelos) totalVelo
FROM Comptage_velo
GROUP BY Date;

-- Nombre total de compteurs par quartier
SELECT idQuartier, nomQuartier, COUNT(idCompteur) totalCompteur
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
GROUP BY idQuartier;

-- Les quartiers qui ont au moins 3 Compteurs
SELECT idQuartier, nomQuartier, COUNT(idCompteur) totalCompteur
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
GROUP BY idQuartier
HAVING COUNT(idCompteur) >= 3;

-- Les quartiers ayant eu au moins 500 vélos au total
SELECT idQuartier, nomQuartier, SUM(nombresVelos)
FROM Quartiers
JOIN Compteurs ON idQuartier = unQuartier
JOIN Comptage_velo ON idCompteur = unCompteur
GROUP BY idQuartier
HAVING SUM(nombresVelos) >= 500;

/*
-------------------------------------------------------------------------
TODO DIVISION
-------------------------------------------------------------------------
*/

-- Jour de la semaine qui n'existe pas
CREATE OR REPLACE VIEW vue_jourSemaineImpossible
AS
SELECT date, jour
FROM Date
WHERE jour > 7 OR jour < 1;

SELECT * FROM vue_jourSemaineImpossible;

-- Nom probabilité anomalie inconnue
CREATE OR REPLACE VIEW vue_nomProbabilitéInconnue
AS
SELECT unCompteur, date, UPPER(probabilitePresenceAnomalie)
FROM Comptage_velo
WHERE UPPER(probabilitePresenceAnomalie) NOT IN ('FORT', 'MOYEN', 'FAIBLE', NULL);

SELECT * FROM vue_nomProbabilitéInconnue;

-- Moyenne du nombre de vélo par quartier
CREATE OR REPLACE VIEW vue_moyenneVeloQuartier
AS
SELECT AVG(nombresVelos) AS moyenneVelo, unQuartier
FROM Comptage_Velo
JOIN Compteurs ON unCompteur = idCompteur
GROUP BY unQuartier;

-- Le nombre total de piste cyclable
CREATE OR REPLACE VIEW vue_totalAmenagementCyclable
AS
SELECT SUM(amenagementCyclable)
FROM Quartiers;

SELECT * FROM vue_totalAmenagementCyclable;