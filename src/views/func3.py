from flask import request,render_template,Blueprint,session,jsonify
from redis import Redis
from services.GPT.func3 import IdeaEvaluator

# Blueprintの作成
func3 = Blueprint('func3', __name__)
r=Redis("localhost")

#リダイレクト用
@func3.route('/waiting_evaluation/')
def redirectEvaluationPage():
    return render_template('func3/func3_wait.html')

#リダイレクト用
@func3.route('/display_evaluate_result/')
def redirectToResult():
    great_ideas=r.lrange('evaluate_result',0,-1)
    #ついでに一時データを消去する
    r.delete("pre_evaluated_idea")
    r.delete("evaluate_result")
    return render_template('func3/func3_display_result.html',result_list=great_ideas)

@func3.route('/evaluate_idea_api/')
def evaluateIdea():
    problem=session["problem"]
    pre_evaluate_idea=r.lrange('pre_evaluated_idea')
    #evaluator=IdeaEvaluator(problem,pre_evaluate_idea)
    #evaluator.evaluateIdea()
    return jsonify()
    

