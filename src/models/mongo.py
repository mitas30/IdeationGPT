from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from typing import List

client = MongoClient()
#dbの中にcollectionがあって、collectionの中にdocmentがある

class AuthUser:
    def __init__(self):
        db = client["ideation_gpt"]
        self.users_collection = db["users"]

    def create_user_in_db(self,nickname,password):
        hashed_password = generate_password_hash(password)
        try:
            self.users_collection.insert_one({"nickname": nickname, "password": hashed_password})
            return True, "User created successfully"
        except DuplicateKeyError:
            return False, "Nickname already exists"

    def find_user_by_nickname(self,nickname):
        return self.users_collection.find_one({"nickname": nickname})
    
class ThreadAdmin:
    def __init__(self):
        db = client["ideation_gpt"]
        self.users_collection = db["threads"]
        
    def createNewThread(self,u_id:str):
        result=self.users_collection.insert_one({"u_id": u_id,"progress":0})
        return str(result.inserted_id)
    
    def addProblem(self,thread_id:str,problem:str):
        self.users_collection.update_one({"_id":ObjectId(thread_id)},{"$set":{"problem":problem,"progress":1}})
        
    def addCriterias(self,thread_id:str,criteria_list:List[str]):
        print(thread_id)
        self.users_collection.update_one({"_id":ObjectId(thread_id)},{"$set":{"criterias":criteria_list,"progress":2}})
        
    def fetchThreads(self,user_name:str)->List[dict[str,str,int]]:
        cursor=self.users_collection.find({"u_id":user_name})
        ret_list=[]
        for doc in cursor:
            thread_id=str(doc.get("_id"))
            problem=doc.get("problem","")
            progress=doc.get("progress")
            ret_list.append({"thread_id":thread_id,"problem":problem,"progress":progress})
        return ret_list
    
    def fetchProblem(self,thread_id:str)->str:
        doc=self.users_collection.find_one({"_id":ObjectId(thread_id)})
        return doc.get("problem")
    
    def fetchCriterias(self,thread_id:str)->List[str]:
        doc=self.users_collection.find_one({"_id":ObjectId(thread_id)})
        return doc.get("criterias")
    
    def updateProgressToComplete(self,thread_id:str):
        self.users_collection.update_one({"_id":ObjectId(thread_id)},{"$set":{"progress":3}})
        
class IdeaAdmin:
    def __init__(self):
        db = client["ideation_gpt"]
        self.users_collection = db["ideas"]
        
    def storageIdea(self,normalize_data=dict[str,str,str,str,str,str])->None:
        return self.users_collection.insert_one(normalize_data)
    
    def fetchGreatIdeas(self,thread_id:str):
        '''そのthread_idのgreatなideaを格納したcursorを返却する'''
        return self.users_collection.find(
            filter={'$and':[{'thread_id':thread_id},{'is_great':{"$exists":True}}]},
            projection={'_id':False,'Title':True,'Core Idea':True,'Technologies and Materials Used':True,
                        'Revised Approach to Problem-Solving':True,'Concrete Use Cases':True})
        
        
    
    
           