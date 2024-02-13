from services.Gemini.g_func1 import FalseFacer,IdeaBox,BruteThinker
from threading import Thread
problem="An unprecedented experience"

bt=BruteThinker(problem=problem)
thread3=Thread(target=bt.bruteThink)
thread3.start()
thread3.join()