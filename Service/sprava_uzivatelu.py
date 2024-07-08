import hashlib

from flask import session, flash

from database.database import get_db
import config



class SpravaUzivatelu:
    @staticmethod
    def kontrola(email):
        db = get_db()
        email = db.execute("SELECT email FROM Uzivatel WHERE email =?", [email]).fetchone()
        if email:
            return True
        else:
            return False

    @staticmethod
    def insert_uzivatel(name, prijmeni, email, password, obrazek=None):
        db = get_db()
        hashed_passorwd = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        db.execute(
            'INSERT INTO Uzivatel (jmeno,prijmeni,email,heslo,foto) VALUES (?,?,?,?,?)',
            [name, prijmeni, email, hashed_passorwd.hexdigest(), obrazek]
        )
        db.commit()

    @staticmethod
    def verify(email, password):

        db = get_db()
        hashed_passorwd = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        # print(hashed_passorwd.hexdigest())

        user = db.execute('''
            SELECT u.foto,u.uzivatel_id, u.jmeno, u.prijmeni, u.email, u.heslo, u.role_id, r.nazev role,s.nazev skupina,o.nazev oddeleni
            FROM Uzivatel u JOIN Role r ON (u.role_id=r.role_id)
            JOIN SKupina s on u.skupina_id=s.skupina_id
            JOIN Oddeleni o on u.oddeleni_id=o.oddeleni_id
            WHERE email = ? AND heslo = ?''', [email, hashed_passorwd.hexdigest()]).fetchone()
        if user:
            return user
        else:
            return None

    @staticmethod
    def vypis_uzivatele():
        db = get_db()
        sql = ("SELECT jmeno,prijmeni,skupina.nazev,role.nazev,oddeleni.nazev,uzivatel_id,foto FROM Uzivatel"
               " JOIN Role ON (Uzivatel.role_id=Role.role_id)"
               " JOIN Skupina ON(Uzivatel.skupina_id=Skupina.skupina_id)"
               " JOIN Oddeleni ON (Uzivatel.oddeleni_id=Oddeleni.oddeleni_id) ")
        return db.execute(sql).fetchall()

    @staticmethod
    def smaz_uzivatele(uzivatel_id):
        db = get_db()
        db.execute("DELETE FROM Prispevek where uzivatel_id=?", (uzivatel_id,))

        sql = "DELETE FROM Uzivatel WHERE uzivatel_id = ?"
        db.execute(sql, (uzivatel_id,))
        db.commit()

    @staticmethod
    def vypis_skupiny(oddeleni):
        db = get_db()
        id_oddeleni = db.execute("SELECT oddeleni_id FROM Oddeleni WHERE nazev =?", (oddeleni,)).fetchone()
        if id_oddeleni is not None:
            id_oddeleni=id_oddeleni['oddeleni_id']
            sql = ("SELECT skupina_id, nazev from Skupina WHERE oddeleni_id =?")
            return db.execute(sql,[id_oddeleni]).fetchall()

    @staticmethod
    def udaje_uzivatel(uzivatel_id):
        db = get_db()
        sql = (
            "SELECT foto,jmeno, prijmeni, skupina.nazev skupina, role.nazev role, oddeleni.nazev oddeleni, uzivatel_id, foto FROM Uzivatel"
            " JOIN Role ON (Uzivatel.role_id=Role.role_id)"
            " JOIN Skupina ON (Uzivatel.skupina_id=Skupina.skupina_id)"
            " JOIN Oddeleni ON (Uzivatel.oddeleni_id=Oddeleni.oddeleni_id) "
            " WHERE Uzivatel.uzivatel_id=?"
        )
        return db.execute(sql, (uzivatel_id,)).fetchall()

    @staticmethod
    def edituj_uzivatele(uzivatel_id, role, skupina, oddeleni):
        db = get_db()
        id_oddeleni=db.execute("SELECT oddeleni_id FROM Skupina WHERE skupina_id=?", (skupina,)).fetchone()
        id_oddeleni=id_oddeleni['oddeleni_id']

        role = int(role)
        skupina = int(skupina)

        id_vedouciho_skupiny = db.execute("SELECT id_vedouci FROM Skupina WHERE skupina_id=?", (skupina,)).fetchone()

        if role == 1 and skupina == 1:
            flash("Musí se pro uživatele nastavit skupina")
        elif skupina == 1:
            flash("Musí se pro uživatele nastavit skupina")
        elif (role == 2 or role == 3) and id_vedouciho_skupiny is not None:
            flash("Skupina již má vedoucího")
        else:
            sql = 'UPDATE Uzivatel SET role_id=?, oddeleni_id=?, skupina_id=? WHERE uzivatel_id=?'
            db.execute(sql, [role, id_oddeleni, skupina, uzivatel_id])
            db.commit()
            # SESSION
            role_id = db.execute("SELECT role_id FROM Uzivatel WHERE uzivatel_id=?", (uzivatel_id,)).fetchone()
            role_nazev = db.execute("SELECT nazev FROM Role WHERE role_id=?", (role_id)).fetchone()

            oddeleni_id = db.execute("SELECT oddeleni_id FROM Uzivatel WHERE uzivatel_id=?", (uzivatel_id,)).fetchone()
            oddeleni_nazev = db.execute("SELECT nazev FROM Oddeleni WHERE oddeleni_id=?", (oddeleni_id)).fetchone()

            skupina_id = db.execute("SELECT skupina_id FROM Uzivatel WHERE uzivatel_id=?", (uzivatel_id,)).fetchone()
            skupina_nazev = db.execute("SELECT nazev FROM Skupina WHERE skupina_id=?", (skupina_id)).fetchone()

            if skupina_nazev and oddeleni_nazev and role_nazev is not None:
                session['role_id'] = role_id['role_id']
                session['role'] = role_nazev['nazev']
                session['skupina'] = skupina_nazev['nazev']
                session['oddeleni'] = oddeleni_nazev['nazev']


    @staticmethod
    def edituj_img(uzivatel_id, img):
        db = get_db()
        sql = 'UPDATE Uzivatel SET foto=? WHERE uzivatel_id=?'
        db.execute(sql, [img, uzivatel_id])
        db.commit()

        obrazek = db.execute("SELECT foto FROM Uzivatel WHERE uzivatel_id=?", (uzivatel_id,)).fetchone()

        # Update the role_id in the session
        session['foto'] = obrazek['foto']

    @staticmethod
    def vypis_role():
        db = get_db()
        sql = 'SELECT * FROM Role'
        return db.execute(sql).fetchall()

    @staticmethod
    def vypis_oddeleni():
        db = get_db()
        sql = 'SELECT * FROM Oddeleni WHERE oddeleni_id >1'
        return db.execute(sql).fetchall()

    @staticmethod
    def edituj_heslo(uzivatel_id, heslo):
        db = get_db()
        hashed_passorwd = hashlib.sha256(f'{heslo}{config.PASSWORD_SALT}'.encode())
        sql = 'UPDATE Uzivatel SET heslo=? WHERE uzivatel_id=?'
        db.execute(sql, [hashed_passorwd, uzivatel_id])
        db.commit()
