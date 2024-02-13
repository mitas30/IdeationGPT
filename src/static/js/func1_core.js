document.addEventListener('DOMContentLoaded', ()=> fetchData());

//awaitとasync,.thenはいずれも非同期処理 asyncの中でawaitは使用可能
async function fetchData() {
    try {
        // API呼び出し
        let response = await fetch('http://localhost:5000/func1/make_idea_api');
        let data = await response.json();
        console.log(data.message)
    } catch (error) {
        console.error('API呼び出し中にエラーが発生しました', error);
    }
}