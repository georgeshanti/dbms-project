from flask import Flask
from flask_login import LoginManager
from src import set_pages, set_api, User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

set_pages(app)
set_api(app)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
