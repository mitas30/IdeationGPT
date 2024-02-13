from flask import Flask,render_template
from views.user_input import user_input
from views.func1 import func1
from views.func2 import func2
from views.func3 import func3
from views.error import error
from views.auth_user import auth_user
from flask_cors import CORS
from datetime import timedelta

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

@app.route("/")
def mainMenu():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)