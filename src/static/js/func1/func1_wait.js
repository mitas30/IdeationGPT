//HTMLが読み込まれてから実行される
document.addEventListener('DOMContentLoaded',async()=>{
    //awaitは、非同期関数のPromiseが帰るまで一時停止する機構
    await initProgress();
    //ここの2つは並行に実行される
    fetchData();
    setInterval(getProgress,5000);
});

const button=document.getElementById('backToMyPage');

button.addEventListener('click',function(){
    window.location.assign('/func1/back_to_mypage');
})

//awaitを使用しない場合、並列で物事が進んでいく
async function initProgress(){
    try {
        const response = await fetch('/func1/init_progress/');
        if(response.status==200){
            console.log('redisの初期化完了')
        }
    } catch (error) {
        console.error('redisの初期化ができなかった', error);
    }
}

async function fetchData() {
    try {
        const response = await fetch('/func1/make_idea_api/');
        if(response.status==200){
            window.location.assign('/func1/display_result');
        }
    } catch (error) {
        console.error('API呼び出し中にエラーが発生しました', error);
    }
}

async function getProgress(){
    try{
        const response=await fetch('/func1/get_progress');
        const data=await response.json();
        console.log(data);
        switch(data[0]){
            //まだ何も終わっていない
            case '0':
                break;
            //アイデア作成の完了
            case '1':
                const compa=document.getElementById('step1');
                compa.classList.add('completed');
                break;
            //アイデア評価1回目
            case '2':
                const compb=document.getElementById('step2');
                compb.classList.add('completed');
                break;
            //アイデア向上の完了
            case '3':
                const compc=document.getElementById('step3');
                compc.classList.add('completed');
                break;
            //アイデア評価2回目
            case '4':
                const compd=document.getElementById('step4');
                compd.classList.add('completed');
                break;
            default:
                console.log(data[0]);
        }
        const event_data=document.getElementById('latest-event');
        event_data.textContent=data[1];
    }catch(error){

    }
}

