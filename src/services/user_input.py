from typing import List
import deepl,os
import redis
from models.mongo import ThreadAdmin as TAdmin

translator=deepl.Translator(os.getenv("DEEPL_API_KEY"))

class UserInputHandler:
    EVAL_CRITERIAS=[
    "Originality: Does the idea present a unique perspective or solution that others have not thought of? High originality is marked by the idea's novelty and its ability to stand out from common or traditional concepts.",
    "Innovativeness: This criterion assesses the extent to which the idea breaks existing norms and conventions. While originality is high for unique ideas (those others have not thought of), innovativeness scores highly for ideas that transcend implicit constraints in addressing a problem. It's about the degree of newness and the potential to disrupt current practices or thoughts.",
    "Practicality: Does the idea provide a viable solution to the given problem? An idea scores high in practicality if it directly addresses and effectively resolves the core issues at hand.",
    "Sustainability: Can the idea maintain its relevance and impact over a long period? Ideas with high sustainability are those whose benefits and effectiveness do not diminish quickly over time.",
    "Feasibility: Is the idea easy to implement in a real-world scenario? High feasibility is indicated by the ease with which the idea can be brought to life, considering available resources, technology, and time constraints.",
    "Efficiency: This evaluates the cost-effectiveness of the idea. It's determined by dividing the anticipated economic impact of the idea by its expected implementation costs. An idea scores high in efficiency if it promises significant benefits or savings relative to its cost.",
    "Profitable Scalability: This criterion evaluates the potential of the idea to generate significant revenue when scaled up as a large-scale software solution. It assesses the idea's capacity for expansion in terms of market reach and revenue generation, particularly when implemented on a larger or more comprehensive scale.",
    "User Experience (UX): This assesses whether the idea will result in a positive and satisfying experience for the end-user or customer. It involves considering aspects like usability, accessibility, engagement, and overall satisfaction. High UX scores are attributed to ideas that are user-friendly, intuitive, and appealing to their target audience."
]
    
    def receiveTranslatedProblem(self,problem:str)->str:
        """日本語で書かれたproblemをgetメソッドで受け取って，英語に翻訳してから格納する"""
        translated_problem=translator.translate_text(problem,target_lang="EN-US").text
        return translated_problem
        
    '''
    def receiveTranslatedIdea(self,idea:str,function_code:str)->None:
        """webフォームから1つずつstr形式で入力されたideaを受け取って，英語で格納する"""
        translated_ideas=translator.translate_text(idea,target_lang="EN-US").text
        if function_code=="func2":
            r.rpush("user_ideas",translated_ideas)
        elif function_code=="func3":
            r.rpush("pre_evaluated_idea",translated_ideas)
    '''
        
    def _convertCriteriaNumberIntoStr(self,selected_criterias:List[str])->List[str]:
        ret_list=[]
        for num in selected_criterias:
            ret_list.append(UserInputHandler.EVAL_CRITERIAS[int(num)-1])
        return ret_list    
    
    def receiveCriteriasAsStr(self,thread_id:str,criterias:List[str]):
        """webフォームからstr形式のボタン番号を渡されるので，mongoに格納する"""
        thread_admin=TAdmin()
        criterias=self._convertCriteriaNumberIntoStr(criterias)
        thread_admin.addCriterias(thread_id,criterias)
        

#mongoDBに渡すだけの操作
def addProblemToThread(thread_id:str,problem:str):
    thread_admin=TAdmin()
    thread_admin.addProblem(thread_id,problem)

        
    