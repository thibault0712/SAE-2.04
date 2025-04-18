/*
 SCHEMA RELATIONNEL
 Comptage_Velo(unCompteur=@Compeurs.idCompteur INT (1), uneDate=@Date.date DATE (1), nombreVelos INT (NN), probalitePresenceAnomalie VARCHAR)
 Compteurs (idCompteur INT (1), unQuartier=@Quartiers.identifiant INT, localisation VARCHAR (NN))
 Quartiers (idQuartier INT (1), nomQuartier VARCHAR (NN), amenagementCyclable FLOAT (NN))
 Date (date DATE (1), jour INT (NN), temperatureMoyenne FLOAT (NN), vacances VARCHAR (NN))

 CONTRAINTES TEXTUELLES
 jour est entre 1 et 7 INCLUS
 amenagementCyclable > 0
 probabilitePresenceAnomalie est soit Fort | Moyen | Faible ou Rien
 */

DROP TABLE IF EXISTS Comptage_Velo;
DROP TABLE IF EXISTS Compteurs;
DROP TABLE IF EXISTS Quartiers;
DROP TABLE IF EXISTS Date;

CREATE TABLE Date (
    date DATE,
    jour INT NOT NULL,
    temperatureMoyenne FLOAT NOT NULL,
    vacances VARCHAR(100),
    CONSTRAINT pk_Date PRIMARY KEY (date)
);

CREATE TABLE Quartiers (
    idQuartier INT,
    nomQuartier VARCHAR(50) NOT NULL,
    amenagementCyclable FLOAT NOT NULL,
    CONSTRAINT pk_Quartiers PRIMARY KEY (idQuartier)
);

CREATE TABLE Compteurs (
    idCompteur INT,
    unQuartier INT,
    localisation VARCHAR(100) NOT NULL,
    CONSTRAINT pk_Compteur PRIMARY KEY (idCompteur),
    CONSTRAINT fk_Quartiers FOREIGN KEY (unQuartier) REFERENCES Quartiers(idQuartier)
);

CREATE TABLE Comptage_Velo (
    unCompteur INT,
    uneDate DATE,
    nombresVelos INT NOT NULL,
    probabilitePresenceAnomalie VARCHAR(50),
    CONSTRAINT pk_comptageVelo PRIMARY KEY (unCompteur, uneDate),
    CONSTRAINT fk_numCompteur FOREIGN KEY (unCompteur) REFERENCES Compteurs(idCompteur),
    CONSTRAINT fk_date FOREIGN KEY (uneDate) REFERENCES Date(date)
);