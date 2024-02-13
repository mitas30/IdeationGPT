window.onload = async function() 
{
    try{
        const response=await fetch('/func3/evaluate_idea_api/');
    if(response.ok){
        window.location.href='/func3/display_evaluate_result/';
    }
    else{
        throw new Error('HTTP error!')
    }
    }catch(error){
        console.error('There was a problem with the fetch operation:', error);
    }
};