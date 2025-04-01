-- Liste des Quartiers qui possèdent un compteur
SELECT DISTINCT UPPER(nomQuartiers)
FROM Quartiers
INNER JOIN Compteur ON idQuartier = identifiant;

-- Les jours qui ont exactement le même nombre de vélo
SELECT C1.une_date Date1, C2.une_date Date2, C1.nombres_velos
FROM Comptage_Velo C1
JOIN Comptage_Velo C2 ON C1.nombres_velos = C2.nombres_velos;