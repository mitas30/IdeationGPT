#NOTE blueprint→app→socket→blueprintの循環import問題、及びsessionの更新頻度からの不具合
#NOTE したがって、進捗管理は、redisを用いたポーリングで行う
#NOTE redisではbyte文字列で格納される

import redis

class ProgressAdmin:
    '''進捗の管理を行う'''
    def __init__(self) -> None:
        self.r=redis.Redis()
        
    def initProgress(self,thread_id:str)->None:
        self.r.hmset(thread_id,{'progress':'0',"event":'None'})
        
    def takeProgresses(self,thread_id:str)->list[bytes,bytes]:
        return self.r.hmget(thread_id,'progress','event')
    
    def changeProgress(self,thread_id:str,progress:str):
        self.r.hset(thread_id,'progress',progress)
    
    def changeEvent(self,thread_id:str,event:str):
        self.r.hset(thread_id,'event',event)
        
        
        
    
    