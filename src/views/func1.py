from flask import Blueprint,jsonify
from threading import Thread
from services.Gemini.g_func1 import FalseFacer,IdeaBox,BruteThinker
from services.GPT.func3 import IdeaEvaluator
from services.GPT.func2 import Innovator
from LogSettings import logging,logger
from deep_translator import GoogleTranslator
import redis

func1 = Blueprint('func1', __name__)
r=redis.Redis(db=1)

#improve_ideaのAPI部分
@func1.route('/make_idea_api/')
def makeIdea():
    return jsonify()
    #step1:アイデア作成
    problem=r.get('problem').decode('utf-8')
    falsefacer=FalseFacer(problem=problem)
    thread1=Thread(target=falsefacer.falseFace)
    ib=IdeaBox(problem=problem)
    thread2=Thread(target=ib.ideaBox)
    bt=BruteThinker(problem=problem)
    thread3=Thread(target=bt.bruteThink)
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    idea_list=falsefacer.improve_idea_list
    print("ffのアイデアの数",str(len(idea_list)))
    idea_list=ib.improve_idea_list
    print("ibのアイデアの数",str(len(idea_list)))
    idea_list=bt.improve_idea_list
    print("btのアイデアの数",str(len(idea_list)))
    idea_list=falsefacer.improve_idea_list+ib.improve_idea_list+bt.improve_idea_list
    i=1
    for idea in idea_list:
        translated=GoogleTranslator(source='en',target='ja').translate(text=idea)
        logger.log(logging.INFO,f"アイデア{i}\n{translated}")
        i+=1
    #step2:アイデアの評価
    evaluator=IdeaEvaluator(problem,idea_list)
    evaluator.evaluateIdea()
    evaluator.sortByScores()
    idea_list=evaluator.great_ideas
    #step3:アイデアの改善と評価
    for i in range(1):
        innovator=Innovator(problem,idea_list)
        innovator.scamperMethod()
        idea_list=innovator.all_improve_idea
        print("アイデアの数",str(len(idea_list)))
        evaluator=IdeaEvaluator(problem,idea_list)
        evaluator.evaluateIdea()
        evaluator.sortByScores()
        idea_list=evaluator.great_ideas
    for idea in idea_list:
        print(idea)
    return jsonify({"idea":idea_list})