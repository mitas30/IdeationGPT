from typing import List,Tuple
from openai import OpenAI
from LogSettings import logger,logging
import re,deepl,os
from redis import Redis

client=OpenAI()
gpt_model="gpt-3.5-turbo-1106"
translator=deepl.Translator(os.getenv("DEEPL_API_KEY"))
r=Redis("localhost",db=1)

class IdeaEvaluator():
    def __init__(self,problem:str,ideas:List[str]):
        self.problem=problem
        self.selected_criterias=r.lrange("criterias",0,-1)
        "型List[str](アイデアが5つが1つのstrとしてまとまっている) アイデアの概要だから最後まで捨てないこと"
        self.pre_evaluate_idea=ideas
        "アイデアの評価は5個ごとに1つのstrで収納する"
        self.idea_eval_list=[]
        self.great_ideas=[]
        
    def _ideaDevideByFive(self,count:int)->List[str]:
        """大きなListから、5つの要素だけを切り出す"""
        ret_list=self.pre_evaluate_idea[5*count:min(5*(count+1),len(self.pre_evaluate_idea))]
        return ret_list
            
    def evaluateIdea(self)->None:
        roop_max=len(self.pre_evaluate_idea)//5
        
        system_message="You are required to fairly evaluate my ideas, possessing both high creativity and implementation skills. The evaluation is strict, and you would assign a score of 6 out of 10 to ideas you consider good based on the evaluation criteria."
        
        user_template_message='''Please implement the following guidelines.\n
Guidelines: see the list of <idea> to solve (issue). The list of <idea> is formatted as follows\n
1.[Idea Name1]\nCore Idea:\nTechniques and materials to be used:\nRevised approach to solving the problem:\nSpecific Use:\n2.[Idea Name2]\n...
This list contains the names of several ideas and their details. Rate each idea in <Idea> on a scale of 1 to 10 according to the criteria in (Criteria).\n Also, please output your responses to each idea in the following <FORMAT> format. The [] part is a variable, so change it depending on your ideas and criteria

<FORMAT>\n[Idea number (starting from 1)]. [Idea name].\n[criteria1]: [X1(score)]/10\n[Why did you choose that score for that criterion?]\n....\n[criteria y]:[Xy(score)]/10\n[Why did you choose that score for that criterion?]
'''
        pre_evaluate_idea_list=["""Emotion Share Sticker
Core Idea:The Emotion Share Sticker is a pioneering smartphone accessory, ingeniously crafted to offer a unique way of expressing emotions. This accessory bridges the gap between digital communication and sensory experience, enriching interactions in a world increasingly reliant on remote connections. By adhering to the back of a smartphone, it introduces a blend of visual appeal and olfactory sensation, representing various emotions. The sticker’s design is a kaleidoscope of colors, where hues like bright yellows and oranges symbolize joy and optimism, while blues and greens evoke calmness and serenity. Its innovative feature lies in the integration of olfactory capsules, which, when activated via an accompanying app, release scents correlating to the chosen emotions. This creative approach allows users to convey their feelings in a more comprehensive and multisensory manner.
Technologies and Materials Used:The Emotion Share Sticker incorporates advanced microencapsulation technology, encapsulating a variety of fragrances in tiny, durable spheres. These capsules are carefully designed to release specific scents when prompted by the user through a custom-designed smartphone app. The technology behind this involves meticulous programming that allows users to select and modify the intensity and duration of the scent, thus offering a personalized experience. The app's interface is user-friendly, ensuring seamless interaction between the user and the sticker’s features.
Revised Approach to Problem-Solving:In a world where digital communication often lacks the depth of face-to-face interaction, the Emotion Share Sticker offers a novel solution. It enhances remote communication by introducing an olfactory dimension to digital messages, thereby enriching the emotional context of exchanges. This sticker is particularly beneficial in scenarios where verbal or textual communication falls short, offering a subtle yet impactful means to convey feelings.
Concrete Use Cases:The sticker finds its utility in various scenarios. In remote work settings, it can be used to express work-related stress or accomplishment without the need for explicit communication. It also plays a significant role in personal relationships, allowing individuals to share their feelings in a non-verbal but profoundly expressive manner. For instance, sending a scent of lavender could indicate a need for calmness in stressful times, while a citrus fragrance could celebrate a joyful moment. The Emotion Share Sticker thus stands out as an innovative tool, enhancing the depth and quality of remote interactions.""",
"""Emotional VR
Core Idea:Emotional VR is a state-of-the-art virtual reality system meticulously engineered to provide a personalized emotional experience. It stands as a technological marvel that not only recognizes but also adapts to the user's current emotional state, offering an immersive journey through virtual environments that resonate with their feelings. By harnessing the power of emotion recognition technology, Emotional VR interprets emotions from facial expressions and voice tones, transforming these cues into dynamic VR experiences. This system tailors virtual scenarios in real-time, ensuring that each virtual space is a reflection of the user's emotional landscape.
Technologies and Materials Used:At the heart of Emotional VR lies cutting-edge emotion recognition technology, which utilizes advanced algorithms to analyze facial expressions and voice modulations. This technology is integrated with VR hardware to create an environment that dynamically adjusts based on the user's emotional state. The VR scenarios are crafted with high-definition graphics and sound, providing a deeply immersive and sensory-rich experience. The system also includes professionally designed voice guides, which further enrich the user’s journey through various emotional landscapes.
Revised Approach to Problem-Solving:Emotional VR revolutionizes the way individuals engage with their emotions. It acknowledges the importance of emotional health and offers a virtual space where users can confront and explore their feelings in a controlled, safe environment. Whether it's stress relief through serene natural settings or joy enhancement via lively social events, Emotional VR caters to a wide spectrum of emotional needs, promoting psychological well-being.
Concrete Use Cases:The system's versatility allows for a multitude of applications. In a therapeutic context, it provides a tool for mental health professionals to guide clients through emotional landscapes, offering a novel approach to emotional healing. For everyday users, it offers an escape into calming environments or exciting adventures based on their current mood, serving as a daily emotional wellness tool. Emotional VR thus stands as a pioneering platform that bridges the gap between technology and emotional well-being.""",
"""Biometric Interaction in VR
Core Idea:Biometric Interaction in VR is a groundbreaking system that seamlessly blends biometric sensors with virtual reality, creating a symbiotic environment responsive to the user's emotional state. This advanced system takes VR experiences to new heights by not just immersing users in virtual worlds but also making these worlds react in real-time to their emotions. Users don VR headsets equipped with sensors that track physiological indicators such as heart rate, skin conductance, and breathing patterns. An intelligent emotion recognition algorithm interprets these data, enabling the VR environment to adapt and respond to the user's emotional nuances.
Technologies and Materials Used:This system integrates sophisticated biometric sensors with VR technology. The sensors, worn by the user, capture real-time physiological data, which are then processed by an advanced emotion recognition algorithm. The VR environment is powered by high-end graphics engines, capable of creating diverse and responsive scenarios that shift according to the user's emotional state. Additionally, the system encourages users to express emotions through specific VR movements, enhancing the interactive and immersive nature of the experience.
Revised Approach to Problem-Solving:Biometric Interaction in VR introduces a transformative approach to understanding and expressing emotions. By linking physiological responses to VR experiences, it provides users with a unique method to manage and explore their emotional states. This technology serves not only as a tool for personal emotional awareness but also has practical applications in emotional health promotion and stress management.
Concrete Use Cases:The system finds its use in various settings, from therapeutic to recreational. In a therapeutic setting, it aids in emotional regulation and stress management, providing users with a controlled environment to explore and understand their emotional responses. For recreational users, it offers a novel form of entertainment, where games and experiences are tailored to their emotional state, creating a highly personalized and engaging experience. In both contexts, Biometric Interaction in VR stands as an innovative solution for enhancing emotional connectivity and well-being.""",
"""Emotion-Harmonizing Smart Jewelry
Core Idea:Emotion-Harmonizing Smart Jewelry represents an innovative blend of fashion and technology, designed to offer a novel way of expressing and understanding emotions through wearable accessories. This smart jewelry, encompassing items like bracelets and necklaces, is embedded with emotion-recognition sensors that detect and interpret the wearer's emotional states in real-time. The core functionality of this jewelry lies in its ability to change color or pattern based on the wearer's emotions, providing a visual representation of feelings.
Technologies and Materials Used:The jewelry incorporates advanced sensors capable of monitoring physiological indicators such as heart rate and skin temperature. These sensors utilize sophisticated algorithms to infer the wearer's current emotional state. The aesthetic elements of the jewelry, such as color-changing materials or e-ink displays, dynamically alter their appearance to reflect emotional changes – warmer tones for joy and cooler tones for relaxation. The jewelry is also integrated with a smartphone app, enhancing the emotional experience by offering personalized recommendations like music or meditation suggestions based on the detected emotions.
Revised Approach to Problem-Solving:Emotion-Harmonizing Smart Jewelry introduces a unique approach to emotional awareness and communication. By making emotional states visible, the jewelry encourages wearers to become more conscious of their feelings, fostering emotional intelligence and empathy. It also serves as a subtle yet powerful tool for non-verbal emotional expression, enhancing interpersonal connections.
Concrete Use Cases:The jewelry finds its utility in various personal and social scenarios. In personal use, it helps individuals track and manage their emotional states, acting as a catalyst for mindfulness and self-care. Socially, it allows wearers to non-verbally communicate their feelings to others, facilitating deeper emotional connections. The accessory can also be used in therapeutic settings, aiding in emotional regulation and awareness exercises.""",
"""Emotion-Sync Social Network
Core Idea:Emotion-Sync Social Network is a revolutionary concept that intertwines emotion recognition technology with social media. This platform enables users to share their emotional states in real-time, fostering a new dimension of connectivity and empathy in the digital world. It reads emotions from various inputs like text, voice, or facial expressions and displays this information on user profiles, creating an emotionally attuned social network.
Technologies and Materials Used:The platform employs advanced emotion recognition algorithms that analyze user inputs – text, voice, and facial expressions – to accurately discern their current emotional state. This technology integrates with a user-friendly app or social media platform, allowing users to communicate and share their emotions authentically and effortlessly.
Revised Approach to Problem-Solving:Emotion-Sync Social Network redefines the way people interact on social media. By focusing on emotional states, it creates a more empathetic and supportive online community. This approach enables users to find and connect with others experiencing similar emotions, be it for shared support during challenging times or celebrating joyous moments together.
Concrete Use Cases:This platform caters to a wide range of emotional interactions. Users feeling down can seek and offer support to others in similar emotional states, creating a community of care and understanding. Conversely, those in a positive emotional state can spread joy and positivity, enhancing overall emotional well-being. This network acts as a digital haven for emotional support and positive communication, contributing significantly to mental health and emotional wellness."""]
        
        
        select_criteria_list=["""Originality:Does the idea present a unique perspective or solution that others have not thought of? High originality is marked by the idea's novelty and its ability to stand out from common or traditional concepts.""",
                            """Innovativeness:This criterion assesses the extent to which the idea breaks existing norms and conventions. While originality is high for unique ideas (those others have not thought of), innovativeness scores highly for ideas that transcend implicit constraints in addressing a problem. It's about the degree of newness and the potential to disrupt current practices or thoughts.""",
                            """Practicality:Does the idea provide a viable solution to the given problem? An idea scores high in practicality if it directly addresses and effectively resolves the core issues at hand.""",
                            """Sustainability:Can the idea maintain its relevance and impact over a long period? Ideas with high sustainability are those whose benefits and effectiveness do not diminish quickly over time.""",
                            """Feasibility:Is the idea easy to implement in a real-world scenario? High feasibility is indicated by the ease with which the idea can be brought to life, considering available resources, technology, and time constraints."""]

        
        user_example_message=f"""{user_template_message}\n<Issue>\nHow to use information technology to enrich people's emotions\n\n<Idea>\n{pre_evaluate_idea_list}\n\n<Criteria>\n{select_criteria_list}"""
        
        assistant_answer_message='''Evaluation:
1. Emotion Share Sticker\nOriginality: 8/10\nThe concept of blending digital communication with sensory experience, especially olfactory, is quite unique.\nInnovativeness: 7/10\nIt innovatively integrates visual and scent elements in digital interactions, which is a fresh approach but relies on existing technology.\nPracticality: 5/10\nThe idea is practical in concept but may face challenges in terms of consistent and effective scent delivery.\nSustainability: 6/10\nThe novelty might wear off, but if the technology evolves, it could maintain relevance.\nFeasibility: 4/10\nImplementing advanced microencapsulation technology in a small, affordable sticker form could be challenging.
2. Emotional VR\nOriginality: 7/10\nVR for emotional experiences exists, but tailoring it to users' emotions in real-time is a novel aspect.\nInnovativeness: 8/10\nIt pushes the boundaries of VR technology by incorporating emotion recognition in real-time.\nPracticality: 6/10\nUseful for emotional exploration and therapy, but might be limited by the need for high-end VR equipment.\nSustainability: 7/10\nAs VR technology advances, its applications in emotional health could remain relevant.\nFeasibility: 5/10\nThe technology is complex and might require significant development to be reliable.
3. Biometric Interaction in VR\nOriginality: 8/10\nIntegrating biometric feedback into VR for emotional interaction is a unique approach.\nInnovativeness: 9/10\nIt's a significant leap in VR technology, creating a symbiotic environment between user and virtual world.\nPracticality: 5/10\nUseful in both therapeutic and entertainment settings, but may be complex to implement.\nSustainability: 7/10\nHas the potential to evolve with advancements in biometric and VR technologies.\nFeasibility: 4/10\nThe integration of accurate biometric sensors in VR environments is a challenging task.
4. Emotion-Harmonizing Smart Jewelry\nOriginality: 7/10\nWearable technology for emotional representation isn't new, but this approach is distinctive.\nInnovativeness: 6/10\nIt extends the current trend in smart wearables but with a focus on emotional states.\nPracticality: 8/10\nIt's a practical, subtle way of understanding and expressing emotions.\nSustainability: 6/10\nIf the technology keeps pace with fashion trends, it can remain relevant.\nFeasibility: 7/10\nThe technology required is currently available and could be implemented with relative ease.
5. Emotion-Sync Social Network\nOriginality: 6/10\nThe integration of emotion recognition in social media is a fresh idea, though similar concepts exist.\nInnovativeness: 7/10\nIt challenges the traditional form of social media interaction.\nPracticality: 5/10\nPractical in theory, but privacy concerns and accuracy of emotion recognition could be issues.\nSustainability: 5/10\nIt depends heavily on user acceptance and continuous technological advancement.\nFeasibility: 6/10\nTechnologically feasible but may face social and ethical challenges in implementation.\n'''
        
        for i in range(roop_max):
            pre_evaluate_idea_devided=self._ideaDevideByFive(i)
            user_message=f'''{user_template_message}\n<Isuue>\n{self.problem}\n\n<Idea>\n{pre_evaluate_idea_devided}\n\n<Criteria>\n{self.selected_criterias}'''
            message=[
            {"role":"system", "content":system_message },
            {"role":"user", "content":user_example_message },
            {"role":"assistant", "content": assistant_answer_message},
            {"role":"user","content":user_message}
            ]
            logger.log(logging.INFO,f"アイデア評価の{i+1}回目の呼び出し")
            response=client.chat.completions.create(model=gpt_model,messages=message,max_tokens=4000)
            self.idea_eval_list.append(response.choices[0].message.content)
            i+=1
        return user_example_message

    def _extractPoints(self,text:str)->List[Tuple[int,int]]:
        # 正規表現で点数を抽出（評価基準を緩くする）
        pattern = re.compile(r'(\d+)/10')
        matches = pattern.findall(text)
        # 各アイデアごとの総点数とそのインデックスをタプルとして格納
        idea_points = [(sum(int(score) for score in matches[i:i+len(self.selected_criterias)]), i // len(self.selected_criterias))
                       for i in range(0, len(matches), len(self.selected_criterias))]
        return idea_points

    def sortByScores(self)->None:
        """良いアイデアだけを取る"""
        idea_score_list=[]
        for idea_thought in self.idea_eval_list:
            idea_score_list.extend(self._extractPoints(idea_thought))
        idea_score_list.sort(key=lambda pair:pair[0],reverse=True)
        print("idea score list:",idea_score_list)
        i=0
        #上位の5つのみ
        while i<5:
            print("point:",idea_score_list[i][0])
            #great_ideaは、評価の高い10個を選出する
            self.great_ideas.append(self.pre_evaluate_idea[idea_score_list[i][1]])
            i+=1
            
    
    def translateText(english_result:str)->None:
        """表示するいいアイデアを日本語に翻訳する"""
        ja_result=translator.translate_text(english_result,target_lang="JA")
        r.rpush(ja_result[0].text)