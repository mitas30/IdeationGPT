from flask import request,render_template,Blueprint

func2 = Blueprint('func2', __name__)

@func2.route('/func2_core/')
def core_prog():
    return render_template('func2/func2_wait.html')

#improve_ideaのAPI部分
@func2.route('/improve_idea_api/')
def improveIdea():
    pass