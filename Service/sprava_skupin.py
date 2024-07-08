from database.database import get_db

class SpravaSkupin:
    @staticmethod
    def jevedouci(email):
        db = get_db()
        uzivatel = db.execute("SELECT role_id FROM Uzivatel WHERE email=?", (email,)).fetchone()
        if uzivatel['role_id']==3:
            return False
        else:
            return True
    @staticmethod
    def kontrola_email(email):
        db=get_db()

        uzivatel =db.execute("SELECT uzivatel_id FROM Uzivatel WHERE email=?", (email,)).fetchone()
        if uzivatel:
            return True
        else:
            return False
    @staticmethod
    def insert_skupina(nazev, email,id_oddeleni):
        db = get_db()
        cursor = db.cursor()
        id_vedouci = db.execute("SELECT uzivatel_id FROM Uzivatel WHERE email=?", (email,)).fetchone()
        id_vedouci = id_vedouci['uzivatel_id']
        cursor.execute('INSERT INTO Skupina (nazev,id_vedouci,oddeleni_id) VALUES (?,?,?)', [nazev,id_vedouci,id_oddeleni])
        skupina_id = cursor.lastrowid
        db.commit()
        id_oddeleni = db.execute("SELECT oddeleni_id FROM Skupina WHERE skupina_id=?", (skupina_id,)).fetchone()
        id_oddeleni = id_oddeleni['oddeleni_id']
        cursor.execute('UPDATE Uzivatel SET role_id=3, skupina_id=?,oddeleni_id=? WHERE email=?', [skupina_id,id_oddeleni, email])
        db.commit()
        cursor.close()

    @staticmethod
    def vypis_skupiny():
        db = get_db()

        sql = (
            "SELECT s.nazev, u.jmeno, u.prijmeni, s.skupina_id,o.nazev "
            "FROM Skupina s "
            "JOIN Uzivatel u ON s.skupina_id = u.skupina_id "
            "JOIN Oddeleni o on s.oddeleni_id = o.oddeleni_id "
            "WHERE s.skupina_id != 1 AND u.role_id =3"
        )
        return db.execute(sql).fetchall()

    @staticmethod
    def get_all_skupina():
        db = get_db()
        sql = ("SELECT * FROM Skupina")
        return db.execute(sql).fetchall()


    @staticmethod
    def smaz_skupinu(skupina_id):
        db = get_db()

        db.execute("UPDATE Uzivatel SET skupina_id =1,role_id =4,oddeleni_id =1 WHERE skupina_id =?", (skupina_id,))
        prispevek_id = db.execute("SELECT prispevek_id FROM PrispevekSkupina WHERE skupina_id =?", (skupina_id,)).fetchall()


        for prispevek in prispevek_id:
            prispevek_id= prispevek['prispevek_id']
            prispevek_id=int(prispevek_id)
            db.execute("DELETE FROM PrispevekSkupina WHERE prispevek_id = ?", (prispevek_id,))
        sql = "DELETE FROM Skupina WHERE skupina_id = ?"
        db.execute(sql,(skupina_id,))
        db.commit()