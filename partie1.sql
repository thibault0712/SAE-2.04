-- 1) Liste des Quartiers qui possèdent un compteur
SELECT DISTINCT UPPER(nomQuartier) nomQuartier
FROM Quartiers
INNER JOIN Compteurs ON idQuartier = unQuartier;

-- 2) Les jours qui ont exactement le même nombre de vélos
SELECT C1.date Date1, C2.date Date2, C1.nombresVelos
FROM Comptage_Velo C1
JOIN Comptage_Velo C2 ON C1.nombresVelos = C2.nombresVelos;

-- 3) Les paires de dates distinctes où le même nombre de vélos a été compté
SELECT DISTINCT C1.date Date1, C2.date Date2, C1.nombresVelos
FROM Comptage_Velo C1
LEFT JOIN Comptage_Velo C2 ON C1.nombresVelos = C2.nombresVelos AND C1.date <> C2.date;

-- 4) Lister toutes les dates de comptage
SELECT 
    Date.date,
    Date.jour,
    Comptage_Velo.nombresVelos,
    Comptage_Velo.probabilitePresenceAnomalie
FROM 
    Date
RIGHT JOIN 
    Comptage_Velo
ON 
    Date.date = Comptage_Velo.date;

-- 5) 


-- 6) 


-- 7) 


-- 8) 


-- 9) 


-- 10) 


-- 11) 

