# IdeationGPT
**IdeationGPT**は、発想法と大規模言語モデル（LLM）を活用して、革新的で実行可能なアイデアを生成するツールです。  
このアプリケーションは、あなたの問題解決の手助けとなるよう設計されており、革新的で実行可能なアイデアを生成します。0から1へのアイデア生成、1を10に拡張するアイデア向上、そして精密なアイデア評価のclassが協調することで、最終的に5つの質の高いアイデアを提供します。

~~詳細な設計については[こちら](リンク先URL)をご覧ください。~~

## 特長 
- **革新的アイデアの生成:** One-shotをはじめとするプロンプトエンジニアリングと発想法を基にしたプロンプトを用いて、独創的なアイデアをLLMで生成します。
- **効率的な選択プロセス:** 約100個のアイデアから、最も有望な5つを選出。ユーザーは最良の選択肢のみを確認できます。
- **カスタマイズされた評価:** ユーザーが設定した評価基準に基づいてアイデアを評価、ユーザーのニーズに合致した提案を行います。
- **詳細なアイデア提示:** 各提案は、概要、使用テクノロジー、問題解決方法、ユースケースからなる計400単語の詳細な説明で提示され、ユーザーがプロジェクトを容易に理解できるようになります。
- **アイデアの再閲覧と再検討:** このサービスでは、ユーザーが登録することによって、一度生成された優れたアイデアを何度でも閲覧することが可能です。ユーザーはログインすることで、過去に生み出されたアイデアを簡単に参照し、再検討することができます。これにより、以前に作成されたアイデアを思い出したり、新しいインスピレーションを得る際に、重要なリソースとして利用することが可能になります。

## デモビデオ
https://github.com/mitas30/IdeationGPT/assets/83048191/d0539d84-369f-43be-8003-400570bb698c

# Quick Start
In Progress.

