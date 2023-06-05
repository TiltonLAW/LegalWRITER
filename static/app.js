const queryField = document.getElementById("query-field");
const inputField = document.getElementById("input-field");
const submitButton = document.getElementById("submit-button");
const outputDiv = document.getElementById("output-container");

// Event listener for Enter key press
inputField.addEventListener("keyup", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    submitButton.click();
  }
});

// Event listener for click on submit button
submitButton.addEventListener("click", function () {
  const query = queryField.value;
  const prompt = inputField.value;

  // Check if either input field is empty
  if (prompt === "") {
    alert("Legal question is required.");
    return;
  }

  queryField.disabled = true;
  inputField.disabled = true;
  inputField.value = "";
  queryField.value = "";

  outputDiv.innerHTML += `<div class="output-question">Q: ${prompt} (based on query: ${query})</div>`;
  outputDiv.innerHTML += `<div class="output-answer typing-indicator">scholar:</div>`;

  // Start typing animation
  animateTypingIndicator();

  fetch("/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query, prompt: prompt }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Stop typing animation
      clearInterval(typingIndicatorInterval);
      // Remove typing indicator
      let typingIndicatorDiv = document.querySelector(".typing-indicator");
      typingIndicatorDiv.parentElement.removeChild(typingIndicatorDiv);

      const answer = data.answer; // Extract the answer string
      outputDiv.innerHTML += `<div class="output-answer"><br><br>${answer}</div>`;

      generateCaseSummaries(data.summarize_buttons); // Generate case summaries with buttons

      outputDiv.scrollTop = outputDiv.scrollHeight;
      queryField.disabled = false;
      inputField.disabled = false;
      inputField.focus();
    })
    .catch((error) => {
      console.error(error);
      // If there is an error, we should re-enable the inputs and stop the typing animation
      clearInterval(typingIndicatorInterval);
      let typingIndicatorDiv = document.querySelector(".typing-indicator");
      typingIndicatorDiv.parentElement.removeChild(typingIndicatorDiv);
      queryField.disabled = false;
      inputField.disabled = false;
    });
});

// Function to generate case summaries with buttons
function generateCaseSummaries(summarizeButtons) {
  for (const button of summarizeButtons) {
    const caseUrl = button.url;  // Use the JSON case URL
    const fullCaseUrl = `${caseUrl}?full_case=true`;  // Append ?full_case=true

    const summarizeButton = document.createElement("button");
    summarizeButton.className = "summarize-button";
    summarizeButton.dataset.caseUrl = fullCaseUrl;
    summarizeButton.innerText = `Summarize ${button.name_abbreviation}`;
    summarizeButton.addEventListener("click", () => {
      summarizeCase(fullCaseUrl);
    });
    outputDiv.appendChild(summarizeButton);
    outputDiv.appendChild(document.createElement("br"));
  }
}

// Function to summarize a case
function summarizeCase(caseUrl) {
  fetch("/summarize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: caseUrl }),
  })
    .then((response) => response.json())
    .then((data) => {
      const summary = data.summary;
      // Display the case summary in the output container
      const summaryDiv = document.createElement("div");
      summaryDiv.className = "case-summary";
      summaryDiv.innerHTML = summary;
      outputDiv.appendChild(summaryDiv);
    })
    .catch((error) => {
      console.error(error);
    });
}

// For the typing indicator
let typingIndicatorInterval;

function animateTypingIndicator() {
  let dots = "";
  typingIndicatorInterval = setInterval(() => {
    if (dots.length === 3) dots = "";
    dots += ".";
    let typingIndicatorDiv = document.querySelector(".typing-indicator");
    if (typingIndicatorDiv) {
      typingIndicatorDiv.innerHTML = `<br>Researching ${dots}`;
    }
  }, 1800);
}
