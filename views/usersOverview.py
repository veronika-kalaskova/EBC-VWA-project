from flask import Blueprint, render_template, redirect, url_for, request
from Service.sprava_uzivatelu import SpravaUzivatelu
import auth
usersOverview = Blueprint('users-overview', __name__)


@usersOverview.route("/",)
@auth.login_required
def view_users_overview():
    uzivatele = SpravaUzivatelu.vypis_uzivatele()
    uzivatele_prvky =[]
    for uzivatel in uzivatele:
        uzivatele_dict = {
            "jmeno": uzivatel[0],
            "prijmeni": uzivatel[1],
            "skupina_nazev": uzivatel[2],
            "role_nazev": uzivatel[3],
            "oddeleni_nazev": uzivatel[4],
            "uzivatel_id":uzivatel[5],
            "foto":uzivatel[6]
        }
        uzivatele_prvky.append(uzivatele_dict)
    return render_template("users-overview/users-overview.jinja", uzivatele=uzivatele_prvky)

@usersOverview.route('/', methods=['POST'])
def smazat_uzivatele():
    id_uzivatele = request.form.get('id_uzivatele')
    SpravaUzivatelu.smaz_uzivatele(id_uzivatele)
    return redirect(url_for('users-overview.view_users_overview'))