# 技術概要
## Workflow 
![ソフトウェア概要](https://github.com/mitas30/IdeationGPT/assets/83048191/e81abcc6-c652-4dd1-9e3b-f18f8d2c2bba)

## 使用したツールなど  
### python:
- [Gemmini-Pro](https://platform.openai.com/docs/api-reference/chat)/[GPT4](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [mongoDB](https://pymongo.readthedocs.io/en/stable/)  
- [redis](https://github.com/redis/redis-py)  
- [re](https://docs.python.org/ja/3.12/library/re.html)  
- [threading](https://docs.python.org/ja/3/library/threading.html)  
- [deepl](https://www.deepl.com/docs-api)  
### javascript:
- [async/await](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/async_function)
### 発想法:  
#### [前提逆転発想法](https://diamond.jp/articles/-/16331)  
問題の前提を疑い、それを反転させることで新しい視点やアイデアを生み出す手法。  
具体的には、課題を言葉で表現し、前提条件を挙げて反対にしてみることで、新たな解決策を探求する。
<details><summary>ソフト内で使用している「反転させた前提」を生成するプロンプト(one-shotに使用しているSystem+Userの例)</summary><div>
"role":"system", "content":'You are a maker with high creativity and implementation skills.<br>  Please utilize your creativity to come up with effective ideas for the problem at hand.<br><br>
"role":"user", "content":please adhere to the following &ltinstruction&gt.<br>
<br>&ltproblem&gtReducing Urban Traffic Congestion<br><br>
&ltinstruction&gt<br>
1.List Assumptions:
Identify three key assumptions about &ltproblem&gt.However, you need to follow the &ltassumption_format&gt.<br>     
2.Reverse Assumptions:<br>
Invert each assumption to explore new ideas.<br>However, you need to follow the &ltreversed_assumption_format&gt.<br><br>
&ltassumption_format&gt<br>
Assumptions:<br>
A: The first assumption inherent in the problem<br>
B: The second assumption inherent in the problem<br>
C: The third assumption inherent in the problem<br><br>
&ltreversed_assumption_format&gt<br>
Reversed Assumptions:<br>
A:The Reversed Paradox of the Assumption A Inherent in the Problem<br>
B:The Reversed Paradox of the Assumption B Inherent in the Problem<br>
C:The Reversed Paradox of the Assumption C Inherent in the Problem<br>
</div></details>
<details><summary>ソフト内で使用している「前提逆転を用いたアイデア出し」プロンプト(one-shotに使用しているSystem+Userの例)</summary><div>
role":"system", "content":'You are a maker with high creativity and implementation skills.Please utilize your creativity to come up with effective ideas for the problem at hand.<br><br>
"role":"user", "content":<br>
&ltproblem&gt Reducing Urban Traffic Congestion<br>
&ltReversed Assumptions&gt Traffic congestion is a round-the-clock issue.<br><br>
Please create five innovative ideas by adhering to the following &ltinstruction&gt.<br>
Additionally, let's take a moment to read and understand the &ltIntro --false face--&gt, which explains the objective of the 'False Face' method.<br><br>
&ltInrto --false face--&gt<br>
The 'false face' Thinking Method is an approach used in problem-solving and creative thinking that challenges universally accepted premises and fundamental assumptions, overturning them to elicit new perspectives and ideas. This method urges us to confront assumptions and beliefs we usually hold unconsciously and encourages us to overturn them fundamentally. This process shines a new light on what are perceived as immutable facts or 'common sense,' aiding in the discovery of original solutions.<br>
For instance, questioning and reversing commonly accepted business practices or life rules can lead to completely new approaches and business models. This method is not just about adopting the opposite stance, but aims to rethink problems from a fundamentally different angle, stepping outside of conventional thought frameworks. Such a shift can connect seemingly unrelated or impractical ideas to innovative solutions.<br>
In essence, 'false face' thinking stimulates creativity by breaking free from entrenched mindsets, allowing for the discovery of innovative ideas and solutions beyond the usual confines of established thinking.<br><br>
&ltinstruction&gt --Brainstorming Ideas Based on Reversed Assumption--<br>
Using the 'False Face' method, focus on the &ltReversed Assumption&gt to reinterpret &ltproblem&gt from a new angle. Generate five unique ideas that address &ltproblem&gt specifically through this reversed assumption. It's vital to adhere to the guidelines in &ltnote&gt and elaborate on each idea in detail as per the &ltformat&gt.<br><br>
&ltformat&gt<br>
[Idea number]: [Idea Name] (optional)<br>
Core idea: [Brief explanation of the core idea]<br>
Technologies and Materials Used: [Technologies and materials used]<br>
Revised Approach to Problem-Solving: [How the problem is solved with this idea]<br>
Concrete Use Cases: [List of use cases for the idea]<br><br>
&ltnote&gt<br>
You need to follow the &ltformat&gt below and attach a lengthy explanation of approximately 400 words for each idea.Also, output 5 ideas.<br>
Each idea needs to be described in sufficient detail so that it can form the basis for a requirements definition.<br>
Therefore, although a 400-word explanation may seem lengthy at first glance, it is necessary to write in such detail to properly convey the concept.<br>
</div></details>

#### [IdeaBox発想法](https://ssaits.jp/promapedia/method/idea-box.html)  
課題の特性や要素を詳細に分析し、その様々なパラメーターの組み合わせを通じて新たなアイデアを創出する手法。
<details><summary>ソフト内で使用している「要素とパラメータ」を特定するプロンプト(one-shotに使用しているSystem+Userの例)</summary><div>
"role":"system", "content":'You are a maker with high creativity and implementation skills. Additionally, you are skilled at abstracting concepts.'<br><br>
"role":"user", "content": Please follow the instructions according to the following &ltguide&gt.<br><br>
&ltproblem&gtBridging the Educational Gap<br>
<br>&ltguide&gt<br>
Idea Box Method: A Creative Blueprint
Overview:The Idea Box method is a systematic approach to generating innovative ideas. It involves identifying key parameters of a problem or project and exploring various combinations of these parameters to discover novel solutions.<br>
Steps:<br>
1.Identify Parameters:<br>
List up four essential aspects or features related to the challenge &ltproblem&gt. Consider whether this challenge would exist without this parameter. Also, output according to the following &ltformat&gt.<br><br>
Example problem: Improve the design of a laundry basket.<br>
Example Parameters: Material, Shape, Finish, Placement<br><br>
&ltformat&gt<br>
Parameters: [Output parameters A, B, C, D for the challenge, separated by commas]<br><br>
2.List Variations:<br>
Write down ten variations for each parameter. However, output according to the following &ltformat&gt.<br><br>
&ltformat&gt<br>
variations:<br>
1. [Output attributes A, B, C...I,J for the first parameter, separated by commas]<br>
2. [Output attributes A, B, C...I,J for the second parameter, separated by commas]<br>
3. [Output attributes A, B, C...I,J for the third parameter, separated by commas]<br>
4. [Output attributes A, B, C...I,J for the fourth parameter, separated by commas]<br><br>
Example problem: Improve the design of a laundry basket.<br>
Example Parameters: Material, Shape, Finish, Placement<br>
Example variations:<br>
1.Wicker, Plastic, Paper, Metal, Mesh, Bamboo, Rattan, Silicone, Fabric, Recycled materials<br>
2.Square, Cylinder, Rectangle, Hexagon, Cube, Oval, Round, Triangular, Spherical, Irregular<br>
3.Natural, Tinted, Transparent, Reflective, Neon, Matte, Glossy, Textured, Lacquered, Weathered<br>
4.Floor mounted, Ceiling suspended, Wall mounted, Basement entrance, Door hangings, Under-bed, Corner, Freestanding, Modular, Portable<br>
</div></details>

<details><summary>ソフト内で使用している「IdeaBoxを使ったアイデア出し」プロンプト(one-shotに使用しているSystem+Userの例)</summary><div>
    "role":"system", "content":'You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.<br><br>
    "role":"user", "content":<br>&ltProblem&gt Bridging the Educational Gap<br><br>&ltGuide&gt<br>
    &ltparameter&gt Educational Content, Accessibility, Technological Integration, Teacher Training<br>
    &ltattributes&gt<br>
    varitations:<br>
    1:Culturally Diverse,Community Centers,Big Data Analytics,Peer Collaboration Networks<br>
    2:Experiential Learning,Braille Resources,Blockchain for Education,Pedagogical Innovation<br>
    3:Holistic Education,Mobile Learning,Artificial Intelligence,Digital Literacy<br>
    4:Adaptive Learning,Online Platforms,Educational Apps,Online PD Courses<br>
    5:Multilingual,Radio Broadcasts,Educational Apps,Diversity Training<br><br>
    Overview:<br>
    The Idea Box Method is a dynamic approach for generating creative solutions, especially suited for addressing &ltproblem&gt. By leveraging a combination of various attributes under identified parameters, you can unlock a spectrum of innovative ideas.<br><br>
    Method:<br>
    Combinations of attributes related to &ltparameter&gt are listed in &ltattributes&gt following the &ltattribute_format&gt for five sets. You are to come up with one idea for each set of attributes listed in &ltattributes&gt, totaling five ideas. This means you should develop one idea using all attributes from attribute_set 1, another idea using all attributes from attribute_set 2, and so on, resulting in a total of five ideas.  
    Each idea should follow the provided &ltformat&gt.
    Also, pay attention to the guidelines on how to write ideas in &ltnote&gt.<br><br>
    &ltattribute_format&gt<br>
    1.attribute set1<br>
    2.attribute set2<br>
    3.attribute set3<br>
    4.attribute set4<br>
    5.attribute set5<br><br>
    &ltformat&gt<br>
    [Idea number]: [Idea Name] (optional)<br>
    Core idea: [Brief explanation of the core idea]<br>
    Technologies and Materials Used: [Technologies and materials used]<br>
    Revised Approach to Problem-Solving: [How the problem is solved with this idea]<br>
    Concrete Use Cases: [List of use cases for the idea]<br><br>
    &ltnote&gt<br>
    You need to follow the &ltformat&gt below and attach a lengthy explanation of approximately 400 words for each idea.Also, output 5 ideas.
    Each idea needs to be described in sufficient detail so that it can form the basis for a requirements definition.
    Therefore, although a 400-word explanation may seem lengthy at first glance, it is necessary to write in such detail to properly convey the concept.
</div></details>

#### [Brutethink](https://www.mycoted.com/Brutethink)
ランダムな言葉を取り入れて、それと課題との強制的な関連付けを通じて新しいアイデアを生み出す技法。
<details><summary>ソフト内で使用している「BruteThink」プロンプト。(one-shotに使用しているSystem+Userの例)</summary><div>
"role":"system", "content":You are a maker with high creativity and implementation skills.  Please utilize your creativity to come up with effective ideas for the problem at hand.<br><br>
"role":"user", "content":<br>&ltEssential Rules to Strictly Follow&gt<br>
&ltnote&gt<br>
You need to follow the &ltformat&gt below and attach a lengthy explanation of approximately 400 words for each idea.Also, output 5 ideas.
Each idea needs to be described in sufficient detail so that it can form the basis for a requirements definition.
Therefore, although a 400-word explanation may seem lengthy at first glance, it is necessary to write in such detail to properly convey the concept.<br>
<br>&ltproblem&gt How can we make public transportation more appealing to commuters?
<br>&ltword&gt coffee<br>
<br>&ltGuide&gt<br>
Please read the following text and execute the &ltBluePrint&gt. Sections such as &ltIntroduction&gt, &ltThe Brutethink Approach&gt, &ltCase Studies and Examples: Problem Scenarios and Simplified Solutions&gt, and &ltSummary&gt are provided to help you understand the Brutethink Method, so refer to them as needed.<br>
<br>&ltIntroduction --Brutethink Method--&gt<br>
In the pursuit of original and innovative ideas, one essential approach is to create new patterns in our minds, forcing connections between unrelated elements. This method can lead to discovering groundbreaking ideas from seemingly nothing. The practice of juxtaposing unrelated concepts, like contrasting a garbage truck and a sunset in modern art, can spark new ideas by contrasting practicality with beauty.<br>
<br>&ltThe Brutethink Approach&gt<br>
This method involves combining unrelated elements, learning from the connections that emerge. For instance, the invention of float glass, a breakthrough in the glass-making industry, came from such a connection. Alastair Pilkington, inspired by soap floating in water, developed a method where glass forms on molten tin, revolutionizing glass production.
<br>&ltBluePrint&gt<br>
Step 1<br>
Discover five different attributes or aspects of each word in &ltwords&gt. Follow the &ltattribute_format&gt in this process.<br>
Step 2<br>
Next, link each attribute identified in Step 1 with &ltproblem&gt to create ideas that solve &ltproblem&gt. For each word, develop one idea per attribute, resulting in a total of five ideas per word. This method enables the generation of diverse and creative solutions.
However, be cautious not to use the words in &ltwords&gt directly as solutions.<br> For example, if 'coffee' is listed in &ltwords&gt, suggesting the opening of a coffee shop would be too literal and not in line with the Brutethink methodology. Instead, use attributes of 'coffee', such as its aroma or warmth, to inspire your ideas. Ensure that all ideas are formatted according to &ltformat&gt and adhere to the guidelines specified in &ltnote&gt.<br>
<br>&ltattribute_format&gt
<br>&ltattribute&gt<br>
[attribute 1]: [Attribute1 Description]<br>
...<br>
[attribute 5]: [Attribute5 Description]<br>
<br>&ltformat&gt<br>
[Idea number]: [Idea Name] (optional)<br>
Core idea: [Brief explanation of the core idea]<br>
Technologies and Materials Used: [Technologies and materials used]<br>
Revised Approach to Problem-Solving: [How the problem is solved with this idea]<br>
Concrete Use Cases: [List of use cases for the idea]<br>
<br>&ltCase Studies and Examples: Problem Scenarios and Simplified Solutions&gt  
<br>&ltproblem&gtHow can I improve my relationship with my boss?
<br>&ltword&gtpencil
<br>&ltattribute&gt<br>
1.Eraser: The eraser on a pencil represents the ability to correct mistakes. This attribute is linked to the "Clean Slate Policy" as it symbolizes the notion of acknowledging errors and moving forward without lingering on past faults.<br>
2.Lead: The lead in a pencil, essential for writing, represents core functionality but can also symbolize slow processes (due to its heaviness). This relates to the "Mentorship for Efficiency", where addressing and guiding slower processes in the workplace is key.<br>
3.Yellow Color: The color yellow on many pencils, particularly in America, is often associated with caution or the need to proceed with care. This color inspires the "Yellow Room for Open Communication", emphasizing a space where caution in communication is respected, yet openness is encouraged.<br>
4.Cost-effectiveness: Pencils are known for being cost-effective tools. This aspect is mirrored in the "Competitive Commission Plan", where the aim is to create value and effectiveness in the workplace, similar to how a pencil provides a simple yet valuable function.<br>
5.Hexagonal Shape: The hexagonal shape of many pencils ensures a comfortable grip and prevents rolling away. This shape is the inspiration behind the "Six-Point Work Dynamics Plan", representing stability and multi-faceted approaches to improving workplace dynamics.<br><br>
&ltidea&gt<br>
Idea 1.Clean Slate Policy (Eraser)
<br>Core Idea: Implementing a monthly reflection session where employees can discuss past errors without judgment, similar to how an eraser cleanly removes pencil marks, promoting a culture of openness and improvement.
<br>Idea 2.Mentorship for Efficiency (Lead)
<br>Core Idea: Pairing less experienced employees with mentors to work on specific projects, similar to how a pencil’s lead is essential for writing, ensuring that everyone contributes efficiently to team goals. 
<br>Idea 3.Yellow Room for Open Communication (Yellow Color)
<br>Core Idea: Designing the room with a welcoming yellow decor and providing resources like conversation starters and feedback boxes, fostering a warm and inviting    atmosphere for open discussions.
<br>Idea 4.Competitive Commission Plan (Cost-effectiveness)
<br>Core Idea: Conducting quarterly reviews of commission structures in comparison to industry standards, ensuring the plan remains as practical and valuable as a standard pencil.
<br>Idea 5.Six-Point Work Dynamics Plan (Hexagonal Shape)
<br>Core Idea: Each point of the plan is reviewed and updated bi-annually, ensuring the plan remains relevant and effective, similar to how the hexagonal shape of a pencil provides a consistent and reliable grip.<br>
</div></details>

#### [SCAMPER](https://stockmark.co.jp/coevo/scamper)
アイデア改良のための7つの質問を用いて、ビジネスや研究開発における新しいアイデアを発散させ、創出する手法。  
<details><summary>ソフト内で使用している「SCAMPER」プロンプト(one-shotに使用しているSystem+Userの例)</summary><div> 
"role":"system","content":You are a maker with high creativity and implementation skills. Moving forward, there's a need for you to refine ideas. Please utilize your creativity to come up with effective ideas for the problem at hand.<br><br>
Please follow the (guide) below and come up with five ideas that expand on (base_idea). Of course, it is important that these ideas are also ideas that solve (issue).Each idea should be described in about 450 words. However, each idea must conform to the (format). The brackets [] in the format are explanations of what should be written. For example, where it says [specific number], actually insert a specified matter like 2000. Parts like core idea: do not need to be changed.In addition, since developed ideas will be presented on a separate occasion from (base_idea), please do not mention (base_idea) in the idea document, e.g., "improve (base_idea)". In other words, (bad_ex) and (good_ex) are documents about the same idea, but should be written like (good_ex).<br><br>
"role":"user", "content":<br>problem:How to use information technology to enrich people's emotions<br><br>
Format:<br>Idea x:[Idea Name]([technique using in SCAMPER])<br>
core idea:[Explanation of the Core Idea]<br>
Technologies and Materials Used:[What kind of technologies and materials are used]<br>
Revised Approach to Problem-Solving:[How the given problem is solved]<br>
Concrete Use Cases:[List the use cases]<br><br>
Guide:SCAMPER Technique: An Enhanced Guide for Creative Innovation<br>
Introduction:<br>
SCAMPER is a powerful tool for sparking creativity, encouraging innovative thinking by altering existing elements. It stands for Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, and Reverse. <br>
<br>Incorporating Additional Insights:<br>
Emphasize that all new ideas are modifications of existing ones, adding or altering components.<br>
Highlight that the first idea is not always the best, and exploring alternatives can lead to more effective solutions.<br>
Encourage thinking beyond the immediate challenge, considering how an idea might solve unrelated problems or lead to breakthrough innovations.<br>
<br>Substitute:<br>
Change parts, materials, or people to improve or alter the function.<br>
Case Study: Starbucks' continuous substitution led to the creation of the Frappuccino.<br>
Additional Insight: Rod Spruel's innovation in creating fireplace fuel from used coffee grounds and candle wax.<br>
<br>Combine:<br>
Merge different ideas, products, or services for enhanced functionality.<br>
Case Study: Hungarian architects' combination of cement and glass fiber to create light-transmitting concrete.<br>
Additional Insight: How Gutenberg's combination of a wine press and coin punch led to the invention of the printing press.<br>
<br>Adapt:<br>
Borrow elements from other contexts to solve problems in a new setting.<br>
Case Study: Jacuzzi's adaptation of farm pumps for hydrotherapy baths.<br>
Additional Insight: Jacuzzi's transformation of a simple idea into a luxury bathroom product.<br>
<br>Modify:<br>
Alter the size, shape, or properties to serve a new purpose.<br>
Case Study: Moen’s showerheads modified for a unique water flow pattern.<br>
Additional Insight: The evolution of Mr. Clean Magic Reach, a bathroom cleaning tool adapted from an observed cleaning technique in Puerto Rico.<br>
<br>Eliminate:<br>
Remove unnecessary elements to simplify and improve efficiency.<br>
Case Study: Dutch Boy's reimagined paint packaging for ease of use.<br>
Additional Insight: NASA's simplification of space suits for Mars expeditions.<br>
<br>Reverse:<br>
Change the order or perspective to see things differently.<br>
Case Study: Cirque du Soleil's reversal of traditional circus concepts.<br>
Additional Insight: FBI's undercover operation using a wedding scenario to capture criminals.<br>
<br>Implementing SCAMPER:<br>
Apply SCAMPER to each element of a challenge, exploring new ideas.<br>
Encourage exploring multiple options and returning to the original idea if it remains the best solution.<br>
Emphasize the importance of case studies in understanding and applying SCAMPER.<br>
<br>Concluding Thoughts:<br>
SCAMPER, a checklist of questions, can transform existing ideas into innovative solutions.<br>
Its flexibility makes it a valuable tool across various industries.<br>
By repeatedly applying SCAMPER, one can discover unique, original ideas, fostering innovation and problem-solving.<br>
<br>bad_ex:Mindful Mood Mixer (MMM) (Adapt)<br>
Core Idea: Mindful Mood Mixer (MMM) is a virtual reality (VR) system that integrates mindfulness and meditation into a personalized VR experience. It adapts a concept similar to Emotional VR, where the VR environment responds to the user's emotional state. In MMM, this environment is tailored to guide users through mindfulness and meditation practices based on their current emotional state, detected through biometric readings. The aim is to provide immediate emotional relief while fostering long-term emotional regulation and resilience through mindfulness techniques.<br>
<br>good_ex:Mindful Mood Mixer (MMM) (Adapt)<br>
Core Idea: Mindful Mood Mixer (MMM) is a pioneering virtual reality system focused on enhancing mental well-being through personalized mindfulness and meditation experiences. This system uses advanced biometric monitoring to gauge a user's emotional state, then adapts its VR environment accordingly to provide tailored mindfulness and meditation practices. The concept is to offer immediate emotional support while also cultivating long-term emotional resilience and mindfulness skills.<br>
<br>base_idea:Emotional VR<br>
Core Idea:Emotional VR is an innovative virtual reality system that provides customized emotional experiences based on individual users' emotional states. By analyzing biometric signals such as heart rate and skin conductance to interpret emotions, the system dynamically alters the VR environment based on these readings. This assists users in appropriately controlling their emotions and guiding them in a positive direction. The technology enables users not only to understand their emotions but also to actively manage them and learn methods to reduce stress.<br>
<br>Technologies and Materials Used:The system utilizes sensor technology for biometric signal recognition, machine learning algorithms for emotion analysis, and a 3D graphics engine to create a dynamic VR environment that responds to emotions. Additionally, it incorporates high-quality audio output and voice guides that use a psychological approach to enhance.<br>
<br>Revised Approach to Problem-Solving:The system accurately reads users' current emotions and provides an environment that either amplifies those emotions or induces relaxation, thereby solving mental health issues. For example, a calming forest scene is provided for users feeling stress, aiding relaxation and supporting emotional control. When positive emotions are detected, the system offers social events within VR to further enhance users' sense of happiness.<br>
<br>Concrete Use Cases:For instance, a user returning home from a tiring day at work can use this system to experience a tranquil walk in the forest tailored to their day's stress level. On weekends, they can relive and share happy moments with family and friends in VR. Additionally, as part of mental health care, users can participate in guided meditation sessions led by psychotherapists in VR
</div></details>

### 評価法:
#### 選択可能な評価基準:
<details><summary>1. 独創性</summary><div>
そのアイデアは、他の人が思いつかないようなユニークな視点や解決策を提示しているか。  
高い独創性は、アイデアの新規性や、一般的または伝統的な概念から際立つ能力によって示される。
</div></details>
<details><summary>2. 革新性</summary><div>
アイデアが既存の規範や慣習をどの程度打ち破るかを評価する。<br>独創性はユニークなアイデア（他の人が思いつかないようなアイデア）に高得点がつくが、革新性は問題に取り組む際の暗黙の制約を超越したアイデアに高得点がつく。新しさの度合いと、現在の慣行や考えを破壊する可能性を意味する。
</div></details>
<details><summary>3. 実現可能性</summary><div>
そのアイデアは現実のシナリオで実行しやすいか。  
高い実現可能性は、利用可能な資源、技術、時間の制約を考慮した上で、アイデアを実現することが容易であることを示す。
</div></details>
<details><summary>4. 実用性</summary><div>
そのアイデアは、与えられた問題に対して実行可能な解決策を提供しているか。  
そのアイデアが、目の前の中核的な問題に直接取り組み、効果的に解決するものであれば、実用性において高得点となる。
</div></details>
<details><summary>5. 持続可能性</summary><div>
そのアイデアは、長期にわたって関連性と影響力を維持できるか。  
持続可能性の高いアイデアとは、時間が経過しても、そのメリットや効果がすぐに減少しないものである。
</div></details>
<details><summary>6. 効率性</summary><div>
アイデアの費用対効果を評価する。<br>
これは、そのアイデアの予想される経済効果を、予想される実施コストで割ることによって決定される。<br>そのアイデアが、コストに比して大きな利益や節約を約束するものであれば、効率性において高得点となる。
</div></details>
<details><summary>7. 収益の高い拡張性</summary><div>
この基準は、大規模なソフトウェアソリューションとしてスケールアップしたときに、そのアイデアが大きな収益を生み出す可能性を評価するものである。<br>
特に、より大規模または包括的な規模で実施された場合に、市場へのリーチと収益の創出という点で、アイデアの拡大能力を評価する。
</div></details>
<details><summary>8. ユーザーエクスペリエンス</summary><div>
アイデアがエンドユーザーや顧客にとって肯定的で満足のいく体験をもたらすかどうかを評価する。<br>
ユーザビリティ、アクセシビリティ、エンゲージメント、総合的な満足度といった側面を考慮する必要がある。<br>
高いUXスコアは、ユーザーフレンドリーで、直感的で、ターゲットオーディエンスにとって魅力的なアイデアに起因する。
</div></details>

#### 使用したプロンプト:
<details><summary>評価プロンプト(one-shotに使用しているSystem+Userの例)</summary><div>
"role":"system", "content":You are required to fairly evaluate my ideas, possessing both high creativity and implementation skills. The evaluation is strict, and you would assign a score of 6 out of 10 to ideas you consider good based on the evaluation criteria.<br><br>
"role":"user", "content":Please implement the following guidelines.<br><br>
&ltIssue&gt<br>
How to use information technology to enrich people's emotions<br><br>
Guidelines: see the list of &ltidea&gt to solve (issue). The list of &ltidea&gt is formatted as follows:<br>
1.[Idea Name1]<br>
Core Idea:<br>
Techniques and materials to be used:<br>
Revised approach to solving the problem:<br>
Specific Use:<br>
2.[Idea Name2]<br>
...<br>
This list contains the names of several ideas and their details. Rate each idea in &ltIdea&gt on a scale of 1 to 10 according to the criteria in (Criteria).<br>
 Also, please output your responses to each idea in the following &ltFORMAT&gt format. The [] part is a variable, so change it depending on your ideas and criteria.<br><br>
&ltFORMAT&gt<br>
[Idea number (starting from 1)]. [Idea name].<br>
[criteria1]: [X1(score)]/10<br>
[Why did you choose that score for that criterion?]<br>
....<br>
[criteria y]:[Xy(score)]/10<br>
[Why did you choose that score for that criterion?]<br><br>
&ltIdea&gt<br>
["Emotion Share Sticker<br>
Core Idea:The Emotion Share Sticker is a pioneering smartphone accessory, ingeniously crafted to offer a unique way of expressing emotions. This accessory bridges the gap between digital communication and sensory experience, enriching interactions in a world increasingly reliant on remote connections. By adhering to the back of a smartphone, it introduces a blend of visual appeal and olfactory sensation, representing various emotions. The sticker’s design is a kaleidoscope of colors, where hues like bright yellows and oranges symbolize joy and optimism, while blues and greens evoke calmness and serenity. Its innovative feature lies in the integration of olfactory capsules, which, when activated via an accompanying app, release scents correlating to the chosen emotions. This creative approach allows users to convey their feelings in a more comprehensive and multisensory manner.<br>
Technologies and Materials Used:The Emotion Share Sticker incorporates advanced microencapsulation technology, encapsulating a variety of fragrances in tiny, durable spheres. These capsules are carefully designed to release specific scents when prompted by the user through a custom-designed smartphone app. The technology behind this involves meticulous programming that allows users to select and modify the intensity and duration of the scent, thus offering a personalized experience. The app's interface is user-friendly, ensuring seamless interaction between the user and the sticker’s features.<br>
Revised Approach to Problem-Solving:In a world where digital communication often lacks the depth of face-to-face interaction, the Emotion Share Sticker offers a novel solution. It enhances remote communication by introducing an olfactory dimension to digital messages, thereby enriching the emotional context of exchanges. This sticker is particularly beneficial in scenarios where verbal or textual communication falls short, offering a subtle yet impactful means to convey feelings.<br>
Concrete Use Cases:The sticker finds its utility in various scenarios. In remote work settings, it can be used to express work-related stress or accomplishment without the need for explicit communication. It also plays a significant role in personal relationships, allowing individuals to share their feelings in a non-verbal but profoundly expressive manner. For instance, sending a scent of lavender could indicate a need for calmness in stressful times, while a citrus fragrance could celebrate a joyful moment. The Emotion Share Sticker thus stands out as an innovative tool, enhancing the depth and quality of remote interactions.",<br><br>
 "Emotional VR<br>
Core Idea:Emotional VR is a state-of-the-art virtual reality system meticulously engineered to provide a personalized emotional experience. It stands as a technological marvel that not only recognizes but also adapts to the user's current emotional state, offering an immersive journey through virtual environments that resonate with their feelings. By harnessing the power of emotion recognition technology, Emotional VR interprets emotions from facial expressions and voice tones, transforming these cues into dynamic VR experiences. This system tailors virtual scenarios in real-time, ensuring that each virtual space is a reflection of the user's emotional landscape.<br>
Technologies and Materials Used:At the heart of Emotional VR lies cutting-edge emotion recognition technology, which utilizes advanced algorithms to analyze facial expressions and voice modulations. This technology is integrated with VR hardware to create an environment that dynamically adjusts based on the user's emotional state. The VR scenarios are crafted with high-definition graphics and sound, providing a deeply immersive and sensory-rich experience. The system also includes professionally designed voice guides, which further enrich the user’s journey through various emotional landscapes.<br>
Revised Approach to Problem-Solving:Emotional VR revolutionizes the way individuals engage with their emotions. It acknowledges the importance of emotional health and offers a virtual space where users can confront and explore their feelings in a controlled, safe environment. Whether it's stress relief through serene natural settings or joy enhancement via lively social events, Emotional VR caters to a wide spectrum of emotional needs, promoting psychological well-being.<br>
Concrete Use Cases:The system's versatility allows for a multitude of applications. In a therapeutic context, it provides a tool for mental health professionals to guide clients through emotional landscapes, offering a novel approach to emotional healing. For everyday users, it offers an escape into calming environments or exciting adventures based on their current mood, serving as a daily emotional wellness tool. Emotional VR thus stands as a pioneering platform that bridges the gap between technology and emotional well-being.",<br><br> 
"Biometric Interaction in VR<br>
Core Idea:Biometric Interaction in VR is a groundbreaking system that seamlessly blends biometric sensors with virtual reality, creating a symbiotic environment responsive to the user's emotional state. This advanced system takes VR experiences to new heights by not just immersing users in virtual worlds but also making these worlds react in real-time to their emotions. Users don VR headsets equipped with sensors that track physiological indicators such as heart rate, skin conductance, and breathing patterns. An intelligent emotion recognition algorithm interprets these data, enabling the VR environment to adapt and respond to the user's emotional nuances.<br>
Technologies and Materials Used:This system integrates sophisticated biometric sensors with VR technology. The sensors, worn by the user, capture real-time physiological data, which are then processed by an advanced emotion recognition algorithm. The VR environment is powered by high-end graphics engines, capable of creating diverse and responsive scenarios that shift according to the user's emotional state. Additionally, the system encourages users to express emotions through specific VR movements, enhancing the interactive and immersive nature of the experience.<br>
Revised Approach to Problem-Solving:Biometric Interaction in VR introduces a transformative approach to understanding and expressing emotions. By linking physiological responses to VR experiences, it provides users with a unique method to manage and explore their emotional states. This technology serves not only as a tool for personal emotional awareness but also has practical applications in emotional health promotion and stress management.<br>
Concrete Use Cases:The system finds its use in various settings, from therapeutic to recreational. In a therapeutic setting, it aids in emotional regulation and stress management, providing users with a controlled environment to explore and understand their emotional responses. For recreational users, it offers a novel form of entertainment, where games and experiences are tailored to their emotional state, creating a highly personalized and engaging experience. In both contexts, Biometric Interaction in VR stands as an innovative solution for enhancing emotional connectivity and well-being.", 
<br><br>"Emotion-Harmonizing Smart Jewelry<br>
Core Idea:Emotion-Harmonizing Smart Jewelry represents an innovative blend of fashion and technology, designed to offer a novel way of expressing and understanding emotions through wearable accessories. This smart jewelry, encompassing items like bracelets and necklaces, is embedded with emotion-recognition sensors that detect and interpret the wearer's emotional states in real-time. The core functionality of this jewelry lies in its ability to change color or pattern based on the wearer's emotions, providing a visual representation of feelings.<br>
Technologies and Materials Used:The jewelry incorporates advanced sensors capable of monitoring physiological indicators such as heart rate and skin temperature. These sensors utilize sophisticated algorithms to infer the wearer's current emotional state. The aesthetic elements of the jewelry, such as color-changing materials or e-ink displays, dynamically alter their appearance to reflect emotional changes – warmer tones for joy and cooler tones for relaxation. The jewelry is also integrated with a smartphone app, enhancing the emotional experience by offering personalized recommendations like music or meditation suggestions based on the detected emotions.<br>
Revised Approach to Problem-Solving:Emotion-Harmonizing Smart Jewelry introduces a unique approach to emotional awareness and communication. By making emotional states visible, the jewelry encourages wearers to become more conscious of their feelings, fostering emotional intelligence and empathy. It also serves as a subtle yet powerful tool for non-verbal emotional expression, enhancing interpersonal connections.<br>
Concrete Use Cases:The jewelry finds its utility in various personal and social scenarios. In personal use, it helps individuals track and manage their emotional states, acting as a catalyst for mindfulness and self-care. Socially, it allows wearers to non-verbally communicate their feelings to others, facilitating deeper emotional connections. The accessory can also be used in therapeutic settings, aiding in emotional regulation and awareness exercises.",<br><br> 
'Emotion-Sync Social Network<br>
Core Idea:Emotion-Sync Social Network is a revolutionary concept that intertwines emotion recognition technology with social media. This platform enables users to share their emotional states in real-time, fostering a new dimension of connectivity and empathy in the digital world. It reads emotions from various inputs like text, voice, or facial expressions and displays this information on user profiles, creating an emotionally attuned social network.<br>
Technologies and Materials Used:The platform employs advanced emotion recognition algorithms that analyze user inputs – text, voice, and facial expressions – to accurately discern their current emotional state. This technology integrates with a user-friendly app or social media platform, allowing users to communicate and share their emotions authentically and effortlessly.<br>
Revised Approach to Problem-Solving:Emotion-Sync Social Network redefines the way people interact on social media. By focusing on emotional states, it creates a more empathetic and supportive online community. This approach enables users to find and connect with others experiencing similar emotions, be it for shared support during challenging times or celebrating joyous moments together.<br>
Concrete Use Cases:This platform caters to a wide range of emotional interactions. Users feeling down can seek and offer support to others in similar emotional states, creating a community of care and understanding. Conversely, those in a positive emotional state can spread joy and positivity, enhancing overall emotional well-being. This network acts as a digital haven for emotional support and positive communication, contributing significantly to mental health and emotional wellness.']<br><br>
&ltCriteria&gt<br>
["Originality:Does the idea present a unique perspective or solution that others have not thought of? High originality is marked by the idea's novelty and its ability to stand out from common or traditional concepts.",<br><br>
"Innovativeness:This criterion assesses the extent to which the idea breaks existing norms and conventions. While originality is high for unique ideas (those others have not thought of), innovativeness scores highly for ideas that transcend implicit constraints in addressing a problem. It's about the degree of newness and the potential to disrupt current practices or thoughts.", <br><br>'Practicality:Does the idea provide a viable solution to the given problem? An idea scores high in practicality if it directly addresses and effectively resolves the core issues at hand.', 
<br><br>'Sustainability:Can the idea maintain its relevance and impact over a long period? Ideas with high sustainability are those whose benefits and effectiveness do not diminish quickly over time.', 
<br><br>'Feasibility:Is the idea easy to implement in a real-world scenario? High feasibility is indicated by the ease with which the idea can be brought to life, considering available resources, technology, and time constraints.'],<br>
</div></details>

## 参考文献
- 