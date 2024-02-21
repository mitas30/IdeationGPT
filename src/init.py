from flask import Flask
from views.user_input import user_input
from views.func1 import func1
from views.func2 import func2
from views.func3 import func3
from views.error import error
from views.auth_user import auth_user
from flask_cors import CORS
from datetime import timedelta
from jinja2 import Environment

# 改行文字をHTMLの改行タグに変換するフィルター関数
def nl2br(s):
    return s.replace("\n", "<br>")

def create_app():
    '''app_instanceを作成する関数 ファクトリーパターンらしい?'''
    app = Flask(__name__)
    app.secret_key="finding_nemo"
    app.permanent_session_lifetime = timedelta(minutes=100) 
    CORS(app)
    app.register_blueprint(user_input,url_prefix='/input')
    app.register_blueprint(func1, url_prefix='/func1')
    app.register_blueprint(func2, url_prefix='/func2')
    app.register_blueprint(func3, url_prefix='/func3')
    app.register_blueprint(auth_user,url_prefix='/auth_user')
    app.register_blueprint(error, url_prefix='/error')
    return app

app=create_app()

# Jinja2環境にカスタムフィルターを登録
app.jinja_env.filters['nl2br'] = nl2br