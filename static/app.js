const inputField = document.getElementById("input-field");
const submitButton = document.getElementById("submit-button");
const outputDiv = document.getElementById("output-container");

inputField.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        submitButton.click();
    }
});

submitButton.addEventListener("click", function() {
    const prompt = inputField.value;
    if (prompt === "") {
        return;
    }
    inputField.disabled = true;
    inputField.value = "";
    outputDiv.innerHTML += `<div class="output-question">${prompt}</div>`;
    outputDiv.innerHTML += `<div class="output-answer typing-indicator">scholar:</div>`;
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({prompt: prompt})
    })
    .then(response => response.json())
    .then(data => {
        outputDiv.lastElementChild.classList.remove("typing-indicator");
        outputDiv.innerHTML += `<div class="output-answer">${data}</div>`;
        outputDiv.scrollTop = outputDiv.scrollHeight;
        inputField.disabled = false;
        inputField.focus();
    })
    .catch(error => console.error(error));
});

const typingIndicator = '<div class="output-answer typing-indicator">.</div>';

function animateTypingIndicator() {
    let dots = '';
    setInterval(() => {
        if (dots.length === 3) dots = '';
        dots += '.';
        document.querySelector('.typing-indicator').innerHTML = dots;
    }, 700);
}

submitButton.addEventListener("click", function() {
    const prompt = inputField.value;
    if (prompt === "") {
        return;
    }
    inputField.disabled = true;
    inputField.value = "";
    outputDiv.innerHTML += `<div class="output-question">A: ${prompt}</div>`;
    outputDiv.innerHTML += typingIndicator;
    animateTypingIndicator();
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({prompt: prompt})
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(animateTypingIndicator);
        outputDiv.lastElementChild.classList.remove("typing-indicator");
        outputDiv.innerHTML += `<div class="output-answer">${data}</div>`;
        outputDiv.scrollTop = outputDiv.scrollHeight;
        inputField.disabled = false;
        inputField.focus();
    })
    .catch(error => console.error(error));
});
