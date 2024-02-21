from flask import render_template
from init import app

@app.route("/")
def mainMenu():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="localhost",port=5000,debug=True)