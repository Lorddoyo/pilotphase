from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import flask_admin as Admin
from flask_uploads import UploadSet,configure_uploads,IMAGES
from config import config_options
from flask_mail import Mail
from flask_simplemde import SimpleMDE
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()

photos = UploadSet('photos', IMAGES)

mail = Mail()
simple = SimpleMDE()



def create_app(config_name):

    app = Flask(__name__)

    admin =Admin(app)
    admin.add = View(MyModelView(User, db.session))

    # Creating the app configurations
    app.config.from_object(config_options[config_name])
   

    # Intializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)


    # Will add the views and forms

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user_auth import user_auth as u_auth_bp
    app.register_blueprint(u_auth_bp,url_prefix = '/authenticate')

    # configure UploadSet
    configure_uploads(app,photos)

    # set optional bootswatch theme
    # app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    # admin = Admin(app, name='accesscontrol', template_mode='bootstrap4')
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Post, db.session))
    # Create admin
    admin = admin.Admin(app, 'Example: Auth', index_view=MyAdminIndexView(), base_template='my_master.html')

    # Add view
    admin.add_view(MyModelView(User, db.session))
    

    return app