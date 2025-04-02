DROP TABLE IF EXISTS Comptage_Velo;
DROP TABLE IF EXISTS Compteur;
DROP TABLE IF EXISTS Quartiers;
DROP TABLE IF EXISTS Date;

CREATE TABLE Date (
    date DATE,
    jour INT,
    températureMoyenne FLOAT,
    vacances INT,
    CONSTRAINT pk_Date PRIMARY KEY (date),
    CONSTRAINT ck_Vacances CHECK (vacances IN (0, 1))
);

CREATE TABLE Quartiers (
    identifiant INT,
    nom VARCHAR(50) NOT NULL,
    amenagement_cyclable FLOAT NOT NULL,
    CONSTRAINT pk_Quartiers PRIMARY KEY (identifiant)
);

CREATE TABLE Compteur (
    idCompteur INT,
    idQuartier INT,
    libelle VARCHAR(100) NOT NULL,
    CONSTRAINT pk_Compteur PRIMARY KEY (idCompteur),
    CONSTRAINT fk_Quartiers FOREIGN KEY (idQuartier) REFERENCES Quartiers(identifiant)
);

CREATE TABLE Comptage_Velo (
    num_compteur INT,
    date DATE,
    nombres_velos INT NOT NULL,
    Probabilite_presence_anomalie VARCHAR(50),
    CONSTRAINT pk_Comptage_Velo PRIMARY KEY (num_compteur, date),
    CONSTRAINT fk_num_compteur FOREIGN KEY (num_compteur) REFERENCES Compteur(idCompteur),
    CONSTRAINT fk_date FOREIGN KEY (date) REFERENCES Date(date)
);