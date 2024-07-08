DROP TABLE IF EXISTS Skupina;
DROP TABLE IF EXISTS Priorita;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS Oddeleni;
DROP TABLE IF EXISTS Uzivatel;
DROP TABLE IF EXISTS Prispevek;
DROP TABLE IF EXISTS Sprava_skupin;
DROP TABLE IF EXISTS PrispevekSkupina;
DROP TABLE IF EXISTS PrispevekOddeleni;
DROP TABLE IF EXISTS PrispevekRole;
CREATE TABLE "Skupina" (
	"skupina_id"	INTEGER NOT NULL,
	"nazev"	TEXT NOT NULL,
    "id_vedouci" INTEGER,
    "oddeleni_id" INTEGER,
	PRIMARY KEY("skupina_id"),
    FOREIGN KEY (oddeleni_id) REFERENCES Oddeleni(oddeleni_id)
);

CREATE TABLE "Priorita" (
	"priorita_id"	INTEGER NOT NULL,
	"uroven"	INTEGER NOT NULL,
	PRIMARY KEY("priorita_id" AUTOINCREMENT)
);

CREATE TABLE "Role" (
	"role_id"	INTEGER NOT NULL,
	"nazev"	INTEGER,
	PRIMARY KEY("role_id" AUTOINCREMENT)
);
CREATE TABLE "PrispevekRole"(
    "id_ro_prispevku" INTEGER NOT NULL PRIMARY KEY ,
    role_id INTEGER,
    prispevek_id INTEGER,
    FOREIGN KEY(prispevek_id) REFERENCES Prispevek(prispevek_id),
    FOREIGN KEY(role_id) REFERENCES Role(Role_id)

);

CREATE TABLE "Oddeleni" (
	"oddeleni_id"	INTEGER NOT NULL,
	"nazev"	INTEGER NOT NULL,
    "id_vedouci" INTEGER,
	PRIMARY KEY("oddeleni_id" AUTOINCREMENT)
);
CREATE TABLE "Uzivatel" (
	"uzivatel_id"	INTEGER NOT NULL,
	"jmeno"	TEXT NOT NULL,
    "prijmeni" TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"heslo"	TEXT NOT NULL,
	"foto"	BLOB,
	"role_id"	INTEGER DEFAULT 1,
	"oddeleni_id"	INTEGER DEFAULT 1,
    "skupina_id" integer DEFAULT 1,
	PRIMARY KEY("uzivatel_id" AUTOINCREMENT),
	FOREIGN KEY (role_id) REFERENCES Role(role_id),
	FOREIGN KEY (oddeleni_id) REFERENCES Oddeleni(oddeleni_id),
    FOREIGN KEY (skupina_id) REFERENCES Skupina(skupina_id)
);
CREATE TABLE "Prispevek" (
	"prispevek_id"	INTEGER NOT NULL,
	"datum" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "obsah" TEXT,
	"viditelnost_id"	INTEGER,
	"uzivatel_id"	INTEGER,
	"priorita_id"	INTEGER,
    "delka_priority" INTEGER DEFAULT 0,
    "budouci_datum" TIMESTAMP,
    "pro_vedouci" BOOLEAN DEFAULT FALSE,
	PRIMARY KEY("prispevek_id" AUTOINCREMENT),
	FOREIGN KEY("uzivatel_id") REFERENCES Uzivatel (uzivatel_id),
    FOREIGN KEY("viditelnost_id") REFERENCES PrispevekSkupina (id_sk_prispevku),
	FOREIGN KEY ("priorita_id") REFERENCES Priorita(priorita_id)
);
CREATE TABLE "Sprava_skupin" (
	"skupina_id"	INTEGER,
	"uzivatel_id"	INTEGER,
	PRIMARY KEY("skupina_id","uzivatel_id"),
	FOREIGN KEY("uzivatel_id") REFERENCES Uzivatel(uzivatel_id) ,
	FOREIGN KEY("skupina_id") REFERENCES Skupina(skupina_id)
);

CREATE TABLE PrispevekSkupina (
    id_sk_prispevku INTEGER PRIMARY KEY,
    prispevek_id INTEGER,
    skupina_id INTEGER,
    FOREIGN KEY(prispevek_id) REFERENCES Prispevek(prispevek_id),
    FOREIGN KEY(skupina_id) REFERENCES Skupina(skupina_id)
);
CREATE TABLE PrispevekOddeleni (
    id_od_prispevku INTEGER PRIMARY KEY,
    prispevek_id INTEGER,
    oddeleni_id INTEGER,
    FOREIGN KEY(prispevek_id) REFERENCES Prispevek(prispevek_id),
    FOREIGN KEY(oddeleni_id) REFERENCES Skupina(skupina_id)
);
INSERT INTO Skupina (nazev) VALUES ('Není přiřazena');
INSERT INTO Skupina (nazev, id_vedouci) VALUES ('Skupina 2', 1);
INSERT INTO Role (nazev) VALUES ('Admin');
INSERT INTO Role (nazev) VALUES ('Manažer');
INSERT INTO Role (nazev) VALUES ('Vedoucí skupiny');
INSERT INTO Role (nazev) VALUES ('Pracovník');
INSERT INTO Oddeleni (nazev) VALUES ('Není přiřazeno');
INSERT INTO Uzivatel (jmeno, prijmeni, email, heslo, role_id) VALUES ('manazer', 'ultra', 'manazer@gmail.com', '5577c41466556d5ac78fbbbc6fa7570b8b358c4810edb67f2a621e52d2aa097e', 1);
INSERT INTO Uzivatel (jmeno, prijmeni, email, heslo, role_id) VALUES ('Kristián', 'Tihon', 'tihon.kristian@seznam.cz', '5577c41466556d5ac78fbbbc6fa7570b8b358c4810edb67f2a621e52d2aa097e', 1);
INSERT INTO Uzivatel (jmeno, prijmeni, email, heslo, role_id) VALUES ('KristiánX', 'Tihon', 'xtihon@mendelu.cz', '5577c41466556d5ac78fbbbc6fa7570b8b358c4810edb67f2a621e52d2aa097e', 1);
INSERT INTO Uzivatel (jmeno, prijmeni, email, heslo, role_id) VALUES ('Emil', 'Novák', 'vedouci@seznam.cz', '5577c41466556d5ac78fbbbc6fa7570b8b358c4810edb67f2a621e52d2aa097e', 1);
INSERT INTO Uzivatel (jmeno, prijmeni, email, heslo, role_id) VALUES ('Vašek', 'Novotný', 'pracovnikk@seznam.cz', '5577c41466556d5ac78fbbbc6fa7570b8b358c4810edb67f2a621e52d2aa097e', 1);
INSERT INTO Uzivatel (jmeno, prijmeni, email, heslo, role_id) VALUES ('Veronika', 'Kalášková', 'veronika.kalaskova@seznam.cz', '5577c41466556d5ac78fbbbc6fa7570b8b358c4810edb67f2a621e52d2aa097e', 1);



