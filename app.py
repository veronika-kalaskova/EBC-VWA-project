from flask import Flask
from database import database
from views.auth import auth_bp
from views.homepage import homepage
from views.usersOverview import usersOverview
from views.usersProfile import usersProfile
from views.groupSetting import groupSetting

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

app.register_blueprint(homepage, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(usersOverview, url_prefix='/prehled-uzivatelu')
app.register_blueprint(usersProfile, url_prefix='/profil')
app.register_blueprint(groupSetting, url_prefix='/sprava')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
