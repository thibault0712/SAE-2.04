DROP TABLE IF EXISTS Comptage_Velo;
DROP TABLE IF EXISTS Compteurs;
DROP TABLE IF EXISTS Quartiers;
DROP TABLE IF EXISTS Date;

CREATE TABLE Date (
    date DATE,
    jour INT,
    températureMoyenne FLOAT,
    vacances VARCHAR(100),
    CONSTRAINT pk_Date PRIMARY KEY (date),
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
    date DATE,
    nombresVelos INT NOT NULL,
    probabilitePresenceAnomalie VARCHAR(50),
    CONSTRAINT pk_comptageVelo PRIMARY KEY (numCompteur, date),
    CONSTRAINT fk_numCompteur FOREIGN KEY (numCompteur) REFERENCES Compteurs(idCompteur),
    CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES Date(date)
);