const slider = document.getElementById('love-slider');
const scoreDisplay = document.getElementById('score-display');
const emojiHeart = document.getElementById('emoji-heart');
const sendBtn = document.getElementById('send-btn');
const statusMsg = document.getElementById('status-message');
const messageArea = document.getElementById('daily-message');

// עדכון התצוגה כשהסליידר זז
slider.oninput = function() {
    const value = this.value;
    scoreDisplay.innerText = value;
    
    // הגדלת הלב לפי הציון
    const scale = 0.5 + (value / 10);
    emojiHeart.style.transform = `scale(${scale})`;
    
    // שינוי אימוג'י לפי הציון
    if (value <= 3) emojiHeart.innerText = '😌';
    else if (value <= 7) emojiHeart.innerText = '❤️';
    else emojiHeart.innerText = '💖';
};

// שליחת הנתונים
sendBtn.onclick = function() {
    const data = {
        score: slider.value,
        message: messageArea.value
    };

    console.log('Sending love data:', data);

    sendBtn.disabled = true;
    sendBtn.innerText = 'שולח...';

    fetch('/submit-love', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
        sendBtn.classList.add('hidden');
        statusMsg.classList.remove('hidden');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('אופס, הייתה תקלה בשליחת האהבה. נסי שוב?');
        sendBtn.disabled = false;
        sendBtn.innerText = 'שלחי אהבה 🚀';
    });
};
