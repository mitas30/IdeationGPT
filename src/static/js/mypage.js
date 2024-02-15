document.addEventListener('DOMContentLoaded', () => {
    loadThreads();
    document.getElementById('create-thread').addEventListener('click', () => {
        createThread()
    });
});

async function createThread(){
    try{
    await fetch('/auth_user/create_thread_api');
    window.location.assign("/input/input_prob");
    }catch(error){
        console.log("Error",error);
    }
}

async function loadThreads() {
    const response = await fetch('/auth_user/fetch_thread_api');
    const data = await response.json();
    const threads = data.threads;
    const threadList = document.getElementById('thread-list');
    threadList.innerHTML = '';

    threads.forEach(thread => {
        const div = document.createElement('div');
        div.classList.add('clickable-thread'); // クリック可能なスタイルを適用
        div.innerHTML = `<p>${thread.jp_problem}</p>`;
        div.setAttribute('data-thread-id', thread.thread_id); // スレッドのIDをデータ属性として追加
        div.setAttribute('progress', thread.progress);
        
        // クリックイベントリスナーを追加
        div.addEventListener('click', function() {
            const thread_id = this.getAttribute('data-thread-id');
            const progress=this.getAttribute('progress');
            //progressはstrになった
            switch(progress){
                case '0':
                    window.location.href =`/input/input_prob?thread_id=${thread_id}`;
                    break;
                case '1':
                    window.location.href = `/input/save_and_redirect?thread_id=${thread_id}`;
                    break;
                case '2':
                    window.location.href = `/input/display_wait?thread_id=${thread_id}`;
                    break;
            }
        });
        threadList.appendChild(div);
    });
}

