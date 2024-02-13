document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const nickname = document.getElementById('signup-nickname').value;
    const password = document.getElementById('signup-password').value;

    signup(nickname,password);
});

async function signup(nickname,password){
    try{
    const response=await fetch('/auth_user/signup_api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nickname, password }),
    })
    if(response.status==400){
        alert('既に登録されたニックネームです。\n別のニックネームを選んでください。');
    }else{
        window.location.assign("/auth_user/login");
    }
    }catch(error){
        console.log('Error',error);
    }
}
