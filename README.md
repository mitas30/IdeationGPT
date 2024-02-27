# IdeationGPT
**IdeationGPT**は、発想法と大規模言語モデル（LLM）を活用して、革新的で実行可能なアイデアを生成するツールです。  
このアプリケーションは、あなたの問題解決の手助けとなるよう設計されており、革新的で実行可能なアイデアを生成します。0から1へのアイデア生成、1を10に拡張するアイデア向上、そして精密なアイデア評価のclassが協調することで、最終的に5つの質の高いアイデアを提供します。

~~詳細な設計については[こちら](リンク先URL)をご覧ください。~~

## デモビデオ
https://github.com/mitas30/IdeationGPT/assets/83048191/d0539d84-369f-43be-8003-400570bb698c

## 特長 
- **革新的アイデアの生成:** One-shotや人格定義をはじめとするプロンプトエンジニアリングと発想法を基にしたプロンプトを用いて、独創的なアイデアをLLMで生成します。
- **効率的な選択プロセス:** 約100個のアイデアから、最も有望な5つを選出。ユーザーは最良の選択肢のみを確認できます。
- **カスタマイズされた評価:** ユーザーが設定した評価基準に基づいてアイデアを評価、ユーザーのニーズに合致した提案を行います。
- **詳細なアイデア提示:** 各提案は、概要、使用テクノロジー、問題解決方法、ユースケースからなる計400単語の詳細な説明で提示され、ユーザーがプロジェクトを容易に理解できるようになります。
- **アイデアの再閲覧と再検討:** このサービスでは、ユーザーが登録することによって、一度生成された優れたアイデアを何度でも閲覧することが可能です。ユーザーはログインすることで、過去に生み出されたアイデアを簡単に参照し、再検討することができます。これにより、以前に作成されたアイデアを思い出したり、新しいインスピレーションを得る際に、重要なリソースとして利用することが可能になります。

# Quick Start


# 技術概要
## Workflow 
[図](URL)
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
- [前提逆転発想法](https://diamond.jp/articles/-/16331):  
問題の前提を疑い、それを反転させることで新しい視点やアイデアを生み出す手法。  
具体的には、課題を言葉で表現し、前提条件を挙げて反対にしてみることで、新たな解決策を探求する。
- [IdeaBox発想法](https://ssaits.jp/promapedia/method/idea-box.html):  
課題の特性や要素を詳細に分析し、その様々なパラメーターの組み合わせを通じて新たなアイデアを創出する手法。
- [Brutethink](https://www.mycoted.com/Brutethink):  
ランダムな言葉を取り入れて、それと課題との強制的な関連付けを通じて新しいアイデアを生み出す技法。
- [SCAMPER](https://stockmark.co.jp/coevo/scamper):  
アイデア改良のための7つの質問を用いて、ビジネスや研究開発における新しいアイデアを発散させ、創出する手法。   
 



