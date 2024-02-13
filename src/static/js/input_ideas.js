let idea_count=0;

document.getElementById('ideaform').onsubmit = async function(event) {
  //ページのリロード及びgetメソッドを防ぐ
  //何個も送信する場合には，UXの問題から非同期処理を使用する
  event.preventDefault();
  idea_count++;
  let ideaName =document.getElementById('ideaname').value;
  let coreIdea =document.getElementById('core').value;
  let requiredTech=document.getElementById('reqtech').value;
  let effectiveness=document.getElementById('effectiveness').value;
  let useCase=document.getElementById('usecase').value;
  let post_idea=ideaName+"\nCore Idea "+coreIdea+"\nTechnologies and Materials Used: "+requiredTech+"\nRevised Approach to Problem-Solving: "+effectiveness+"\nConcrete Use Cases: "+useCase;

try {
  //responseはfetch(API)からの戻り値
  const response = await fetch('/input/receive_idea_api/', 
  { 
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json', 
    },
    body: JSON.stringify({ idea: post_idea }), 
  });
  //apiからの返答に対して応答する
  if (response.ok) {
    console.log('Idea submitted:', post_idea);
    //アイデア送信後、テキストエリアをclearする
    document.getElementById('ideaname').value = '';
    document.getElementById('core').value = '';
    document.getElementById('reqtech').value = '';
    document.getElementById('effectiveness').value = '';
    document.getElementById('usecase').value = '';
  } else {
    throw new Error('Something went wrong');
  }
}
//catch()は、try内の全てのエラーを補足できる 
//しかも、errorが起きた時点でtryの残りの処理は行われない
catch (error) {
  console.error('Error submitting idea:', error);
}
};

document.getElementById('finishBtn').onclick = function() {
  if(idea_count>0)
  {
    window.location.href='/input/redirect_select_criterias/';
  }
  else
  {
    alert("アイデアが1つも提出されていません")
  }
};
