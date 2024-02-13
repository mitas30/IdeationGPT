from services import user_input as input
from flask import Blueprint, jsonify,request,render_template,session

user_input = Blueprint('user_input', __name__)
input_handler=input.UserInputHandler()

# NOTE: 一旦保留(機能をアイデア作成だけにする func_codeは廃止)
'''
#htmlのGETメソッドの受け先
@user_input.route('/receive_function/',methods=['GET'])
def select_func():
    function_code=request.args.get('func')
    r.set("func_code",function_code)
    return render_template('reuse/input_prob.html',func_code=function_code)
    
@user_input.route('/receive_idea_api/', methods=['POST'])
def receive_idea():
    request_data=request.json
    input_handler.receiveTranslatedIdea(request_data['idea'])
    return jsonify()
'''
@user_input.route('/input_prob', methods=['GET'])
def redSelectFunc():
    return render_template('reuse/input_prob.html')

@user_input.route('/receive_prob/', methods=['POST'])
def receive_prob():
    input_problem=request.form["problem"]
    translate_problem=input_handler.receiveTranslatedProblem(input_problem)
    thread_id=session.get('thread_id')
    input.addProblemToThread(thread_id,translate_problem)
    return render_template('reuse/select_criterias.html')

@user_input.route('/receive_criteria/', methods=['POST'])
def receiveCriteria():
    input_criterias=request.form.getlist("criteria")
    thread_id=session.get('thread_id')
    input_handler.receiveCriteriasAsStr(thread_id,input_criterias)
    return render_template("func1/func1_wait.html")  
