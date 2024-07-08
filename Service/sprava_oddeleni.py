
from database.database import get_db
from Service.sprava_skupin import SpravaSkupin
class SpravaOddeleni:

    @staticmethod
    def jemanazer(email):
        db = get_db()
        uzivatel = db.execute("SELECT role_id FROM Uzivatel WHERE email=?", (email,)).fetchone()
        if uzivatel['role_id'] == 2:
            return False
        else:
            return True
    @staticmethod
    def insert_oddeleni(nazev, email):
        db = get_db()
        cursor = db.cursor()
        id_vedouci =db.execute("SELECT uzivatel_id FROM Uzivatel WHERE email=?", (email,)).fetchone()
        id_vedouci = id_vedouci['uzivatel_id']

        cursor.execute('INSERT INTO Oddeleni (nazev,id_vedouci) VALUES (?,?)', [nazev,id_vedouci])
        oddeleni_id = cursor.lastrowid
        cursor.execute('UPDATE Uzivatel SET role_id=2, oddeleni_id=? WHERE email=?', [oddeleni_id, email])
        db.commit()
        cursor.close()

    @staticmethod
    def vypis_oddeleni():
        db = get_db()
        sql = (
            "SELECT o.nazev, u.jmeno, u.prijmeni, o.oddeleni_id "
            "FROM Oddeleni o "
            "JOIN Uzivatel u ON o.oddeleni_id = u.oddeleni_id "
            "WHERE o.oddeleni_id != 1 AND u.role_id <=2 "
        )
        return db.execute(sql).fetchall()

    @staticmethod
    def get_all_oddeleni():
        db = get_db()
        sql = ("SELECT * FROM Oddeleni")
        return db.execute(sql).fetchall()

    @staticmethod
    def smaz_oddeleni(oddeleni_id):
        db = get_db()
        skupina_id = db.execute("SELECT skupina_id FROM Skupina WHERE oddeleni_id =?", (oddeleni_id,)).fetchone()
        skupina_id = skupina_id['skupina_id']
        prispevek_id = db.execute("SELECT prispevek_id FROM PrispevekOddeleni WHERE oddeleni_id =?",
                                  (oddeleni_id,)).fetchall()

        for prispevek in prispevek_id:
            prispevek_id = prispevek['prispevek_id']
            prispevek_id = int(prispevek_id)
            db.execute("DELETE FROM PrispevekOddeleni WHERE prispevek_id = ?", (prispevek_id,))
        SpravaSkupin.smaz_skupinu(skupina_id)
        db.execute("UPDATE Uzivatel SET oddeleni_id =1 WHERE oddeleni_id =?", (oddeleni_id,))
        sql = "DELETE FROM Oddeleni WHERE oddeleni_id = ?"
        db.execute(sql, (oddeleni_id,))
        db.commit()