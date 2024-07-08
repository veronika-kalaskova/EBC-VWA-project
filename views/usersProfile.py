from flask import Blueprint, render_template, request, redirect, url_for

import auth
from Service.sprava_roli import SpravaRoli
from Service.sprava_skupin import SpravaSkupin
from Service.sprava_oddeleni import SpravaOddeleni
from Service.sprava_uzivatelu import SpravaUzivatelu
import forms
usersProfile = Blueprint('users-profile', __name__)

@usersProfile.route("/",)
@auth.login_required
def view_users_profile():
    role = SpravaRoli.vypis_role()
    skupina = SpravaSkupin.get_all_skupina()
    oddeleni = SpravaOddeleni.get_all_oddeleni()

    form = forms.EditPersonalInfo(request.form)
    form.role.choices = [(r['role_id'], r['nazev']) for r in role]
    form.skupina.choices = [(s['skupina_id'], s['nazev']) for s in skupina]
    form.oddeleni.choices = [(o['oddeleni_id'], o['nazev']) for o in oddeleni]

    return render_template("users-profile/users-profile.jinja", role=role, form=form)

@usersProfile.route("/edit_user/<int:user_id>", methods=['GET','POST'])
@auth.login_required
def edit_users_profile(user_id):
    print(user_id)
    role = SpravaRoli.vypis_role()
    skupina = SpravaSkupin.get_all_skupina()
    oddeleni = SpravaOddeleni.get_all_oddeleni()
    uzivatel_udaje=SpravaUzivatelu.udaje_uzivatel(user_id)
    form = forms.EditPersonalInfo(request.form)
    form.role.choices = [(r['role_id'], r['nazev']) for r in role]
    form.skupina.choices = [(s['skupina_id'], s['nazev']) for s in skupina]
    form.oddeleni.choices = [(o['oddeleni_id'], o['nazev']) for o in oddeleni]
    return render_template("users-profile/edit-profile.jinja",udaje=uzivatel_udaje,role = role, form=form)

@usersProfile.route("/editProfile", methods=['POST'])
@auth.login_required
def editProfile():
    role = request.form.get('role')
    skupina = request.form.get('skupina')
    oddeleni = request.form.get('oddeleni')
    id_uzivatele =request.form['id_uzivatele']
    print(role,skupina,oddeleni)
    print(id_uzivatele)
    SpravaUzivatelu.edituj_uzivatele(id_uzivatele, role, skupina, oddeleni)
    return redirect(url_for('users-overview.view_users_overview'))

@usersProfile.route("/editImg", methods=['POST'])
@auth.login_required
def editImg():
    id_uzivatele =request.form['id_uzivatele']
    img = request.form['obrazek']
    SpravaUzivatelu.edituj_img(id_uzivatele, img)
    return redirect(url_for('users-overview.view_users_overview'))

@usersProfile.route("/editPsw", methods=['POST'])
@auth.login_required
def editPsw():
    id_uzivatele =request.form['id_uzivatele']
    heslo = request.form['password']
    SpravaUzivatelu.edituj_heslo(id_uzivatele, heslo)
    return redirect(url_for('users-overview.view_users_overview'))
