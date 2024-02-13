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
    const response=await fetch('/auth_user/fetch_thread_api');
    const data=await response.json();
    const threads=data.threads;
    const threadList = document.getElementById('thread-list');
    threadList.innerHTML = '';

    //クリックできるボタンにすること
    threads.forEach(thread => {
        const div = document.createElement('div');
        div.innerHTML = `<p>${thread.problem}</p>`;
        threadList.appendChild(div);
    });
}
