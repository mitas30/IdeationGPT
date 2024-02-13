#それより後の機能でも使われる関数のモジュール
from flask import render_template,Blueprint

error = Blueprint('error', __name__)

@error.route("/404_error/")
def error_redirect():
    return render_template('error.html')