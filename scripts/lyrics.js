document.addEventListener('DOMContentLoaded', () => {

    const audio = document.getElementById('audio-player');
    const lyricsContainer = document.getElementById('lyrics-container');

    const lyricsData = [
        {
            line: "Hey, what you doing?",
            words: [
                { text: "Hey,", time: 13.413 },
                { text: "what", time: 15.937 },
                { text: "you", time: 16.358 },
                { text: "doing?", time: 16.638 }
            ]
        },
        {
            line: "Not a lot",
            words: [
                { text: "Not", time: 19.263 },
                { text: "a", time: 19.884 },
                { text: "lot", time: 20.004 }
            ]
        },
        {
            line: "Shaking and moving at my local spot",
            words: [
                { text: "Shaking", time: 22.028 },
                { text: "and", time: 23.109 },
                { text: "moving", time: 23.37 },
                { text: "at", time: 25.433 },
                { text: "my", time: 25.594 },
                { text: "local", time: 25.794 },
                { text: "spot", time: 26.455 }
            ]
        },
        {
            line: "Baby, don't ask me why, don't ask me why",
            words: [
                { text: "Baby,", time: 28.639 },
                { text: "don't", time: 29.12 },
                { text: "ask", time: 29.54 },
                { text: "me", time: 29.781 },
                { text: "why,", time: 30.061 },
                { text: "Don't", time: 32.305 },
                { text: "ask", time: 32.726 },
                { text: "me", time: 33.006 },
                { text: "why", time: 33.227 }
            ]
        },
        {
            line: "Lay, lady, lay",
            words: [
                { text: "Lay,", time: 39.637 },
                { text: "lady,", time: 42.201 },
                { text: "lay", time: 42.882 }
            ]
        },
        {
            line: "On this side of paradise",
            words: [
                { text: "On", time: 44.985 },
                { text: "this", time: 45.145 },
                { text: "side", time: 45.445 },
                { text: "of", time: 45.986 },
                { text: "paradise", time: 46.166 }
            ]
        },
        {
            line: "In the Tropic of Cancer",
            words: [
                { text: "In", time: 47.688 },
                { text: "the", time: 47.889 },
                { text: "Tropic", time: 48.009 },
                { text: "of", time: 49.391 },
                { text: "Cancer", time: 49.551 }
            ]
        },
        {
            line: "'Cause if I had my way, you would always stay",
            words: [
                { text: "'Cause", time: 52.275 },
                { text: "if", time: 52.595 },
                { text: "I", time: 52.856 },
                { text: "had", time: 53.016 },
                { text: "my", time: 53.296 },
                { text: "way,", time: 53.557 },
                { text: "You", time: 55.86 },
                { text: "would", time: 56.06 },
                { text: "always", time: 56.481 },
                { text: "stay", time: 56.781 }
            ]
        },
        {
            line: "And I'd be your tiny dancer, honey",
            words: [
                { text: "And", time: 58.183 },
                { text: "I'd", time: 59.565 },
                { text: "be", time: 61.207 },
                { text: "your", time: 61.648 },
                { text: "tiny", time: 61.968 },
                { text: "dancer,", time: 62.629 },
                { text: "Honey,", time: 63.991 }
            ]
        },
        {
            line: "I waited for you",
            words: [
                { text: "I", time: 64.672 },
                { text: "waited", time: 67.837 },
                { text: "for", time: 68.437 },
                { text: "you", time: 69.058 }
            ]
        },
        {
            line: "In the spot you said to wait",
            words: [
                { text: "In", time: 70.602 },
                { text: "the", time: 71.043 },
                { text: "spot", time: 71.323 },
                { text: "you", time: 71.664 },
                { text: "said", time: 71.784 },
                { text: "to", time: 72.244 },
                { text: "wait", time: 72.665 }
            ]
        },
        {
            line: "In the city, on a park bench",
            words: [
                { text: "In", time: 73.967 },
                { text: "the", time: 74.147 },
                { text: "city,", time: 74.428 },
                { text: "on", time: 74.848 },
                { text: "a", time: 74.928 },
                { text: "park", time: 75.089 },
                { text: "bench", time: 75.549 }
            ]
        },
        {
            line: "In the middle of the pouring rain",
            words: [
                { text: "In", time: 77.272 },
                { text: "the", time: 77.492 },
                { text: "middle", time: 77.953 },
                { text: "of", time: 78.093 },
                { text: "the", time: 78.173 },
                { text: "pouring", time: 78.353 },
                { text: "rain", time: 79.215 }
            ]
        },
        {
            line: "'Cause I adored you",
            words: [
                { text: "'Cause", time: 80.576 },
                { text: "I", time: 81.197 },
                { text: "adored", time: 81.918 },
                { text: "you", time: 82.92 }
            ]
        },
        {
            line: "I just wanted things to be the same",
            words: [
                { text: "I", time: 83.801 },
                { text: "just", time: 83.921 },
                { text: "wanted", time: 84.202 },
                { text: "things", time: 84.562 },
                { text: "to", time: 84.843 },
                { text: "be", time: 85.043 },
                { text: "the", time: 85.424 },
                { text: "same", time: 85.664 }
            ]
        },
        {
            line: "You said to meet me up there tomorrow",
            words: [
                { text: "You", time: 86.946 },
                { text: "said", time: 87.026 },
                { text: "to", time: 87.266 },
                { text: "meet", time: 87.487 },
                { text: "me", time: 87.727 },
                { text: "up", time: 88.047 },
                { text: "there", time: 88.228 },
                { text: "tomorrow", time: 88.848 }
            ]
        },
        {
            "line": "But tomorrow never came",
            "words": [
                { "text": "But", "time": 90.200 },
                { "text": "tomorrow", "time": 90.460 },
                { "text": "never", "time": 90.980 },
                { "text": "came", "time": 91.840 }
            ]
        },
        {
            "line": "Tomorrow never came",
            "words": [
                { "text": "Tomorrow", "time": 96.500 },
                { "text": "never", "time": 97.104 },
                { "text": "came", "time": 97.950 }
            ]
        },
        {
            line: "Hey, what you thinking? Penny for your thoughts",
            words: [
                { text: "Hey,", time: 103.036 },
                { text: "what", time: 107.941 },
                { text: "you", time: 108.261 },
                { text: "thinking?", time: 108.582 },
                { text: "Penny", time: 110.824 },
                { text: "for", time: 111.265 },
                { text: "your", time: 111.705 },
                { text: "thoughts", time: 112.045 }
            ]
        },
        {
            line: "Those lights are blinking on that old jukebox",
            words: [
                { text: "Those", time: 114.108 },
                { text: "lights", time: 114.528 },
                { text: "are", time: 115.029 },
                { text: "blinking", time: 115.149 },
                { text: "on", time: 117.511 },
                { text: "that", time: 117.631 },
                { text: "old", time: 117.992 },
                { text: "jukebox", time: 118.152 }
            ]
        },
        {
            line: "But don't ask me why, just swallow some wine",
            words: [
                { text: "But", time: 120.314 },
                { text: "don't", time: 121.035 },
                { text: "ask", time: 121.515 },
                { text: "me", time: 121.736 },
                { text: "why,", time: 121.936 },
                { text: "just", time: 123.918 },
                { text: "swallow", time: 124.278 },
                { text: "some", time: 124.939 },
                { text: "wine", time: 125.239 }
            ]
        },
        {
            line: "Wi-wi-wi-wi-wi-wi-wi-wine",
            words: [
                { text: "Wi-wi-wi-wi-wi-wi-wi-wine", time: 126.821 }
            ]
        },
        {
            line: "Stay, baby, stay on this side of paradise",
            words: [
                { text: "Stay,", time: 134.221 },
                { text: "baby,", time: 134.822 },
                { text: "stay", time: 134.842 },
                { text: "on", time: 137.265 },
                { text: "this", time: 137.385 },
                { text: "side", time: 137.565 },
                { text: "of", time: 138.106 },
                { text: "paradise", time: 138.226 }
            ]
        },
        {
            line: "In the Tropic of Cancer",
            words: [
                { text: "In", time: 139.688 },
                { text: "the", time: 139.808 },
                { text: "Tropic", time: 139.968 },
                { text: "of", time: 141.25 },
                { text: "Cancer", time: 141.41 }
            ]
        },
        {
            line: "'Cause if I had my way, you would always stay",
            words: [
                { text: "'Cause", time: 144.394 },
                { text: "if", time: 144.594 },
                { text: "I", time: 144.834 },
                { text: "had", time: 145.035 },
                { text: "my", time: 145.295 },
                { text: "way,", time: 145.515 },
                { text: "you", time: 147.838 },
                { text: "would", time: 148.018 },
                { text: "always", time: 148.399 },
                { text: "stay.", time: 148.739 }
            ]
        },
        {
            line: "And you'd be my tiny dancer, baby",
            words: [
                { text: "And", time: 151.202 },
                { text: "you'd", time: 151.383 },
                { text: "be", time: 153.185 },
                { text: "my", time: 153.606 },
                { text: "tiny", time: 153.946 },
                { text: "dancer,", time: 154.547 },
                { text: "baby", time: 155.989 }
            ]
        },
        {
            line: "I waited for you",
            words: [
                { text: "I", time: 159.233 },
                { text: "waited", time: 159.954 },
                { text: "for", time: 160.514 },
                { text: "you.", time: 161.115 }
            ]
        },
        {
            line: "In the spot you said to wait",
            words: [
                { text: "In", time: 162.571 },
                { text: "the", time: 162.831 },
                { text: "spot", time: 162.991 },
                { text: "you", time: 163.472 },
                { text: "said", time: 163.792 },
                { text: "to", time: 164.273 },
                { text: "wait", time: 164.673 }
            ]
        },
        {
            line: "In the city, on a park bench",
            words: [
                { text: "In", time: 165.995 },
                { text: "the", time: 166.135 },
                { text: "city,", time: 166.315 },
                { text: "on", time: 166.876 },
                { text: "a", time: 166.956 },
                { text: "park", time: 167.136 },
                { text: "bench", time: 168.237 }
            ]
        },
        {
            line: "In the middle of the pouring rain",
            words: [
                { text: "In", time: 169.278 },
                { text: "the", time: 169.418 },
                { text: "middle", time: 169.599 },
                { text: "of", time: 170.139 },
                { text: "the", time: 170.239 },
                { text: "pouring", time: 170.399 },
                { text: "rain", time: 171.22 }
            ]
        },
        {
            line: "'Cause I adored you",
            words: [
                { text: "'Cause", time: 172.462 },
                { text: "I", time: 173.202 },
                { text: "adored", time: 173.603 },
                { text: "you", time: 174.604 }
            ]
        },
        {
            line: "I just wanted things to be the same",
            words: [
                { text: "And", time: 175.625 },
                { text: "I", time: 175.885 },
                { text: "just", time: 176.025 },
                { text: "wanted", time: 176.266 },
                { text: "things", time: 176.646 },
                { text: "to", time: 176.886 },
                { text: "be", time: 177.026 },
                { text: "the", time: 177.407 },
                { text: "same", time: 177.687 }
            ]
        },
        {
            line: "You said you'd meet me out there tomorrow",
            words: [
                { text: "You", time: 178.969 },
                { text: "said", time: 179.049 },
                { text: "you'd", time: 179.409 },
                { text: "meet", time: 179.549 },
                { text: "me", time: 179.769 },
                { text: "out", time: 180.11 },
                { text: "there", time: 180.25 },
                { text: "tomorrow", time: 180.73 }
            ]
        },
        {
            line: "But tomorrow never came",
            words: [
                { text: "But", time: 182.352 },
                { text: "tomorrow", time: 182.572 },
                { text: "never", time: 183.593 },
                { text: "came", time: 184.234 }
            ]
        },
        {
            line: "Tomorrow never came",
            words: [
                { text: "Tomorrow", time: 189.139 },
                { text: "never", time: 190.181 },
                { text: "came", time: 190.781 }
            ]
        },
        {
            line: "Roses out in your country house",
            words: [
                { text: "Roses", time: 199.173 },
                { text: "out", time: 200.134 },
                { text: "in", time: 200.374 },
                { text: "your", time: 200.494 },
                { text: "country", time: 200.835 },
                { text: "house", time: 202.877 }
            ]
        },
        {
            line: "We played guitar in your bong",
            words: [
                { text: "We", time: 205.62 },
                { text: "played", time: 205.76 },
                { text: "guitar", time: 206.42 },
                { text: "in", time: 207.021 },
                { text: "your", time: 207.181 },
                { text: "bong", time: 209.243 }
            ]
        },
        {
            line: "And everyday felt like Sunday",
            words: [
                { text: "And", time: 212.507 },
                { text: "everyday", time: 212.587 },
                { text: "felt", time: 213.367 },
                { text: "like", time: 213.588 },
                { text: "Sunday", time: 213.968 }
            ]
        },
        {
            line: "And I, I wish we had stayed home",
            words: [
                { text: "And", time: 216.371 },
                { text: "I,", time: 217.432 },
                { text: "I", time: 219.193 },
                { text: "wish", time: 219.354 },
                { text: "we", time: 219.654 },
                { text: "had", time: 220.034 },
                { text: "stayed", time: 220.214 },
                { text: "home", time: 221.716 }
            ]
        },
        {
            line: "And I could put on the radio to our favorite song",
            words: [
                { text: "And", time: 223.238 },
                { text: "I", time: 223.318 },
                { text: "could", time: 225.76 },
                { text: "put", time: 225.78 },
                { text: "on", time: 225.96 },
                { text: "the", time: 226.221 },
                { text: "radio", time: 226.661 },
                { text: "to", time: 229.177 },
                { text: "our", time: 229.538 },
                { text: "favorite", time: 229.638 },
                { text: "song", time: 230.399 }
            ]
        },
        {
            line: "Lennon and Yoko, we would play all day long",
            words: [
                { text: "Lennon", time: 232.062 },
                { text: "and", time: 232.663 },
                { text: "Yoko,", time: 232.763 },
                { text: "we", time: 233.585 },
                { text: "would", time: 235.708 },
                { text: "play", time: 235.949 },
                { text: "all", time: 236.149 },
                { text: "day", time: 236.77 },
                { text: "long", time: 237.091 }
            ]
        },
        {
            line: "Isn't life crazy? I said now that I'm singing with Sean",
            words: [
                { text: "Isn't", time: 238.773 },
                { text: "life", time: 239.194 },
                { text: "crazy?", time: 239.575 },
                { text: "I", time: 240.817 },
                { text: "said", time: 241.097 },
                { text: "now", time: 242.179 },
                { text: "that", time: 242.36 },
                { text: "I'm", time: 242.66 },
                { text: "singing", time: 242.8 },
                { text: "with", time: 243.261 },
                { text: "Sean", time: 243.622 }
            ]
        },
        {
            line: "Whoa",
            words: [
                { text: "Whoa", time: 251.235 }
            ]
        },
        {
            line: "I could keep waiting for you",
            words: [
                { text: "I", time: 251.255 },
                { text: "could", time: 251.375 },
                { text: "keep", time: 251.595 },
                { text: "waiting", time: 251.856 },
                { text: "for", time: 252.477 },
                { text: "you", time: 253.118 }
            ]
        },
        {
            line: "In the spot we always wait",
            words: [
                { text: "In", time: 254.641 },
                { text: "the", time: 254.921 },
                { text: "spot", time: 255.322 },
                { text: "we", time: 255.582 },
                { text: "always", time: 256.143 },
                { text: "wait", time: 256.884 }
            ]
        },
        {
            line: "In the city, on the park bench",
            words: [
                { text: "In", time: 258.145 },
                { text: "the", time: 258.265 },
                { text: "city,", time: 258.445 },
                { text: "on", time: 258.986 },
                { text: "the", time: 259.106 },
                { text: "park", time: 259.226 },
                { text: "bench", time: 259.667 }
            ]
        },
        {
            line: "In the summer, on the pouring rain",
            words: [
                { text: "In", time: 260.548 },
                { text: "the", time: 261.489 },
                { text: "summer,", time: 261.649 },
                { text: "on", time: 262.23 },
                { text: "the", time: 262.33 },
                { text: "pouring", time: 262.49 },
                { text: "rain", time: 263.591 }
            ]
        },
        {
            line: "Honey, don't ignore me",
            words: [
                { text: "Honey,", time: 264.653 },
                { text: "don't", time: 264.973 },
                { text: "ignore", time: 265.614 },
                { text: "me", time: 266.154 }
            ]
        },
        {
            line: "I just wanted it to be the same",
            words: [
                { text: "I", time: 267.916 },
                { text: "just", time: 268.037 },
                { text: "wanted", time: 268.277 },
                { text: "it", time: 268.737 },
                { text: "to", time: 268.858 },
                { text: "be", time: 269.058 },
                { text: "the", time: 269.458 },
                { text: "same", time: 269.739 }
            ]
        },
        {
            "line": "You said you'd love me like no tomorrow",
            "words": [
                { "text": "You", "time": 271.0 },
                { "text": "said", "time": 271.08 },
                { "text": "you", "time": 271.441 },
                { "text": "loved", "time": 271.661 },
                { "text": "me", "time": 271.821 },
                { "text": "like", "time": 272.141 },
                { "text": "no", "time": 272.662 },
                { "text": "tomorrow", "time": 272.802 }
            ]
        },
        {
            "line": "I guess tomorrow never came, no, no, no",
            "words": [
                { "text": "I", "time": 274.524 },
                { "text": "guess", "time": 274.584 },
                { "text": "tomorrow", "time": 274.724 },
                { "text": "never", "time": 275.766 },
                { "text": "came,", "time": 276.326 },
                { "text": "no,", "time": 278.941 },
                { "text": "no,", "time": 279.241 },
                { "text": "no", "time": 279.521 }
            ]
        },
        {
            "line": "Tomorrow never came, no, no",
            "words": [
                { "text": "Tomorrow", "time": 281.432 },
                { "text": "never", "time": 282.373 },
                { "text": "came,", "time": 282.914 },
                { "text": "no,", "time": 285.961 },
                { "text": "no", "time": 286.076 }
            ]
        },
        {
            "line": "Tomorrow never came, no, no, no",
            "words": [
                { "text": "Tomorrow", "time": 288.000 },
                { "text": "never", "time": 288.941 },
                { "text": "came,", "time": 289.482 },
                { "text": "no,", "time": 292.000 },
                { "text": "no,", "time": 292.200 },
                { "text": "no", "time": 292.400 }
            ]
        },
        {
            "line": "Tomorrow never came",
            "words": [
                { "text": "Tomorrow", "time": 295.571 },
                { "text": "never", "time": 296.374 },
                { "text": "came.", "time": 296.394 }
            ]
        }
    ];

    function setupLyrics() {
        lyricsData.forEach((lineData, lineIndex) => {
            const lineElement = document.createElement('p');
            lineElement.classList.add('lyric-line');
            lineElement.dataset.lineIndex = lineIndex;

            lineData.words.forEach((wordData, wordIndex) => {
                const wordElement = document.createElement('span');
                wordElement.classList.add('lyric-word');
                wordElement.textContent = wordData.text + ' ';
                wordElement.dataset.wordIndex = wordIndex;
                lineElement.appendChild(wordElement);
            });

            lyricsContainer.appendChild(lineElement);
        });
    }

    let currentLine = -1;
    let currentWord = -1;

    function updateLyrics() {
        const currentTime = audio.currentTime;

        let activeLineIndex = lyricsData.findIndex((lineData, index) => {
            if (!lineData.words || lineData.words.length === 0) {
                return false;
            }
            const startTime = lineData.words[0].time;

            let nextLineStartTime = audio.duration;
            for (let i = index + 1; i < lyricsData.length; i++) {
                if (lyricsData[i].words.length > 0) {
                    nextLineStartTime = lyricsData[i].words[0].time;
                    break;
                }
            }

            return currentTime >= startTime && currentTime < nextLineStartTime;
        });

        if (activeLineIndex === -1 && lyricsContainer.children.length > 0) {
            if(currentLine !== -1 && lyricsContainer.children[currentLine]) {
                lyricsContainer.children[currentLine].classList.remove('active-line');
                Array.from(lyricsContainer.children[currentLine].children).forEach(wordEl => wordEl.classList.remove('active'));
            }
            currentLine = -1;
            return;
        }

        if (activeLineIndex !== -1 && activeLineIndex !== currentLine) {
            if (currentLine !== -1 && lyricsContainer.children[currentLine]) {
                lyricsContainer.children[currentLine].classList.remove('active-line');
                Array.from(lyricsContainer.children[currentLine].children).forEach(wordEl => wordEl.classList.remove('active'));
            }

            lyricsContainer.children[activeLineIndex].classList.add('active-line');
            const activeLineElement = lyricsContainer.children[activeLineIndex];
            lyricsContainer.scrollTop = activeLineElement.offsetTop - lyricsContainer.clientHeight / 2 + activeLineElement.clientHeight / 2;

            currentLine = activeLineIndex;
            currentWord = -1;
        }

        if (currentLine !== -1) {
            const lineData = lyricsData[currentLine];
            const lineElement = lyricsContainer.children[currentLine];

            if (!lineData.words || lineData.words.length === 0) return;

            let activeWordIndex = lineData.words.findIndex((wordData, index) => {
                const nextWordData = lineData.words[index + 1];
                const nextLineData = lyricsData[currentLine + 1];
                let nextWordTime = nextLineData && nextLineData.words.length > 0 ? nextLineData.words[0].time : audio.duration;
                if(nextWordData) {
                    nextWordTime = nextWordData.time;
                }

                return currentTime >= wordData.time && currentTime < nextWordTime;
            });

            if (activeWordIndex !== -1 && activeWordIndex !== currentWord) {
                for (let i = 0; i < lineElement.children.length; i++) {
                    if (i <= activeWordIndex) {
                        lineElement.children[i].classList.add('active');
                    } else {
                        lineElement.children[i].classList.remove('active');
                    }
                }
                currentWord = activeWordIndex;
            }
        }
    }

    setupLyrics();
    audio.addEventListener('timeupdate', updateLyrics);

});