document.addEventListener("DOMContentLoaded", function() {
    const hourDropdown = document.getElementById("hour");
    const minuteDropdown = document.getElementById("minute");
    const periodDropdown = document.getElementById("period");
    const translateBtn = document.getElementById("translate-btn");
    const output = document.getElementById("output");
    const historyList = document.getElementById("history-list");
    const clearHistoryBtn = document.getElementById("clear-history-btn"); // ✅ Clear history button
    const realTimeClock = document.getElementById("real-time-clock");
    const digitalClock = document.getElementById("digital-clock");
    const darkModeToggle = document.getElementById("dark-mode-toggle");

    // ✅ Create and Add TTS Button Below Output
    const speakBtn = document.createElement("button");
    speakBtn.innerText = "🔊 Play Yoruba Time";
    speakBtn.style.display = "none"; 
    output.after(speakBtn);

    // Populate Hour and Minute Dropdowns
    for (let i = 1; i <= 12; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        hourDropdown.appendChild(option);
    }

    for (let i = 0; i < 60; i++) {
        let option = document.createElement("option");
        option.value = i.toString().padStart(2, "0");
        option.textContent = i.toString().padStart(2, "0");
        minuteDropdown.appendChild(option);
    }

    // ✅ Dark Mode Toggle
    darkModeToggle.addEventListener("change", function() {
        document.body.classList.toggle("dark-mode");
    });

    // ✅ Translate Time and Enable TTS
    translateBtn.addEventListener("click", function() {
        let timeInput = `${hourDropdown.value}:${minuteDropdown.value} ${periodDropdown.value}`;

        fetch("https://your-username.pythonanywhere.com/translate", { //http://127.0.0.1:5000/translate
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ time: timeInput })
        })
        .then(response => response.json())
        .then(data => {
            output.innerText = `English: ${data.english} ➝ Yoruba: ${data.yoruba}`;
            
            let listItem = document.createElement("li");
            listItem.textContent = output.innerText;
            historyList.prepend(listItem);
            
            // ✅ Show Speak Button Only If Translation Works
            speakBtn.style.display = "block";

            // ✅ Play Yoruba Time
            speakBtn.onclick = function() {
                fetch("http://127.0.0.1:5000/speak", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: data.yoruba })
                })
                .then(response => {
                    if (!response.ok) throw new Error("TTS Failed");
                    return response.blob();
                })
                .then(blob => {
                    const audio = new Audio(URL.createObjectURL(blob));
                    audio.play();
                })
                .catch(() => alert("⚠️ Unable to generate audio. Check internet connection."));
            };
        });
    });

    // ✅ Clear Translation History
    clearHistoryBtn.addEventListener("click", function() {
        historyList.innerHTML = ""; // Clears the history
    });

    // ✅ Update Digital Clock & Yoruba Time
    function updateClocks() {
        let now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes().toString().padStart(2, "0");
        let seconds = now.getSeconds().toString().padStart(2, "0");
        let period = hours >= 12 ? "PM" : "AM";
        hours = hours % 12 || 12;

        digitalClock.innerText = `${hours}:${minutes}:${seconds} ${period}`;

        fetch("http://127.0.0.1:5000/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ time: `${hours}:${minutes} ${period}` })
        })
        .then(response => response.json())
        .then(data => {
            realTimeClock.innerText = data.yoruba; // ✅ Yoruba translation of current time
        });
    }

    setInterval(updateClocks, 1000);
});
