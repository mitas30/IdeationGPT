document.addEventListener('DOMContentLoaded', () => {
    // アイデアカードのクリックイベントを設定
    document.querySelectorAll('.idea-card').forEach(card => {
        card.addEventListener('click', () => {
            const id = card.getAttribute('id');
            showDetails(id);
        });
    });

    // ポップアップの閉じるボタンのクリックイベントを設定
    document.querySelectorAll('.popup .close').forEach(button => {
        button.addEventListener('click', () => {
            const popupId = button.closest('.popup').getAttribute('id');
            closePopup(popupId.replace('popup-', ''));
        });
    });

    const accordions = document.querySelectorAll('.accordion');

    accordions.forEach(accordion => {
        accordion.addEventListener('click', function() {
            this.classList.toggle('active');
            const panel = this.nextElementSibling;

            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    });

    const button=document.getElementById('backToMyPage');
    button.addEventListener('click',function(){
        window.location.assign('/func1/back_to_mypage');
    })
});

function showDetails(id) {
    document.getElementById('popup-' + id).style.display = 'flex';
}

function closePopup(id) {
    document.getElementById('popup-' + id).style.display = 'none';
}
