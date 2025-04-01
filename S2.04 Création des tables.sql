DROP TABLE IF EXISTS Comptage_Velo;
DROP TABLE IF EXISTS Compteur;
DROP TABLE IF EXISTS Quartiers;
DROP TABLE IF EXISTS Date;

CREATE TABLE Date (
    date DATE,
    jour INT,
    temperatureMoyenne FLOAT,
    vacances INT(1),
    CONSTRAINT pk_Date PRIMARY KEY (date),
    CONSTRAINT ck_Vacances CHECK (vacances IN (0, 1))
);

CREATE TABLE Quartiers (
    idQuartier INT,
    nomQuartiers VARCHAR(50) NOT NULL,
    amenagementCyclable FLOAT NOT NULL,
    CONSTRAINT pk_Quartiers PRIMARY KEY (idQuartier)
);

CREATE TABLE Compteurs (
    idCompteur INT,
    idQuartier INT,
    localisation VARCHAR(100) NOT NULL,
    CONSTRAINT pk_Compteur PRIMARY KEY (idCompteur),
    CONSTRAINT fk_Quartiers FOREIGN KEY (idQuartier) REFERENCES Quartiers(identifiant)
);

CREATE TABLE Comptage_Velo (
    numCompteur INT,
    date DATE,
    nombresVelos INT NOT NULL,
    probabilitePresenceAnomalie VARCHAR(50),
    CONSTRAINT pk_comptageVelo PRIMARY KEY (numCompteur, date),
    CONSTRAINT fk_numCompteur FOREIGN KEY (numCompteur) REFERENCES Compteur(idCompteur),
    CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES Date(date)
);