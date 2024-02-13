from flask import Blueprint, jsonify,render_template,request,session
from services.auth_user import create_user, authenticate_user,createThread
import services.auth_user as AuthUser
auth_user = Blueprint('auth_user', __name__)

@auth_user.route('/signup_api', methods=['POST'])
def signup():
    nickname = request.json.get('nickname')
    password = request.json.get('password')
    result, message = create_user(nickname, password)
    if result:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"error": message}), 400

@auth_user.route('/login_api', methods=['POST'])
def login():
    nickname = request.json.get('nickname')
    password = request.json.get('password')
    result, message = authenticate_user(nickname, password)
    if result==True:
        session['user']=nickname
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 401
    
@auth_user.route('/signup', methods=['GET'])
def red_signup():
    return render_template('signup.html')

@auth_user.route('/login', methods=['GET'])
def red_login():
    return render_template('login.html')

@auth_user.route('/mypage',methods=['GET'])
def red_mypage():
    print(session)
    return render_template('mypage.html')

#スレッドの作成
@auth_user.route('/create_thread_api')
def create_thread():
    user_name=session.get('user')
    thread_id=createThread(user_name)
    session['thread_id']=thread_id
    return jsonify()

#スレッドの取得
@auth_user.route('/fetch_thread_api')
def fetch_thread():
    user_name=session.get('user')
    threads=AuthUser.fetchThread(user_name)
    return jsonify({"threads":threads})