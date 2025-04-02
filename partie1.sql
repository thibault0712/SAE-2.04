-- 1) Liste des Quartiers qui possèdent un compteur
SELECT DISTINCT UPPER(nomQuartier) nomQuartier
FROM Quartiers
INNER JOIN Compteurs ON idQuartier = unQuartier;

-- 2) Les jours qui ont exactement le même nombre de vélos
SELECT C1.date Date1, C2.date Date2, C1.nombresVelos
FROM Comptage_Velo C1
JOIN Comptage_Velo C2 ON C1.nombresVelos = C2.nombresVelos;

-- 3) 

-- 4) 

-- 5) 

-- 6) 

-- 7) 

-- 8) 

-- 9) 

-- 10) 

-- 11) 

