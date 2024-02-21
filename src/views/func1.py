from flask import Blueprint,session,render_template,jsonify,request
from threading import Thread
from services.func1 import FFGemini,IBGemini,BTGemini
from services.func3 import EvaluateGPT,IdeaHandler,EvaluateGemini
from services.func2 import InoveteGemini
from services.change_progress import ProgressChanger
from services.user_input import fetchProblemFromThread,fetchCriteriaFromThread
from LogSettings import logging,logger
import time

func1 = Blueprint('func1', __name__)

def createIdeas(problem:str)->list[dict[str,str,str,str,str]]:
    p_changer=ProgressChanger()
    thread_id=session['thread_id']
    '''アイデア作成のstep'''
    falsefacer=FFGemini(problem,thread_id)
    thread1=Thread(target=falsefacer.falseFace)
    ib=IBGemini(problem,thread_id)
    thread2=Thread(target=ib.ideaBox)
    bt=BTGemini(problem,thread_id)
    thread3=Thread(target=bt.bruteThink)
    p_changer.changeEvent("3つの発想法を用いたアイデア作成の開始",thread_id)
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
    p_changer.changeEvent(f"アイデア作成の完了:合計アイデアは{len(candidate_ideas)}個",thread_id)
    #debug 格納されたアイデアが正規化されているか確認する
    for idea in candidate_ideas:
        print('-'*80)
        print(f"name={idea['Title']}")
    return candidate_ideas
    
def evaluateIdeas(problem,idea_list:list[dict[str,str,str,str,str]],criterias:list[str],is_improve:bool)->list[dict[str,str,str,str,str]]:
    '''アイデア評価のstep'''
    p_changer=ProgressChanger()
    thread_id=session['thread_id']
    evaluator=EvaluateGemini(problem,idea_list,criterias,thread_id)
    p_changer.changeEvent(f"アイデア評価の開始",thread_id)
    idea_num=evaluator.concurrentEvaluate()
    logger.log(logging.INFO,f"評価済みアイデアの数:{idea_num}個")
    p_changer.changeEvent(f"アイデア評価完了:評価アイデア{idea_num}個",thread_id)
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
    p_changer.changeEvent(f"再利用アイデアの格納:{threshold}個",thread_id)
    #次に使用するアイデアをidea_listにいれる
    great_ideas=evaluator.great_ideas
    if is_improve==True:
        for great_idea in great_ideas:
            i_handler.storageIdea(great_idea,session['thread_id'],True)
    for great_idea in great_ideas:
        print(great_idea["Title"])
        print('-'*80)
    p_changer.changeEvent(f"良いアイデア:{len(great_ideas)}個の選択完了",thread_id)
    return great_ideas
        
def improveIdeas(problem:str,idea_list:list[dict[str,str,str,str,str]])->list[dict[str,str,str,str,str]]:
    '''アイデア改善のstep'''
    p_changer=ProgressChanger()
    thread_id=session['thread_id']
    innovator=InoveteGemini(problem,idea_list,thread_id)
    p_changer.changeEvent("改善アイデアの作成開始",thread_id)
    innovator.scamperMethod()
    candidate_ideas=innovator.all_improve_idea
    p_changer.changeEvent(f"アイデア向上の完了:新たなアイデアは{len(candidate_ideas)}個",thread_id)
    print("アイデアの数",str(len(candidate_ideas)))
    #debug
    for candidate_idea in candidate_ideas:
        print(candidate_idea['Title'])
    return candidate_ideas
    
@func1.route('/init_progress/')
def init_progress()->None:
    p_changer=ProgressChanger()
    thread_id=session['thread_id']
    p_changer.initProgress(thread_id)
    return jsonify()
    
@func1.route('/get_progress/')
def get_progress():
    p_changer=ProgressChanger()
    thread_id=session['thread_id']
    progresses=p_changer.takeProgresses(thread_id)
    return jsonify(progresses)

#improve_ideaのAPI部分
@func1.route('/make_idea_api/')
def make_idea()->None:
    thread_id=session['thread_id']
    p_changer=ProgressChanger()
    problem=fetchProblemFromThread(thread_id)
    criterias=fetchCriteriaFromThread(thread_id)
    candidate_ideas=createIdeas(problem)
    p_changer.changeProgress(thread_id,"1")
    great_ideas=evaluateIdeas(problem,candidate_ideas,criterias,False)
    p_changer.changeProgress(thread_id,"2")
    improve_ideas=improveIdeas(problem,great_ideas)
    p_changer.changeProgress(thread_id,"3")
    idea_list=evaluateIdeas(problem,improve_ideas,criterias,True)
    p_changer.changeProgress(thread_id,"4")
    count=1
    for idea in idea_list:
        logger.log(logging.INFO,f"idea{count}:\n{idea['Title']}")
        count+=1
    return jsonify()

@func1.route('/display_result/')
def display_result():
    i_handler=IdeaHandler()
    #idea_listは構造化されたアイデア(dict)のList。
    thread_id=request.args.get("thread_id")
    if thread_id!=None:
        session["thread_id"]=thread_id
    thread_id=session['thread_id']
    idea_list=i_handler.fetchGreatIdeas(thread_id)
    for idea in idea_list:
        logger.log(logging.INFO,idea['Title'])
    return render_template('func1/func1_result.html',display_ideas=idea_list)

@func1.route('/back_to_mypage/')
def redirect_to_mypage():
    return render_template('mypage.html')

