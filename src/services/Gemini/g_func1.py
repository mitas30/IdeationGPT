import sys
from pathlib import Path
root_path=Path(__file__).parent.parent.parent
sys.path.append(str(root_path))
import google.generativeai as genai
import re,random,os
from random_word import Wordnik
from typing import List,Tuple,Union
from LogSettings import logger,logging
from threading import Thread
from deep_translator import GoogleTranslator
import static.datastore.falsefacedata as ff
import static.datastore.ideaboxdata as ib
import static.datastore.brutethinkdata as bt

g_api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=g_api_key)
genai.GenerationConfig(candidate_count=1)
client=genai.GenerativeModel('gemini-pro')

class Ideator:
    """発想法classのsuperクラス"""
    def __init__(self,problem=""):
        self.problem=problem
        #型はList[str]で、45個のアイデアが格納される
        self.improve_idea_list=[]
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
        title_noise_pattern = r"\([\w\s]+\)|\"|\*"

        # 各セクションを分割する正規表現パターン
        section_pattern = r"(Core [I,i]dea:|Technologies and Materials Used:|Revised Approach to Problem-Solving:|Concrete Use Cases:)"

        # セクションごとに分割
        sections = re.split(section_pattern, full_idea)
        if len(sections)!=9:
            print(f"正規化エラー:正常なsectionは9つに対して、今回は{str(len(sections))}")
            print(f"errorが出た文章は、\n{full_idea[:300]}")
            return None

        # タイトルからノイズを除去して辞書に格納
        cleaned_title = re.sub(title_noise_pattern, '', sections[0]).strip()
        parsed_dict = {"Title": cleaned_title}

        for i in range(1, len(sections), 2):
            #section名がCore ideaのとき、Core Ideaに変化させる
            section_name = re.sub(r":","",sections[i].strip().replace("Core idea","Core Idea"))
            #\* : \\nを消す
            pattern=r"\*|:"
            content = re.sub(pattern,"",sections[i + 1].strip().replace("\\n","\n"))
            parsed_dict[section_name] = content

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
        '''ここ、indexerrorが起きる可能性あり'''
        tmp_list=re.split('[Rr]eversed\s*[Aa]ssumptions[^:]*:',idea_response)
        pattern="[a-cA-C]:"
        ret_list=re.split(pattern,tmp_list[1])
        ret_list=ret_list[1:4]
        del_list=re.split("[iI]dea\s*\d+:",ret_list[2])
        ret_list[2]=del_list[0]
        return ret_list
    
    def _falseFaceFirstHalf(self)->Tuple[list,list]:
        user_example_problem="Reducing Urban Traffic Congestion"
        user_problem=self.problem
        #仮定の出力フォーマット
        assumption_format=ff.fh_assumption_format
        #反仮定の出力フォーマット
        reversed_assumption_format=ff.fh_r_assumption_format
        #問題を入力するまでのテンプレート
        user_template_a=ff.user_template_a
        #仮定の出力フォーマットまでのテンプレート
        user_template_b=ff.fh_user_template_b
        #one_shotのユーザメッセージ
        user_example_message=f"""{user_template_a}\n\n<problem>{user_example_problem}\n\n{user_template_b}\n\n{assumption_format}\n\n{reversed_assumption_format}\n\n{self.idea_format}\n\n{self.note}"""
        #実際のメッセージ
        user_message=f"""{user_template_a}\n\n<problem>{user_problem}\n\n{user_template_b}\n\n{assumption_format}\n\n{reversed_assumption_format}\n\n{self.idea_format}\n\n{self.note}"""
        #one_shotのアンサーメッセージ
        assistant_answer_message=ff.fh_assistant_answer
        #LLMに渡すstring
        message=f""""role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.'
            "role":"user", "content":{user_example_message} 
            "role":"assistant", "content":{assistant_answer_message },
            "role":"user","content":{user_message}"""
            
        api_response = client.generate_content(message).text
        try:
            reverse_assumption_list=self._extractReverseAssumption(api_response)
            idea_list=self._extractIdea(api_response)
        except IndexError:
            print(api_response)
            print("error")
        return idea_list,reverse_assumption_list
        
    def _falseFaceSecondHalf(self,uans2_rev_assumption:str,count:int):
        user_example_problem="Reducing Urban Traffic Congestion"
        user_problem=self.problem
        #反仮定の例
        example_reverse_assumption="""Traffic congestion is a round-the-clock issue."""
        #入力された反仮定
        reverse_assumption=uans2_rev_assumption
        #問題を入力するまでのテンプレート
        user_template_a=ff.user_template_a
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
        #実際の挙動
        logger.log(logging.INFO,f"falsefaceの{count}回目の呼び出し")
        api_response = client.generate_content(message).text
        idea_list=self._extractIdea(api_response)
        self.improve_idea_list.extend(idea_list)
    
    def falseFace(self,roop_second:int=2)->None:
        logger.log(logging.INFO,"falseFaceの1回目の呼び出し")
        idea_list,reverse_assumption_list=self._falseFaceFirstHalf()
        self.improve_idea_list.extend(idea_list)
        threads=[]
        for i in range(roop_second):
            thread=Thread(target=self._falseFaceSecondHalf,args=(reverse_assumption_list[i],i+2))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()

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
        pattern1=r"[pP]arameter\s*:\s*"
        pattern2=r"\n+"
        params = re.split(pattern2,re.split(pattern1,response)[1])[0]
        return params
        
    def _extractAtt4Prob(self,response :str)->list:
        """response1から属性を切り出して2D(4*10)のlistにする"""
        pattern=r"\n[1-4]\.\s*"
        #parameterを無視するので[1:]
        lines = re.split(pattern,response)[1:]
        lines=[re.sub('\n','',re.sub(',\s+',',',line)) for line in lines]
        #コンマで区切ってlistのlistにする
        attributes = [line.split(",") for line in lines]
        return attributes

    def _enumParaAndAttForProblem(self)->Tuple[str,List[str]]:
        """問題のパラメータと属性を列挙するideaBoxの部分関数"""
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

        message=f"""
            "role":"system", "content":'You are a maker with high creativity and implementation skills. Additionally, you are skilled at abstracting concepts.'
            "role":"user", "content":{uex_message }
            "role":"assistant", "content":{aans_message }
            "role":"user","content":{user_message}"""
        
        #処理部分
        att_response = client.generate_content(message).text
        parameters=self._extractParam(att_response)
        attribute_list=self._extractAtt4Prob(att_response)
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
        uex_message=f"<Guide>\n<Problem> {user_example_problem}\n<parameter> {user_example_parameter}\n<attributes>\n{user_example_attributes}\n{user_template_message}\n\n{self.idea_format}\n\n{self.note}"
        user_message=f"<Guide>\n<Problem> {user_problem}\n<parameter> {parameters}\n<attributes> {selected_attribute}\n{user_template_message}\n\n{self.idea_format}\n\n{self.note}"
        aans_message=ib.lh_aans_message
        
        message=f"""
        "role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.'
        "role":"user", "content":{uex_message }
        "role":"assistant", "content":{aans_message }
        "role":"user","content":{user_message}"""

        #実際の処理
        logger.log(logging.INFO,f"ideaBoxの{num}回目の呼び出し")
        idea_response = client.generate_content(message).text
        idea_list=self._extractIdea(idea_response)
        #idea毎に区切れているか確認する
        if len(idea_list)<10:
            self.improve_idea_list.extend(idea_list)
        else:
            raise Exception("InvalidDivideAtIdeaBoxError")

    def ideaBox(self)->None:
        logger.log(logging.INFO,"ideaBoxの前処理呼び出し:")
        parameters,attribute_list=self._enumParaAndAttForProblem()      
        selected_attributes=self._selectRandAtt4Prob(attribute_list)
        threads = []
        for i in range(3):
            thread=Thread(target=self._generateIdeaUsingIdeaBox,args=(parameters,selected_attributes[i],i+1))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()      
            
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
    
    #TODO:出力最大長の問題から、brutethinkは2つに分ける(属性選択とアイデア出力)
    def _doBruteThink(self,r_word_str:str)->list:
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
        
        #実際の処理
        try:
            response = client.generate_content(message)
            api_response=response.text
        except ValueError:
            print(f"エラー:{response}")
        idea_list=self._extractIdea(api_response)
        #idea毎に区切れているか確認する(本当は=5にしたいけど)
        if 2<len(idea_list)&len(idea_list)<10:
            print(f"btのアイデア数は、{str(len(idea_list))}")
            self.improve_idea_list.extend(idea_list)
        else:
            print(f"Idea数が少ない or 区切れていないエラー:btのアイデア数は、{str(len(idea_list))}")
            raise Exception("InvalidDivideAtBruteThinkError")
        
        
    def _forThread(self,r_word_str:str,count:int):
        logger.log(logging.INFO,f"bruteThinkの{count+1}回目の呼び出し")
        self._doBruteThink(r_word_str)
    
    def bruteThink(self)->None:
        r_word_list=self._generateRandomWords(3)
        threads=[]
        for count in range(3):
            thread=Thread(target=self._forThread,args=(r_word_list[count],count))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()

def split_string_to_chunks(long_string, chunk_size):
    """長い文字列を指定されたサイズのチャンクに分割する関数。"""
    return [long_string[i:i + chunk_size] for i in range(0, len(long_string), chunk_size)]



