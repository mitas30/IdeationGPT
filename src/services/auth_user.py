from models.mongo import AuthUser,ThreadAdmin
from werkzeug.security import check_password_hash
from typing import List

auth=AuthUser()

def create_user(nickname, password):
    if not nickname or not password or len(nickname) > 15:
        return False, "Invalid nickname or password"
    return auth.create_user_in_db(nickname, password)

def authenticate_user(nickname, password):
    user = auth.find_user_by_nickname(nickname)
    if user and check_password_hash(user['password'], password):
        return True, "Login successful"
    else:
        return False, "Invalid credentials"
    
def createThread(user_name:str):
    t_admin=ThreadAdmin()
    return t_admin.createNewThread(user_name)

def fetchThread(user_name:str)->List[dict[str,str]]:
    '''databaseからの操作を返すだけ'''
    t_admin=ThreadAdmin()
    return t_admin.fetchThreads(user_name)
    
