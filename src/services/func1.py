import sys
from pathlib import Path
root_path=Path(__file__).parent.parent.parent
sys.path.append(str(root_path))
import google.generativeai as genai
from openai import OpenAI
import re,random,os
from random_word import Wordnik
from typing import List,Tuple,Union
from LogSettings import logger,logging
from threading import Thread
from deep_translator import GoogleTranslator
from static.datastore import falsefacedata as ff,ideaboxdata as ib,brutethinkdata as bt
from services.change_progress import ProgressChanger

g_api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=g_api_key)
genai.GenerationConfig(candidate_count=1)
GPT_MODEL="gpt-4-0125-preview"
GEMINI_MODEL='gemini-pro'

class Ideator:
    """発想法classのsuperクラス"""
    def __init__(self,problem="",thread_id=""):
        self.problem=problem
        #型はList[str]で、45個のアイデアが格納される
        self.improve_idea_list=[]
        self.p_changer=ProgressChanger()
        self.thread_id=thread_id
        self.idea_format="""<format>
[Idea number]: [Idea Name] (optional)
Core idea: [Brief explanation of the core idea]
Technologies and Materials Used: [Technologies and materials used]
Revised Approach to Problem-Solving: [How the problem is solved with this idea]
Concrete Use Cases: [List of use cases for the idea]"""

        self.note="""<note>
You need to follow the <format> below and attach a lengthy explanation of approximately 400 words for each idea.Also, output 5 ideas.
Each idea needs to be described in sufficient detail so that it can form the basis for a requirements definition. 
Therefore, although a 400-word explanation may seem lengthy at first glance, it is necessary to write in such detail to properly convey the concept."""

    def _normalizeProcess(self,full_idea:str)->Union[dict[str,str,str,str,str],None]:
        '''格納したアイデアを正規化する'''
        # タイトルのノイズを取り除く正規表現パターン
        title_noise_pattern = r"\([\w\s]+\)|[\"\*\<\>]"

        # 各セクションを分割する正規表現パターン
        section_pattern = r"([cC]ore [Ii]dea:|[Tt]echnologies and [Mm]aterials [uU]sed:|[rR]evised [aA]pproach to [pP]roblem-[sS]olving:|[cC]oncrete [uU]se [cC]ases:)"

        # セクションごとに分割
        sections = re.split(section_pattern, re.sub("\*","",full_idea))
        if len(sections)!=9:
            logger.log(logging.ERROR,f"正規化エラー:正常なsectionは9つに対して、今回は{str(len(sections))}")
            with open("D:\Programing\自主制作_code\IdeationGPT\src\static\datastore\error_log.txt","a",encoding="utf-8") as file:
                file.write(f"正規化エラー:正常なsectionは9つに対して、今回は{str(len(sections))}\n")
                i=1
                for section in sections:
                    file.write(f"section{i}:{section}\n")
                    i+=1
            return None

        # タイトルからノイズを除去して辞書に格納
        keys = ["Title","Core Idea", "Technologies and Materials Used", "Revised Approach to Problem-Solving", "Concrete Use Cases"]
        sections[0] = re.sub(title_noise_pattern, '', sections[0]).strip()
        parsed_dict={}
        for i in range(0,9,2):
            #\* : \\nを消す
            pattern=r"\*|:"
            content = re.sub(pattern,"",sections[i].strip().replace("\\n","\n"))
            parsed_dict[keys[i//2]] = content

        return parsed_dict
    
    def _extractIdea(self,idea_response: str) -> list[dict[str,str,str,str,str]]:
        """responseからアイデアを'5'個抽出して、正規化した辞書形式で返却する"""
        # アイデアのセクションを区切る正規表現パターン
        pattern = r'Idea\s*\d+\s*:'
        deivide_str = re.split(pattern, idea_response)
        # 最初の空要素をスキップし、空の行を削除したアイデアのlist
        idea_list=[re.sub(r"\n{2,}", '\n', section).strip() for section in deivide_str[1:6]]
        normalize_idea_list=[]
        for idea in idea_list:
            normalize_idea=self._normalizeProcess(idea)
            #正常に区切れた場合
            if normalize_idea!=None:
                normalize_idea_list.append(normalize_idea)
        return normalize_idea_list
    
    def serializeDict(self,idea:dict[str,str,str,str,str])->str:
        """構造化されたアイデアをstringにシリアライズする"""
        s_data=f"""{idea['Title']}
        Core Idea:{idea['Core Idea']}
        Technologies and Materials Used:{idea['Technologies and Materials Used']}
        Revised Approach to Problem-Solving:{idea['Revised Approach to Problem-Solving']}
        Concrete Use Cases:{idea['Concrete Use Cases']}"""
        return s_data
    
    def serializeDictForList(self,idea_list:List[dict[str,str,str,str,str]])->List[str]:
        """構造化されたアイデアをstringにシリアライズする"""
        ret_list=[]
        for idea in idea_list:
            s_data=self.serializeDict(idea)
            ret_list.append(s_data)
        return ret_list        

class FalseFacer(Ideator):
    def _extractReverseAssumption(self,idea_response:str)->list:
        '''反仮定を抽出する関数'''
        tmp_list=re.split('[Rr]eversed\s*[Aa]ssumptions[^:]*:',idea_response)
        pattern=r"[a-cA-C\-]:"
        ret_list=re.split(pattern,tmp_list[1])
        ret_list=ret_list[1:4]
        del_list=re.split("[iI]dea\s*\d+:",ret_list[2])
        ret_list[2]=del_list[0]
        return ret_list
    
    def falseFace(self,roop_second:int=3)->None:
        reverse_assumption_list=self._falseFaceFirstHalf()
        self.p_changer.changeEvent('falseFace:反仮定を3つ設定した',self.thread_id)
        threads=[]
        for i in range(roop_second):
            thread=Thread(target=self._falseFaceSecondHalf,args=(reverse_assumption_list[i],i+2))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
        self.p_changer.changeEvent('falseFaceのアイデア作成が終了',self.thread_id)

class IdeaBox(Ideator):
    """IdeaBoxという発想法を行えるclass"""
    
    #TODO ここ、たまにバグるから、そのときはもう一回行う処理をする
    def _selectRandAtt4Prob(self,attribute_list:list)->List[str]:
        """4つのパラメータに対する属性の組み合わせSを５つ集めたstrが3つ集まったリスト(len(3)のstrのlist)が出力される"""
        mem=[]
        selected_att=[]
        S = ""
        for i in range(15):
            while True:
                rand = random.randint(0, 9999)
                if rand not in mem:
                    mem.append(rand)
                    break
            S+=(str(i%5+1)+":")
            for j in range(3):
                select = rand % 10
                rand = (rand - select) // 10
                S += (attribute_list[j][select]+",")
            select = rand % 10
            S += (attribute_list[3][select]+"\n")
            if (i%5)==4:
                selected_att.append(S)
                S=""
        return selected_att 
    
    def _extractParam(self,response:str)->str:
        """response1からパラメータを取り出し、stringで返す"""
        pattern1=r"[pP]arameter[s\s*]\s*:\s*"
        pattern2=r"\n+"
        params = re.split(pattern2,re.split(pattern1,response)[1])[0]
        return params
        
    def _extractAtt4Prob(self,response :str)->list[list[str]]:
        """response1から属性を切り出して2D(4*10)のlistにする"""
        pattern=r"\n[1-4]\.\s*"
        #parameterを無視するので[1:]
        lines = re.split(pattern,response)[1:]
        lines=[re.sub('\n','',re.sub(',\s+',',',line)) for line in lines]
        #コンマで区切ってlistのlistにする
        attributes = [line.split(",") for line in lines]
        return attributes

    def ideaBox(self)->None:
        parameters,attribute_list=self._enumParaAndAttForProblem()     
        selected_attributes=self._selectRandAtt4Prob(attribute_list)
        self.p_changer.changeEvent('ideaBox:問題のパラメータと属性を発見',self.thread_id)

        threads = []
        for i in range(3):
            thread=Thread(target=self._generateIdeaUsingIdeaBox,args=(parameters,selected_attributes[i],i+1))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        self.p_changer.changeEvent('ideaBoxの終了',self.thread_id)
            
class BruteThinker(Ideator):
    """発想法BruteThinkを行うclass"""       
    def _generateRandomWords(self,num_words:int)->list:
        """ランダムな単語をlist形式で生成する。num_wordsは生成する長さ"""
        #各種パラメータ定義
        random_word_gerenerator=Wordnik()
        include_part_of_speech="noun"
        min_corpus_count=50000
        min_length=3
        ret=random_word_gerenerator.get_random_words(includePartOfSpeech=include_part_of_speech,minCorpusCount=min_corpus_count,minLength=min_length,limit=num_words)
        return ret
           
    def _forThread(self,r_word_str:str,count:int):
        logger.log(logging.INFO,f"bruteThinkの{count}回目の呼び出し")
        idea_num=self._doBruteThink(r_word_str,count)
        logger.log(logging.INFO,f"bruteThinkの{count}回目のアイデアは{idea_num}個")
    
    def bruteThink(self)->None:
        r_word_list=self._generateRandomWords(3)
        self.p_changer.changeEvent('bruteThink:ランダムな単語の選択完了',self.thread_id)
        threads=[]
        for count in range(3):
            thread=Thread(target=self._forThread,args=(r_word_list[count],count+1))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
        self.p_changer.changeEvent('bruteThinkの完了',self.thread_id)

class FFGPT(FalseFacer):
    def __init__(self, problem=""):
        super().__init__(problem)
        self.client=OpenAI()
        
    def _falseFaceFirstHalf(self)->List[str]:
        logger.log(logging.INFO,"falsefaceの1回目の呼び出し")
        user_example_problem="Reducing Urban Traffic Congestion"
        user_problem=self.problem
        #仮定の出力フォーマット
        assumption_format=ff.fh_assumption_format
        #反仮定の出力フォーマット
        reversed_assumption_format=ff.fh_r_assumption_format
        #問題を入力するまでのテンプレート
        user_template_a=ff.fh_user_template_a
        #仮定の出力フォーマットまでのテンプレート
        user_template_b=ff.fh_user_template_b
        #one_shotのユーザメッセージ
        user_example_message=f"""{user_template_a}\n\n<problem>{user_example_problem}\n\n{user_template_b}\n\n{assumption_format}\n\n{reversed_assumption_format}"""
        #実際のメッセージ
        user_message=f"""{user_template_a}\n\n<problem>{user_problem}\n\n{user_template_b}\n\n{assumption_format}\n\n{reversed_assumption_format}"""
        #one_shotのアンサーメッセージ
        assistant_answer_message=ff.fh_assistant_answer
        #LLMに渡すstring
        message=[
{"role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.'},
{"role":"user", "content":user_example_message},
{"role":"assistant", "content":assistant_answer_message },
{"role":"user","content":user_message}]
        
        #logger.log(logging.DEBUG,message)
        api_response = self.client.chat.completions.create(model=GPT_MODEL,messages=message,max_tokens=4000,temperature=1.00).choices[0].message.content
        try:
            logger.log(logging.DEBUG,f"falsefaceの1回目\nAnswerは:\n{api_response}")
            reverse_assumption_list=self._extractReverseAssumption(api_response)
            logger.log(logging.INFO,reverse_assumption_list)
        except IndexError:
            logger.log(logging.ERROR,f"falsefaceの1回目\nAnswerは:\n{api_response}")
        return reverse_assumption_list
        
    def _falseFaceSecondHalf(self,uans2_rev_assumption:str,count:int):
        user_example_problem="Reducing Urban Traffic Congestion"
        user_problem=self.problem
        #反仮定の例
        example_reverse_assumption="""Traffic congestion is a round-the-clock issue."""
        #入力された反仮定
        reverse_assumption=uans2_rev_assumption
        #問題を入力するまでのテンプレート
        user_template_a=ff.lh_user_template_a
        #仮定の出力フォーマットまでのテンプレート
        user_template_b=ff.lh_user_template_b
        #one_shotのユーザメッセージと、実際のメッセージ
        user_example_message=f"""{user_template_a}\n\n<problem> {user_example_problem}\n<Reversed Assumptions> {example_reverse_assumption}\n\n{user_template_b}\n\n{self.idea_format}\n\n{self.note}"""
        user_message=f"""{user_template_a}\n\n<problem> {user_problem}\n<Reversed Assumptions> {reverse_assumption}\n\n{user_template_b}\n\n{self.idea_format}\n\n{self.note}""" 
        #one_shotのアンサーメッセージ
        assitant_answer_message=ff.lh_assistant_answer
        message=[
            { "role":"system", "content":'You are a maker with high creativity and implementation skills.Please utilize your creativity to come up with effective ideas for the problem at hand.'},
            {"role":"user", "content":user_example_message },
            {"role":"assistant", "content":assitant_answer_message },
            {"role":"user","content":user_message}]
            
        #logger.log(logging.DEBUG,f"falseface2つ目のプロンプト:\n{message}")
        #実際の挙動
        logger.log(logging.INFO,f"falsefaceの{count}回目の呼び出し")
        api_response = self.client.chat.completions.create(model=GPT_MODEL,messages=message,max_tokens=4000,temperature=1.00).choices[0].message.content
        idea_list=self._extractIdea(api_response)
        if len(idea_list)!=5:
            logger.log(logging.WARNING,f"falseface{count}回目のアイデアの数は{str(len(idea_list))}個しかない")
        self.improve_idea_list.extend(idea_list)

class FFGemini(FalseFacer):
    def __init__(self, problem="",thread_id=""):
        super().__init__(problem,thread_id)
        self.client=genai.GenerativeModel(GEMINI_MODEL)
        
    def _falseFaceFirstHalf(self)->List[str]:
        logger.log(logging.INFO,"falsefaceの1回目の呼び出し")
        user_example_problem="Reducing Urban Traffic Congestion"
        user_problem=self.problem
        #仮定の出力フォーマット
        assumption_format=ff.fh_assumption_format
        #反仮定の出力フォーマット
        reversed_assumption_format=ff.fh_r_assumption_format
        #問題を入力するまでのテンプレート
        user_template_a=ff.fh_user_template_a
        #仮定の出力フォーマットまでのテンプレート
        user_template_b=ff.fh_user_template_b
        #one_shotのユーザメッセージ
        user_example_message=f"""{user_template_a}\n\n<problem>{user_example_problem}\n\n{user_template_b}\n\n{assumption_format}\n\n{reversed_assumption_format}"""
        #実際のメッセージ
        user_message=f"""{user_template_a}\n\n<problem>{user_problem}\n\n{user_template_b}\n\n{assumption_format}\n\n{reversed_assumption_format}"""
        #one_shotのアンサーメッセージ
        assistant_answer_message=ff.fh_assistant_answer
        #LLMに渡すstring
        message=f""""role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.'
"role":"user", "content":{user_example_message} 
"role":"assistant", "content":{assistant_answer_message },
"role":"user","content":{user_message}"""
        
        #logger.log(logging.DEBUG,message)
        api_response = self.client.generate_content(message).text
        try:
            logger.log(logging.DEBUG,f"falsefaceの1回目\nAnswerは:\n{api_response}")
            reverse_assumption_list=self._extractReverseAssumption(api_response)
            logger.log(logging.INFO,reverse_assumption_list)
        except IndexError:
            logger.log(logging.ERROR,f"falsefaceの1回目\nAnswerは:\n{api_response}")
        return reverse_assumption_list
        
    def _falseFaceSecondHalf(self,uans2_rev_assumption:str,count:int):
        user_example_problem="Reducing Urban Traffic Congestion"
        user_problem=self.problem
        #反仮定の例
        example_reverse_assumption="""Traffic congestion is a round-the-clock issue."""
        #入力された反仮定
        reverse_assumption=uans2_rev_assumption
        #問題を入力するまでのテンプレート
        user_template_a=ff.lh_user_template_a
        #仮定の出力フォーマットまでのテンプレート
        user_template_b=ff.lh_user_template_b
        #one_shotのユーザメッセージと、実際のメッセージ
        user_example_message=f"""{user_template_a}\n\n<problem> {user_example_problem}\n<Reversed Assumptions> {example_reverse_assumption}\n\n{user_template_b}\n\n{self.idea_format}\n\n{self.note}"""
        user_message=f"""{user_template_a}\n\n<problem> {user_problem}\n<Reversed Assumptions> {reverse_assumption}\n\n{user_template_b}\n\n{self.idea_format}\n\n{self.note}""" 
        #one_shotのアンサーメッセージ
        assitant_answer_message=ff.lh_assistant_answer
        message=f""" "role":"system", "content":'You are a maker with high creativity and implementation skills.Please utilize your creativity to come up with effective ideas for the problem at hand.'
            "role":"user", "content":{user_example_message }
            "role":"assistant", "content":{assitant_answer_message }
            "role":"user","content:"{user_message}"""
            
        #logger.log(logging.DEBUG,f"falseface2つ目のプロンプト:\n{message}")
        #実際の挙動
        logger.log(logging.INFO,f"falsefaceの{count}回目の呼び出し")
        roop=0
        max_roop=3
        while roop<max_roop:
            api_response = self.client.generate_content(message).text
            idea_list=self._extractIdea(api_response)
            if len(idea_list)<4:
                logger.log(logging.WARNING,f"falseface{count}回目{roop+1}周目のアイデアの数は{str(len(idea_list))}個しかない")
                roop+=1
            else:
                break
        if roop==max_roop:
            raise RuntimeError(f"falsefaceの{count}回目が正常に行われなかった")
        self.improve_idea_list.extend(idea_list)
    
class IBGPT(IdeaBox):
    def __init__(self, problem=""):
        super().__init__(problem)
        self.client=OpenAI()
        
    def _enumParaAndAttForProblem(self)->Tuple[str,List[str]]:
        """問題のパラメータと属性を列挙するideaBoxの前半プロンプト indexErrorが出る可能性があるので、3回まで実行する"""
        logger.log(logging.INFO,"ideaBoxの前処理呼び出し:")
        #one_shotの問題例
        uex_problem="Bridging the Educational Gap"
        uans_problem=self.problem
        #problemの前の説明文
        common_user_message_b=ib.fh_common_user_message_b
        #problemの後の説明文
        common_user_message_a=ib.fh_common_user_message_a
        #1回の会話における文章
        uex_message=f""" {common_user_message_b}{uex_problem}{common_user_message_a}"""        
        user_message=f"""{common_user_message_b}{uans_problem}{common_user_message_a}"""        
        aans_message=ib.fh_aans_message

        message=[
{"role":"system", "content":'You are a maker with high creativity and implementation skills. Additionally, you are skilled at abstracting concepts.'},
{"role":"user", "content":uex_message },
{"role":"assistant", "content":aans_message },
{"role":"user","content":user_message}]
            
        count=0 
        max_count=3
        #logger.log(logging.DEBUG,f"ideaBoxの前処理呼び出しメッセージ:\n{message}")
        while count<max_count:
            att_response = self.client.chat.completions.create(model=GPT_MODEL,messages=message,max_tokens=4000,temperature=1.00).choices[0].message.content
            #logger.log(logging.DEBUG,f":ideaBoxの前処理呼び出しレスポンス:\n{att_response}")
            try:
                parameters=self._extractParam(att_response)
                attribute_list=self._extractAtt4Prob(att_response)
                break
            except IndexError as e:
                count+=1
                logger.log(logging.ERROR,f"ideaBoxの前処理で{e}。もう一度実行します。\nError:{att_response}")
        if count==max_count:
            raise RuntimeError(f"ideaBoxの前処理が{count}回失敗したらしい。改善しよう。")
        
        logger.log(logging.INFO,f"ideaBoxのパラメータ:\n{parameters}")
        logger.log(logging.INFO,f"ideaBoxの属性リスト:\n{attribute_list}")
        return parameters,attribute_list
    
    def _generateIdeaUsingIdeaBox(self,parameters:str,selected_attribute:str,num:int):
        #one_shotの問題例
        user_example_problem="Bridging the Educational Gap"
        user_problem=self.problem
        #one_shotのパラメータ例
        user_example_parameter=ib.lh_user_example_parameter
        user_example_attributes=ib.lh_user_example_attributes
        user_template_message=ib.lh_user_template_message
        #1回の会話における文章
        uex_message=f"<Guide>\n\n<Problem> {user_example_problem}\n<parameter> {user_example_parameter}\n<attributes>\n{user_example_attributes}\n{user_template_message}\n\n{self.idea_format}\n\n{self.note}"
        user_message=f"<Guide>\n\n<Problem> {user_problem}\n<parameter> {parameters}\n<attributes> {selected_attribute}\n{user_template_message}\n\n{self.idea_format}\n\n{self.note}"
        aans_message=ib.lh_aans_message
        
        message=[
{"role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.'},
{"role":"user", "content":uex_message },
{"role":"assistant", "content":aans_message },
{"role":"user","content":user_message}]
        
        #logger.log(logging.DEBUG,message[:100])
        count=0
        max_count=3
        logger.log(logging.INFO,f"ideaBoxの{num}回目の呼び出し")
        while(count<max_count):
            idea_response = self.chat.completions.create(model=GPT_MODEL,messages=message,max_tokens=4000,temperature=1.00).choices[0].message.content
            idea_list=self._extractIdea(idea_response)
            #idea毎に区切れているか確認する
            if 4<=len(idea_list) and len(idea_list)<=7:
                self.improve_idea_list.extend(idea_list)
                logger.log(logging.INFO,f"ideaBoxの{num}回目は{len(idea_list)}個のアイデア")
                break
            else:
                count+=1
                logger.log(logging.ERROR,f"ideaBoxの{num}回目の{count}周目が失敗した。\nideaの数は{len(idea_list)}だけである。")
                continue
        if count==max_count:
            raise RuntimeError(f"ideaBoxの{num}回目が実行できなかった")
    
class IBGemini(IdeaBox):
    def __init__(self, problem="",thread_id=""):
        super().__init__(problem,thread_id)
        self.client=genai.GenerativeModel(GEMINI_MODEL)
        
    def _enumParaAndAttForProblem(self)->Tuple[str,List[str]]:
        """問題のパラメータと属性を列挙するideaBoxの前半プロンプト indexErrorが出る可能性があるので、3回まで実行する"""
        logger.log(logging.INFO,"ideaBoxの前処理呼び出し:")
        #one_shotの問題例
        uex_problem="Bridging the Educational Gap"
        uans_problem=self.problem
        #problemの前の説明文
        common_user_message_b=ib.fh_common_user_message_b
        #problemの後の説明文
        common_user_message_a=ib.fh_common_user_message_a
        #1回の会話における文章
        uex_message=f""" {common_user_message_b}{uex_problem}{common_user_message_a}"""        
        user_message=f"""{common_user_message_b}{uans_problem}{common_user_message_a}"""        
        aans_message=ib.fh_aans_message

        message=f""""role":"system", "content":'You are a maker with high creativity and implementation skills. Additionally, you are skilled at abstracting concepts.'
"role":"user", "content":{uex_message }
"role":"assistant", "content":{aans_message }
"role":"user","content":{user_message}"""
            
        count=0 
        max_count=3
        #logger.log(logging.DEBUG,f"ideaBoxの前処理呼び出しメッセージ:\n{message}")
        while count<max_count:
            att_response = self.client.generate_content(message).text
            #logger.log(logging.DEBUG,f":ideaBoxの前処理呼び出しレスポンス:\n{att_response}")
            try:
                parameters=self._extractParam(att_response)
                attribute_list=self._extractAtt4Prob(att_response)
                break
            except IndexError as e:
                count+=1
                logger.log(logging.ERROR,f"ideaBoxの前処理で{e}。もう一度実行します。\nError:{att_response}")
        if count==max_count:
            raise RuntimeError(f"ideaBoxの前処理が{count}回失敗したらしい。改善しよう。")
        
        logger.log(logging.INFO,f"ideaBoxのパラメータ:\n{parameters}")
        logger.log(logging.INFO,f"ideaBoxの属性リスト:\n{attribute_list}")
        return parameters,attribute_list
    
    def _generateIdeaUsingIdeaBox(self,parameters:str,selected_attribute:str,num:int):
        #one_shotの問題例
        user_example_problem="Bridging the Educational Gap"
        user_problem=self.problem
        #one_shotのパラメータ例
        user_example_parameter=ib.lh_user_example_parameter
        user_example_attributes=ib.lh_user_example_attributes
        user_template_message=ib.lh_user_template_message
        #1回の会話における文章
        uex_message=f"<Guide>\n\n<Problem> {user_example_problem}\n<parameter> {user_example_parameter}\n<attributes>\n{user_example_attributes}\n{user_template_message}\n\n{self.idea_format}\n\n{self.note}"
        user_message=f"<Guide>\n\n<Problem> {user_problem}\n<parameter> {parameters}\n<attributes> {selected_attribute}\n{user_template_message}\n\n{self.idea_format}\n\n{self.note}"
        aans_message=ib.lh_aans_message
        
        message=f""""role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.'
"role":"user", "content":{uex_message }
"role":"assistant", "content":{aans_message }
"role":"user","content":{user_message}"""
        
        #logger.log(logging.DEBUG,message[:100])
        count=0
        max_count=3
        logger.log(logging.INFO,f"ideaBoxの{num}回目の呼び出し")
        while(count<max_count):
            idea_response = self.client.generate_content(message).text
            idea_list=self._extractIdea(idea_response)
            #idea毎に区切れているか確認する
            if 4<=len(idea_list) and len(idea_list)<=7:
                self.improve_idea_list.extend(idea_list)
                logger.log(logging.INFO,f"ideaBoxの{num}回目は{len(idea_list)}個のアイデア")
                break
            else:
                count+=1
                logger.log(logging.ERROR,f"ideaBoxの{num}回目の{count}周目が失敗した。\nideaの数は{len(idea_list)}だけである。")
                continue
        if count==max_count:
            raise RuntimeError(f"ideaBoxの{num}回目が実行できなかった")
    
class BTGPT(BruteThinker):
    def __init__(self, problem=""):
        super().__init__(problem)
        self.client=OpenAI()
        
    #TODO:出力最大長の問題から、brutethinkは2つに分ける(属性選択とアイデア出力)
    def _doBruteThink(self,r_word_str:str,count:int)->int:
        system_message="You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand."
        user_example_problem="How can we make public transportation more appealing to commuters?"
        b_user_common_message=bt.b_user_common_message
        attribute_format=bt.attribute_format
        case_study=bt.case_study
        a_user_common_message=f"""{attribute_format}\n{self.note}\n{self.idea_format}\n{case_study}"""
        #1回の会話における文章
        uex_message=f"""<Essential Rules to Strictly Follow>\n{self.note}\n\n{b_user_common_message}\n\n<problem> {user_example_problem}\n<word> coffee\n{a_user_common_message}"""
        user_message=f"""<Essential Rules to Strictly Follow>\n{self.note}\n\n{b_user_common_message}\n<problem> {self.problem}\n<word> {r_word_str}\n{a_user_common_message}"""
        assistant_answer=bt.assistant_answer
        
        message=[
{"role":"system", "content":system_message},
{"role":"user", "content":uex_message},
{"role":"assistant", "content":assistant_answer},
{"role":"user","content":user_message}]
        
        r_count=0
        max_count=3
        while r_count<max_count:
            try:
                api_response = self.clientchat.completions.create(model=GPT_MODEL,messages=message,max_tokens=4000,temperature=1.00).choices[0].message.content
            except ValueError:
                r_count+=1
                logger.log(logging.WARNING,f"BruteThinkでValueError at {count}回目の{r_count}周目:\n{api_response}")
                continue
            idea_list=self._extractIdea(api_response)
            #idea毎に区切れているか確認する(本当は=5にしたいけど)
            if 3<len(idea_list)&len(idea_list)<7:
                self.improve_idea_list.extend(idea_list)
                break
            else:
                r_count+=1
                logger.log(logging.WARNING,f"Idea数が少ない or 区切れていないエラー at {count}回目の{r_count}周目:\nbtのアイデア数は、{str(len(idea_list))}個しかない")
                continue
        if r_count==max_count:
            raise RuntimeError(f"brutethinkのいずれかが{r_count}回失敗した")
        return len(idea_list)
    
class BTGemini(BruteThinker):
    def __init__(self, problem="",thread_id=""):
        super().__init__(problem,thread_id)
        self.client=genai.GenerativeModel(GEMINI_MODEL)
        
    #TODO:出力最大長の問題から、brutethinkは2つに分ける(属性選択とアイデア出力)
    def _doBruteThink(self,r_word_str:str,count:int)->int:
        system_message="You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand."
        user_example_problem="How can we make public transportation more appealing to commuters?"
        b_user_common_message=bt.b_user_common_message
        attribute_format=bt.attribute_format
        case_study=bt.case_study
        a_user_common_message=f"""{attribute_format}\n{self.note}\n{self.idea_format}\n{case_study}"""
        #1回の会話における文章
        uex_message=f"""<Essential Rules to Strictly Follow>\n{self.note}\n\n{b_user_common_message}\n\n<problem> {user_example_problem}\n<word> coffee\n{a_user_common_message}"""
        user_message=f"""<Essential Rules to Strictly Follow>\n{self.note}\n\n{b_user_common_message}\n<problem> {self.problem}\n<word> {r_word_str}\n{a_user_common_message}"""
        assistant_answer=bt.assistant_answer
        
        message=f"""
        "role":"system", "content":{system_message},
        "role":"user", "content":{uex_message},
        "role":"assistant", "content":{assistant_answer},
        "role":"user","content":{user_message}"""
        
        r_count=0
        max_count=3
        while r_count<max_count:
            try:
                response = self.client.generate_content(message)
                api_response=response.text
            except ValueError:
                r_count+=1
                logger.log(logging.WARNING,f"BruteThinkでValueError at {count}回目の{r_count}周目:\n{response}")
                continue
            idea_list=self._extractIdea(api_response)
            #idea毎に区切れているか確認する(本当は=5にしたいけど)
            if 3<=len(idea_list)&len(idea_list)<7:
                self.improve_idea_list.extend(idea_list)
                break
            else:
                r_count+=1
                logger.log(logging.WARNING,f"Idea数が少ない or 区切れていないエラー at {count}回目の{r_count}周目:\nbtのアイデア数は、{str(len(idea_list))}個しかない")
                continue
        if r_count==max_count:
            raise RuntimeError(f"brutethinkのいずれかが{r_count}回失敗した")
        return len(idea_list)
    
def split_string_to_chunks(long_string, chunk_size):
    """長い文字列を指定されたサイズのチャンクに分割する関数。"""
    return [long_string[i:i + chunk_size] for i in range(0, len(long_string), chunk_size)]



