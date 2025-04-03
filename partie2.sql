-- Nom probabilité anomalie inconnue
CREATE OR REPLACE VIEW vue_nomProbabilitéInconnue
AS
SELECT unCompteur, date, UPPER(probabilitePresenceAnomalie)
FROM Comptage_velo
WHERE UPPER(probabilitePresenceAnomalie) NOT IN ('FORT', 'MOYEN', 'FAIBLE')
AND probabilitePresenceAnomalie IS NOT NULL;

-- Moyenne du nombre de vélo par quartier
CREATE OR REPLACE VIEW vue_moyenneVeloQuartier
AS
SELECT AVG(nombresVelos) AS moyenneVelo, unQuartier
FROM Comptage_Velo
JOIN Compteurs ON idCompteur = unCompteur
JOIN Quartiers ON idQuartier = unQuartier
GROUP BY unQuartier;

SELECT * FROM vue_moyenneVeloQuartier;

-- Le nombre total de piste cyclable
CREATE OR REPLACE VIEW vue_totalAmenagementCyclable
AS
SELECT SUM(amenagementCyclable)
FROM Quartiers;

SELECT * FROM vue_totalAmenagementCyclable;