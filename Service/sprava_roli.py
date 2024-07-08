
from database.database import get_db

class SpravaRoli:

    @staticmethod
    def vypis_role():
        db = get_db()
        sql = ("SELECT * FROM Role")
        return db.execute(sql).fetchall()
