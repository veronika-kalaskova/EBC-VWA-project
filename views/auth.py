import bcrypt
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import auth
import forms
from Service.sprava_uzivatelu import SpravaUzivatelu
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    form = forms.SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        user = SpravaUzivatelu.verify(email=request.form['email'], password=request.form['password'])
        print(user)
        if not user:
            flash('Nesprávný email nebo heslo')
        else:
            session['authenticated'] = 1
            session['email'] = user['email']
            session['jmeno'] = user['jmeno']
            session['prijmeni'] = user['prijmeni']
            session['role'] = user['role']
            session['role_id'] = user['role_id']
            session['skupina'] = user['skupina']
            session['oddeleni'] = user['oddeleni']
            session['foto']=user['foto']
            return redirect(url_for('homepage.view_homepage'))
    return render_template("auth/sign_in.jinja", form=form)


@auth_bp.route('/signout')
@auth.login_required
def signout():
    session.pop("authenticated")
    session.pop("email")
    # session.pop("role")
    return redirect(url_for('homepage.view_homepage'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email= form.email.data
        password = form.password.data
        name=form.name.data
        surname=form.surname.data
        salt = bcrypt.gensalt()
        hash_password= bcrypt.hashpw(password.encode('utf-8'),salt)
        img=form.img.data
        check_email = SpravaUzivatelu.kontrola(email)
        if email and password and name:
            if check_email == False:
                SpravaUzivatelu.insert_uzivatel(name, surname, email, password, img)
            else:
                flash('E-mail již existuje')
                return render_template("auth/register.jinja", form=form)

        return redirect(url_for('auth.sign_in'))


    return render_template("auth/register.jinja", form=form)