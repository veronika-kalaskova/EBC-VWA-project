from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, IntegerField, StringField, SelectField, PasswordField, validators


class SignInForm(Form):
    email = StringField(name='email', label='E-mail',
                        validators=[validators.Email(message="Špatný formát E-mailu"), validators.InputRequired()])
    password = PasswordField(name='password', label='Heslo',
                             validators=[validators.Length(min=3), validators.InputRequired()])


class RegisterForm(Form):
    email = StringField(name='email', label='E-mail',
                        validators=[validators.Email(message="Špatný formát E-mailu"), validators.InputRequired()])
    name = StringField(name='name', label='Jméno',
                       validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    surname = StringField(name='prijmeni', label='Příjmení',
                          validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='Heslo',
                             validators=[validators.Length(min=3), validators.InputRequired()])
    img = StringField(name='obrazek', label='Obrázek', validators=[validators.Length(min=0, max=10048)])


class AddGroupForm(Form):
    name = StringField(name='name', label='Název',
                       validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    email = StringField(name='email', label='E-mail',
                        validators=[validators.Email(message="Špatný formát E-mailu"), validators.InputRequired()])


class AddDepartmentForm(Form):
    name = StringField(name='name', label='Název',
                       validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    email = StringField(name='email', label='E-mail',
                        validators=[validators.Email(message="Špatný formát E-mailu"), validators.InputRequired()])


class EditPersonalInfo(Form):
    email = StringField(name='email', label='E-mail',
                        validators=[validators.Email(message="Špatný formát E-mailu"), validators.InputRequired()])
    name = StringField(name='name', label='Jméno',
                       validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    surname = StringField(name='prijmeni', label='Příjmení',
                          validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='Nové heslo',
                             validators=[validators.Length(min=3), validators.InputRequired()])
    img = StringField(name='obrazek', label='Obrázek', validators=[validators.Length(min=0, max=10048)])
    skupina = category_id = SelectField('Skupina', choices=[])
    oddeleni = SelectField('Oddělení', choices=[])
    role = SelectField('Role', choices=[])
