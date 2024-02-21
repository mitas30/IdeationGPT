from models.redis import ProgressAdmin
from flask import session

class ProgressChanger:
    def __init__(self) -> None:
        self.p_admin=ProgressAdmin()
    
    def initProgress(self,thread_id:str):
        self.p_admin.initProgress(thread_id)
    
    def changeProgress(self,thread_id:str,progress:str):
        self.p_admin.changeProgress(thread_id,progress)
    
    def changeEvent(self,event:str,thread_id:str):
        self.p_admin.changeEvent(thread_id,event)
    
    def takeProgresses(self,thread_id:str)->list[str,str]:
        progresses=self.p_admin.takeProgresses(thread_id)
        ret_list=[]
        for att in progresses:
            ret_list.append(att.decode('utf-8'))
        return ret_list
        