from flask import Blueprint, render_template, redirect, url_for, request, session
from Service.sprava_uzivatelu import SpravaUzivatelu
import auth
from Service.sprava_prispevku import SpravaPrispevku
homepage = Blueprint('homepage', __name__)


@homepage.route("/")
@auth.login_required
def view_homepage():
    skupina = session.get('skupina')
    role_id = session.get('role_id')
    oddeleni = session.get('oddeleni')
    role=session.get('role')
    email= session.get('email')
    SpravaPrispevku.zkontroluj_prioritu()
    if role=="Vedoucí skupiny":
        prispevky = SpravaPrispevku.vypis_prispevky_vedouci(skupina,role)
        for pridej_prispevek in prispevky:
            pridej_prispevek = pridej_prispevek['obsah']
            print(pridej_prispevek)
        return render_template("homepage/index.jinja", prispevky=prispevky)
    if role_id<=2:

        prispevky = SpravaPrispevku.vypis_prispevky_manazer(oddeleni,email,role)
        skupiny = SpravaUzivatelu.vypis_skupiny(oddeleni)
        role_nazvy = SpravaUzivatelu.vypis_role()
        oddeleni_nazvy = SpravaUzivatelu.vypis_oddeleni()
        return render_template("homepage/index.jinja", prispevky=prispevky, skupiny=skupiny, role=role_nazvy,oddeleni=oddeleni_nazvy)
    else:
        prispevky = SpravaPrispevku.vypis_prispevky(skupina,role)
        return render_template("homepage/index.jinja", prispevky=prispevky)

    # prispevky = SpravaUzivatelu.vypis_prispevky(skupina)
    # prispevky_prvky = []
    # for prispevek in prispevky:
    #     prispevek_dict = {
    #         "jmeno": prispevek[0],
    #         "prijmeni": prispevek[1],
    #         "obsah": prispevek[2],
    #         "id_prispevku": prispevek[3]
    #
    #     }
    #     prispevky_prvky.append(prispevek_dict)


@homepage.route('/', methods=['POST'])
def pridej_prispevek():
    if request.method == 'POST':
        profiremni=request.form.get('firemni_oddeleni')
        provedouci=request.form.get('vedouci_pracovnici')
        skupiny = request.form.getlist('skupina[]')
        oddeleni_id = request.form.getlist('oddeleni[]')
        role=request.form.getlist('role[]')
        email = request.form.get('email')
        priorita = request.form.get('priorita')
        obsah_prispevku = request.form.get('obsah_prispevku')
        role_id = session.get('role_id')
        oddeleni=session.get('oddeleni')

        if provedouci =='1':
            SpravaPrispevku.pridej_prispevek_vedouci(obsah_prispevku,email)
            return redirect(url_for('homepage.view_homepage'))
        if profiremni =='1':
            SpravaPrispevku.pridej_prispevek_firemni(obsah_prispevku,priorita,email)
            return redirect(url_for('homepage.view_homepage'))
        if role_id <=2:
                if skupiny:
                    SpravaPrispevku.pridej_prispevek(obsah_prispevku, priorita, email, skupiny)
                    SpravaPrispevku.nastav_prioritu(priorita)
                    return redirect(url_for('homepage.view_homepage'))
                if oddeleni_id:
                    SpravaPrispevku.pridej_prispevek_oddeleni(obsah_prispevku, priorita, email,oddeleni_id)
                    SpravaPrispevku.nastav_prioritu(priorita)
                    return redirect(url_for('homepage.view_homepage'))
                if role:
                    SpravaPrispevku.pridej_prispevek_role(obsah_prispevku, priorita, email, role)
                    SpravaPrispevku.nastav_prioritu(priorita)
                    return redirect(url_for('homepage.view_homepage'))
                else:
                    SpravaPrispevku.pridej_prispevek_voddeleni(obsah_prispevku, priorita, email)
                    SpravaPrispevku.nastav_prioritu(priorita)
                    return redirect(url_for('homepage.view_homepage'))
        else:
            SpravaPrispevku.pridej_prispevek(obsah_prispevku, priorita, email, skupiny)

    return redirect(url_for('homepage.view_homepage'))

@homepage.route('/smaz_prispevek', methods=['POST'])
def smaz_prispevek():
    id_prispevku = request.form.get('id_prispevku')
    SpravaPrispevku.smaz_prispevek(id_prispevku)
    return redirect(url_for('homepage.view_homepage'))

