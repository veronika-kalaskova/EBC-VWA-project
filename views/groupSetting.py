from flask import Blueprint, render_template, redirect, url_for, request, flash
from Service.sprava_skupin import SpravaSkupin
from Service.sprava_oddeleni import SpravaOddeleni
import forms
import auth

groupSetting = Blueprint('group-setting', __name__)


@groupSetting.route("/", )
@auth.login_required
def view_group_setting():
    formSkupina = forms.AddGroupForm(request.form)
    formOddeleni = forms.AddDepartmentForm(request.form)

    skupiny = SpravaSkupin.vypis_skupiny()
    oddeleni = SpravaOddeleni.vypis_oddeleni()

    skupiny_prvky = []
    oddeleni_prvky = []

    for skupina in skupiny:
        skupiny_dict = {
            "nazev": skupina[0],
            "jmeno": skupina[1],
            "prijmeni":skupina[2],
            "skupina_id": skupina[3],
            "nazev_oddeleni":skupina[4]
        }

        skupiny_prvky.append(skupiny_dict)

    for od in oddeleni:
        oddeleni_dict = {
            "nazev": od[0],
            "jmeno": od[1],
            "prijmeni": od[2],
            "oddeleni_id": od[3]
        }

        oddeleni_prvky.append(oddeleni_dict)

    return render_template("group-setting/group-setting.jinja", skupiny=skupiny_prvky, oddeleni=oddeleni_prvky,
                           formSkupina=formSkupina, formOddeleni=formOddeleni)


@groupSetting.route('/smazat-skupinu', methods=['POST'])
def smazat_skupinu():
    skupina_id = request.form.get('skupina_id')
    SpravaSkupin.smaz_skupinu(skupina_id)
    return redirect(url_for('group-setting.view_group_setting'))


@groupSetting.route('/smazat-oddeleni', methods=['POST'])
def smazat_oddeleni():
    oddeleni_id = request.form.get('oddeleni_id')
    SpravaOddeleni.smaz_oddeleni(oddeleni_id)
    return redirect(url_for('group-setting.view_group_setting'))

@groupSetting.route('/pridat-skupinu', methods=['POST'])
def pridej_skupinu():
    id_oddeleni = request.form.get('oddeleni')
    nazev = request.form.get('name')
    email = request.form.get('email')
    je_uzivatel=SpravaSkupin.kontrola_email(email)
    if je_uzivatel:
        jevedouci = SpravaSkupin.jevedouci(email)
        if jevedouci:
            SpravaSkupin.insert_skupina(nazev, email,id_oddeleni)
        else:
            flash('Uživatel je již vedoucím jiné skupiny')
    else:
        flash('Uživatel s tímto E-mailem neexistuje')
    return redirect(url_for('group-setting.view_group_setting'))



@groupSetting.route('/pridat-oddeleni', methods=['POST'])
def pridej_oddeleni():
    nazev = request.form.get('name')
    email = request.form.get('email')
    je_uzivatel = SpravaSkupin.kontrola_email(email)
    if je_uzivatel:
        jevedouci = SpravaOddeleni.jemanazer(email)
        if jevedouci:
            SpravaOddeleni.insert_oddeleni(nazev,email)
        else:
            flash('Uživatel je již manažer jiného oddělení')
    else:
        flash('Uživatel s tímto E-mailem neexistuje')
    return redirect(url_for('group-setting.view_group_setting'))

