function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

window.onload = async function() 
{
let count=0;
let num_idea=0;
let result
// HTML要素を選択
const MAXCOUNT=3
const resultContainer = document.getElementById('resultContainer');
const countContainer = document.getElementById('countContainer');
while(count<MAXCOUNT){
    countContainer.textContent="現在のアイデア改良は"+(count+1)+"周目"
    //アイデアを向上させる
    try{
    let response=await fetch('/api/improve_idea/')
    if(!response.ok){
        throw new Error('API request失敗 ='+response.status)
    }
    resultContainer.textContent="アイデア改良が終了しました。5秒待ちます"
    await delay(5000);
    let data1=await response.json();
    if(data1.error!=0){
        throw new Error('error code :'+data1.error)
    }
    else{
        num_idea=data1.num_idea;
    }
    }catch(error){
        console.error('check api/improve_idea');
        window.location.href='/reuse/error/';
    }
    //step2:次にこれを評価する
    resultContainer.textContent="アイデアを評価しています。"
    try{
        let evaluate_response=await fetch('/api/evaluation_data/')
    if(!evaluate_response.ok){
        throw new Error('API request失敗 ='+response.status)
    }
    resultContainer.textContent="アイデア評価が終了しました。5秒待ちます"
    await delay(5000);
    let data2=await evaluate_response.json();
    if(data2.check!=0){
        throw new Error('error code :'+data2.check)
    }
    }catch(error){
        console.error('check api/evaluation_data');
        window.location.href='/reuse/error/';
    }
    //step3:評価したらこれを点数化する
    resultContainer.textContent="評価の点数を集計しています"
    try{
        let scored_response=await fetch('/api/sortout_scores/?num_idea='+num_idea);
    if(!scored_response.ok){
        throw new Error('API request失敗 ='+scored_response.status)
    }
    let data3=await scored_response.json();
    if(data3.check<0){
        throw new Error('error code :'+data3.check)
    }
    else if(data3.check==1){
        result=data3.result;
        break;
    }
    resultContainer.textContent="点数の集計が終わりました。5秒待ちます"
    await delay(5000);
    }catch(error){
        console.error('check api/evaluation_data');
        window.location.href='/reuse/error/';
    }
    count++;
}
//docs:goodなアイデアが3つ以下だった場合
if(count>=MAXCOUNT)
{
    try{
    let great_idea_result=await fetch('/api/get_great_ideas/');
    let json_data3_5=await great_idea_result.json();
    result=json_data3_5.result; 
    }catch(error){
        window.location.href='/reuse/error/';
    }
}
//step4:最後に日本語化する
try{
    const japanese_response=await fetch('/func3/translate_result/',{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body: JSON.stringify({result:result})
    });
    if(!japanese_response.ok){
        throw new Error('API request失敗 ='+japanese_response.status)
    }
    const data4=await japanese_response.json();
    console.log(data4.result);
    resultContainer.textContent = data4.result;
}catch(error){
    console.error('check api/res');
    window.location.href='/reuse/error/';
}
};