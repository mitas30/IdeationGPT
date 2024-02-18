from flask import Blueprint,jsonify,session
from threading import Thread
from services.func1 import FFGemini,IBGemini,BTGemini
from services.func3 import EvaluateGPT,IdeaHandler,EvaluateGemini
from services.func2 import InoveteGemini
from services.user_input import fetchProblemFromThread,fetchCriteriaFromThread
from LogSettings import logging,logger
from deep_translator import GoogleTranslator
from typing import List

func1 = Blueprint('func1', __name__)

def createIdeas(problem:str)->List[dict[str,str,str,str,str]]:
    '''アイデア作成のstep'''
    print(problem)
    falsefacer=FFGemini(problem=problem)
    thread1=Thread(target=falsefacer.falseFace)
    ib=IBGemini(problem=problem)
    thread2=Thread(target=ib.ideaBox)
    bt=BTGemini(problem=problem)
    thread3=Thread(target=bt.bruteThink)
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    #debug 出してくるアイデアの数がちゃんと15ずつであるか確認する
    idea_list=falsefacer.improve_idea_list
    print("ffのアイデアの数",str(len(idea_list)))
    idea_list=ib.improve_idea_list
    print("ibのアイデアの数",str(len(idea_list)))
    idea_list=bt.improve_idea_list
    print("btのアイデアの数",str(len(idea_list)))
    candidate_ideas=falsefacer.improve_idea_list+ib.improve_idea_list+bt.improve_idea_list
    #debug 格納されたアイデアが正規化されているか確認する
    for idea in candidate_ideas:
        print('-'*80)
        print(f"name={idea['Title']}")
        #print(f"name={idea['Title']}",f"abstract={idea['Core Idea']}",f"tech={idea['Technologies and Materials Used']}",f"solving={idea['Revised Approach to Problem-Solving']}",f"usecase={idea['Concrete Use Cases']}",sep="\n")        
    return candidate_ideas
    
def evaluateIdeas(problem,idea_list:List[dict[str,str,str,str,str]],criterias:List[str],is_improve:bool):
    '''アイデア評価のstep'''
    evaluator=EvaluateGemini(problem,idea_list,criterias)
    idea_num=evaluator.concurrentEvaluate()
    logger.log(logging.INFO,f"評価済みアイデアの数:{idea_num}個")
    for score in evaluator.idea_score_list:
        print(score)
    #向上アイデアなら5、0->1アイデアなら10個選出する
    select_idea_num=0
    if is_improve==True:
        select_idea_num=5
    else:
        select_idea_num=10
    evaluator.sortByScores(select_idea_num)
    save_ideas=idea_list
    #step2.5:アイデアの格納
    sorted_score_list=evaluator.idea_score_list
    #収納するアイデアの個数決定
    threshold=(len(idea_list)-select_idea_num)//2
    i_handler=IdeaHandler()
    #アイデアをmongoに収納し続ける
    rank=0
    while rank<threshold:
            i_handler.storageIdea(save_ideas[sorted_score_list[rank][1]],session['thread_id'])
            rank+=1
    #次に使用するアイデアをidea_listにいれる
    great_ideas=evaluator.great_ideas
    if is_improve==True:
        for great_idea in great_ideas:
            i_handler.storageIdea(great_idea,session['thread_id'],True)
    for great_idea in great_ideas:
        print(great_idea["Title"])
        print('-'*80)
    return great_ideas
        
def improveIdeas(problem:str,idea_list:List[dict[str,str,str,str,str]])->List[dict[str,str,str,str,str]]:
    '''アイデア改善のstep'''
    innovator=InoveteGemini(problem,idea_list)
    innovator.scamperMethod()
    candidate_ideas=innovator.all_improve_idea
    print("アイデアの数",str(len(candidate_ideas)))
    #debug
    for candidate_idea in candidate_ideas:
        print(candidate_idea['Title'])
    return candidate_ideas
    
#improve_ideaのAPI部分
@func1.route('/make_idea_api/')
def makeIdea():
    problem=fetchProblemFromThread(session['thread_id'])
    criterias=fetchCriteriaFromThread(session['thread_id'])
    candidate_ideas=createIdeas(problem)
    great_ideas=evaluateIdeas(problem,candidate_ideas,criterias,False)
    improve_ideas=improveIdeas(problem,great_ideas)
    idea_list=evaluateIdeas(problem,improve_ideas,criterias,True)
    count=1
    for idea in idea_list:
        logger.log(logging.INFO,f"idea{count}:\n{idea}")
        count+=1
    return jsonify({"idea":idea_list})