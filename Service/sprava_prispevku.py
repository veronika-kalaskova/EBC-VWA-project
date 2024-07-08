from database.database import get_db
from datetime import datetime, timedelta

class SpravaPrispevku:


    @staticmethod
    def vypis_prispevky_vedouci(skupina,role):
        db = get_db()
        sql = ("SELECT * FROM Uzivatel u"
               " JOIN Prispevek p ON u.uzivatel_id = p.uzivatel_id"
               " LEFT JOIN PrispevekSkupina ps ON p.prispevek_id = ps.prispevek_id"
               " LEFT JOIN Skupina s ON ps.skupina_id = s.skupina_id"
                " LEFT JOIN PrispevekRole pr ON p.prispevek_id=pr.prispevek_id"
                " LEFT JOIN Role r on pr.role_id=r.role_id"
               " WHERE s.nazev=? OR p.pro_vedouci=TRUE OR r.nazev=?"
               " GROUP BY p.prispevek_id"
               " ORDER BY p.priorita_id DESC, p.prispevek_id DESC LIMIT 30")
        params = (skupina,role,)

        return db.execute(sql, params).fetchall()
    @staticmethod
    def pridej_prispevek_vedouci(obsah, email):
        db = get_db()

        uzivatel = db.execute('SELECT uzivatel_id, skupina_id FROM Uzivatel WHERE email = ?', [email]).fetchone()

        if uzivatel:
            uzivatel_id = uzivatel['uzivatel_id']
            skupina_id = uzivatel['skupina_id']
            if uzivatel_id is not None and skupina_id is not None:
                db.execute(
                    'INSERT INTO Prispevek (obsah, uzivatel_id,pro_vedouci) VALUES (?, ?,TRUE)',
                    [obsah, uzivatel_id]
                )
                db.commit()
    @staticmethod
    def smaz_prispevek(id_prispevku):
        db = get_db()
        sql = "DELETE FROM Prispevek WHERE prispevek_id = ?"
        db.execute(sql, (id_prispevku,))
        db.commit()

    @staticmethod
    def vypis_prispevky(skupina,role):
        db = get_db()
        sql = (" SELECT u.foto, u.jmeno, u.prijmeni, p.prispevek_id, p.obsah, p.priorita_id,s.nazev,p.delka_priority "
                 "FROM Uzivatel u"
                 " JOIN Prispevek p ON u.uzivatel_id = p.uzivatel_id"
                 " LEFT JOIN PrispevekSkupina ps ON p.prispevek_id = ps.prispevek_id"
                 " LEFT JOIN Skupina s ON ps.skupina_id = s.skupina_id"
                 " LEFT JOIN PrispevekRole pr ON p.prispevek_id=pr.prispevek_id"
                 " LEFT JOIN Role r on pr.role_id=r.role_id"
                 " WHERE s.nazev=  ? OR r.nazev = ?"
                 " GROUP BY p.prispevek_id"
                 " ORDER BY p.priorita_id DESC, p.prispevek_id DESC"
                 " LIMIT 30")
        params = (skupina,role)


        vysledek = db.execute(sql, params).fetchall()
        return vysledek

    @staticmethod
    def vypis_prispevky_manazer(oddeleni,email,role):
        db = get_db()
        oddeleni_id= db.execute("SELECT oddeleni_id FROM Oddeleni WHERE nazev = ?", (oddeleni,)).fetchone()
        uzivatel = db.execute('SELECT uzivatel_id FROM Uzivatel WHERE email = ?', [email]).fetchone()
        uzivatel_id = uzivatel['uzivatel_id']
        oddeleni_id= oddeleni_id['oddeleni_id']
        vysledky=[]
        videna_id = set()
        skupiny = db.execute("SELECT nazev FROM Skupina WHERE oddeleni_id = ?", (oddeleni_id,)).fetchall()
        for skupina in skupiny:
            skupina= skupina['nazev']
            sql = ("SELECT * FROM Uzivatel u "
               " JOIN Prispevek p ON u.uzivatel_id = p.uzivatel_id"
               " LEFT JOIN PrispevekSkupina ps ON p.prispevek_id = ps.prispevek_id"
               " LEFT JOIN Skupina s ON ps.skupina_id = s.skupina_id"
               " LEFT JOIN PrispevekOddeleni po ON p.prispevek_id = po.prispevek_id"
               " LEFT JOIN Oddeleni o on po.oddeleni_id= o.oddeleni_id"
             " LEFT JOIN PrispevekRole pr ON p.prispevek_id=pr.prispevek_id"
                 " LEFT JOIN Role r on pr.role_id=r.role_id"
               " WHERE o.nazev=? OR p.uzivatel_id =? OR r.nazev=?"
               " GROUP BY p.prispevek_id"
               " ORDER BY p.priorita_id DESC, p.prispevek_id DESC LIMIT 30")
            params = (oddeleni,uzivatel_id,role)
            vysledky_skupin =(db.execute(sql, params).fetchall())

            for prispevek in vysledky_skupin:
                prispevek_id = prispevek['prispevek_id']
                if prispevek_id not in videna_id:
                    videna_id.add(prispevek_id)
                    vysledky.append(prispevek)
        return vysledky

    @staticmethod
    def pridej_prispevek_firemni(obsah, priorita, email):
        db = get_db()

        uzivatel = db.execute('SELECT uzivatel_id,skupina_id FROM Uzivatel WHERE email = ?', [email]).fetchone()

        if uzivatel:
            uzivatel_id = uzivatel['uzivatel_id']

            db.execute(
                    'INSERT INTO Prispevek ( obsah, uzivatel_id, delka_priority) VALUES ( ?, ?, ?)',
                    [obsah, uzivatel_id, priorita]
                )
        db.commit()
        id_prispevku = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        skupina_id = uzivatel['skupina_id']
        db.execute('INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)', [id_prispevku, skupina_id])
        db.commit()
        id_oddeleni = db.execute("SELECT oddeleni_id FROM Oddeleni WHERE nazev='Firemní'").fetchone()
        id_oddeleni = id_oddeleni['oddeleni_id']
        db.execute('INSERT INTO PrispevekOddeleni (prispevek_id, oddeleni_id) VALUES (?,?)', [id_prispevku, id_oddeleni])
        skupiny_id = db.execute("SELECT skupina_id skupina_id FROM Skupina WHERE oddeleni_id = ?", (id_oddeleni,))
        for skupina_id in skupiny_id:
            skupina_id = skupina_id['skupina_id']
            skupina_id = int(skupina_id)
            db.execute('INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)',
                       [id_prispevku, skupina_id, ])
        db.commit()
        db.commit()

    @staticmethod
    def pridej_prispevek(obsah, priorita, email, skupiny):
        db = get_db()
        uzivatel = db.execute('SELECT uzivatel_id,skupina_id,oddeleni_id FROM Uzivatel WHERE email = ?', [email]).fetchone()
        if uzivatel:
            uzivatel_id = uzivatel['uzivatel_id']
            db.execute(
                    'INSERT INTO Prispevek ( obsah, uzivatel_id, delka_priority) VALUES ( ?, ?, ?)',
                    [obsah, uzivatel_id, priorita]
                )
        db.commit()
        id_prispevku = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        skupina_id = uzivatel['skupina_id']
        db.execute('INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)', [id_prispevku, skupina_id])
        db.commit()
        uzivatel_od = uzivatel['oddeleni_id']
        id_oddeleni=int(uzivatel_od)
        db.execute('INSERT INTO PrispevekOddeleni (prispevek_id, oddeleni_id) VALUES (?,?)',
                   [id_prispevku, id_oddeleni])
        db.commit()
        for skupina_id in skupiny:
            skupina_id = int(skupina_id)
            db.execute(
                'INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)',
                [id_prispevku, skupina_id]
            )
            db.commit()


    @staticmethod
    def pridej_prispevek_oddeleni(obsah, priorita, email,oddeleni):
            db = get_db()
            uzivatel = db.execute('SELECT uzivatel_id,oddeleni_id,skupina_id FROM Uzivatel WHERE email = ?', [email]).fetchone()
            if uzivatel:
                uzivatel_id = uzivatel['uzivatel_id']

                db.execute(
                        'INSERT INTO Prispevek ( obsah, uzivatel_id, delka_priority) VALUES ( ?, ?, ?)',
                        [obsah, uzivatel_id, priorita]
                    )

            db.commit()
            id_prispevku = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            skupina_id = uzivatel['skupina_id']
            db.execute('INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)',
                       [id_prispevku, skupina_id])
            db.commit()
            uzivatel_od = uzivatel['oddeleni_id']
            db.execute('INSERT INTO PrispevekOddeleni (prispevek_id, oddeleni_id) VALUES (?,?)',
                       [id_prispevku, uzivatel_od])
            db.commit()
            for oddeleni_id in oddeleni:
                oddeleni_id = int(oddeleni_id)
                db.execute(
                    'INSERT INTO PrispevekOddeleni (prispevek_id, oddeleni_id) VALUES (?,?)',
                    [id_prispevku, oddeleni_id]
                )
                skupiny_id= db.execute("SELECT skupina_id skupina_id FROM Skupina WHERE oddeleni_id = ?", (oddeleni_id,))
                for skupina_id in skupiny_id:
                    skupina_id = skupina_id['skupina_id']
                    skupina_id = int(skupina_id)
                    db.execute('INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)',
                           [id_prispevku,skupina_id,])
                db.commit()
    @staticmethod
    def pridej_prispevek_role(obsah, priorita, email,role):
            db = get_db()

            uzivatel = db.execute('SELECT uzivatel_id,oddeleni_id,skupina_id FROM Uzivatel WHERE email = ?', [email]).fetchone()

            if uzivatel:
                uzivatel_id = uzivatel['uzivatel_id']
                priorita=int(priorita)
                if priorita>0:
                    db.execute(
                    'INSERT INTO Prispevek ( obsah, uzivatel_id, delka_priority,priorita_id) VALUES ( ?, ?, ?,1)',
                    [obsah, uzivatel_id, priorita]
                    )
                else:
                    db.execute(
                        'INSERT INTO Prispevek ( obsah, uzivatel_id, delka_priority) VALUES ( ?, ?, ?)',
                        [obsah, uzivatel_id, priorita]
                    )
            db.commit()
            id_prispevku = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            db.commit()
            for role_id in role:
                role_id = int(role_id)
                db.execute(
                    'INSERT INTO PrispevekRole (prispevek_id, role_id) VALUES (?,?)',
                    [id_prispevku, role_id]
                )
                db.commit()
    @staticmethod
    def nastav_prioritu(priorita):
        if priorita == '1':
                db = get_db()
                posledni = db.execute('SELECT * FROM Prispevek ORDER BY datum DESC LIMIT 1').fetchone()
                if posledni:
                    datum = posledni['datum']
                    budouci_datum = datum + timedelta(days=3)
                    db.execute("UPDATE Prispevek SET budouci_datum = ? WHERE prispevek_id = ?", [budouci_datum, posledni['prispevek_id']])
                    db.commit()
                    db.close()

        if priorita == '2':
            db = get_db()
            posledni = db.execute('SELECT * FROM Prispevek ORDER BY datum DESC LIMIT 1').fetchone()
            if posledni:
                datum = posledni['datum']
                budouci_datum = datum + timedelta(days=2)
                db.execute("UPDATE Prispevek SET budouci_datum = ? WHERE prispevek_id = ?", [budouci_datum, posledni['prispevek_id']])
                db.commit()
                db.close()

        if priorita == '3':
            db = get_db()
            posledni = db.execute('SELECT * FROM Prispevek ORDER BY datum DESC LIMIT 1').fetchone()
            if posledni:
                datum = posledni['datum']
                budouci_datum = datum + timedelta(days=1)
                db.execute("UPDATE Prispevek SET budouci_datum = ? WHERE prispevek_id = ?", [budouci_datum, posledni['prispevek_id']])
                db.commit()
                db.close()

    @staticmethod
    def zkontroluj_prioritu():
        db = get_db()
        prispevky = db.execute("SELECT * FROM Prispevek").fetchall()
        for prispevek in prispevky:
            budouci_datum = prispevek['budouci_datum']
            dnesni_datum_datetime = datetime.now()

            if budouci_datum and dnesni_datum_datetime > budouci_datum:
                print("meni se")
                db.execute("UPDATE Prispevek SET delka_priority = 0 WHERE prispevek_id = ?", [prispevek['prispevek_id']])
                db.commit()

            else:
                print("nemieni")

    @staticmethod
    def pridej_prispevek_voddeleni(obsah, priorita, email):
        db = get_db()
        uzivatel = db.execute('SELECT uzivatel_id,skupina_id,oddeleni_id FROM Uzivatel WHERE email = ?',
                              [email]).fetchone()
        if uzivatel:
            uzivatel_id = uzivatel['uzivatel_id']
            db.execute(
                'INSERT INTO Prispevek ( obsah, uzivatel_id, delka_priority) VALUES ( ?, ?, ?)',
                [obsah, uzivatel_id, priorita]
            )
        db.commit()
        id_prispevku = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        skupina_id = uzivatel['skupina_id']
        db.execute('INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)', [id_prispevku, skupina_id])
        db.commit()
        uzivatel_od = uzivatel['oddeleni_id']
        id_oddeleni = int(uzivatel_od)
        db.execute('INSERT INTO PrispevekOddeleni (prispevek_id, oddeleni_id) VALUES (?,?)',
                   [id_prispevku, id_oddeleni])
        db.commit()
        skupiny=db.execute("SELECT skupina_id FROM Skupina WHERE oddeleni_id=?", [id_oddeleni]).fetchall()
        for skupina_id in skupiny:
            id_skupina = skupina_id['skupina_id']
            id_skupina = int(id_skupina)
            db.execute(
                'INSERT INTO PrispevekSkupina (prispevek_id, skupina_id) VALUES (?,?)',
                [id_prispevku, id_skupina]
            )
            db.commit()


