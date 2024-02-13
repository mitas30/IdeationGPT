document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var nickname = document.getElementById('login-nickname').value;
    var password = document.getElementById('login-password').value;
    
    if (nickname && password) {
        login(nickname,password)
        console.log('Login attempt with:', nickname, password);
    } else {
        document.getElementById('login-message').innerText = 'ニックネームとパスワードを入力してください。';
        document.getElementById('login-message').classList.add('error');
    }
});

async function login(nickname,password){
    try{
        //fetchの中身はPromiseだが、awaitを使うことで直接アクセスできるようになる
        const response=await fetch('/auth_user/login_api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nickname, password }),
        })
        //response.json()自体が非同期処理(awaitをつける→関数が非同期になる　ではなく、関数が非同期→awaitをつけてください)ということ。
        //const data=await response.json();
        if(response.status==401){
            alert('ニックネームまたはパスワードが違うようです。');
        }
        else{
            window.location.assign("/auth_user/mypage");
        }
    }catch(error){
        console.log('Error',error);
    }
}
