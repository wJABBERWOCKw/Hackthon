window.onload = function () {
    // ... Existing code ...

    // Function to handle speech recognition
    function startSpeechRecognition() {
        const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.lang = 'en-US'; // Set the language for speech recognition (you can change it as needed)
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log("Speech Recognized: ", transcript);
            // Do something with the transcript, e.g., display it in a chat window or send it to the server.
        };

        recognition.onerror = (event) => {
            console.error("Speech Recognition Error:", event.error);
        };

        recognition.start();
    }

    // Add an event listener to the "Enable Captions" button
    const captionToggleButton = document.getElementById('caption-toggle-button');
    captionToggleButton.addEventListener('click', () => {
        const captionsEnabled = zp.isCaptionsOn();
        if (captionsEnabled) {
            zp.turnOffCaptions();
            captionToggleButton.textContent = 'Enable Captions';
        } else {
            zp.turnOnCaptions();
            captionToggleButton.textContent = 'Disable Captions';
        }
    });

    // Add an event listener to the "Enable Microphone" button
    const microphoneButton = document.getElementById('microphone-toggle-button');
    microphoneButton.addEventListener('click', () => {
        startSpeechRecognition();
    });
}