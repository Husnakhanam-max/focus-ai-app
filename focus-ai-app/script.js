const API = "http://127.0.0.1:5000";
let currentUser = "";

// AUTH
function signup() {
    fetch(API + "/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    }).then(r => r.json()).then(d => alert(d.message));
}

function login() {
    fetch(API + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    }).then(r => r.json()).then(d => {
        alert(d.message);
        currentUser = username.value;
        loadStats();
    });
}

// PLAN
function getPlan() {
    fetch(API + "/plan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ input: studyInput.value })
    }).then(r => r.json())
      .then(d => result.innerText = d.plan);
}

// TIMER + BREAK SYSTEM
function startTimer() {
    let time = 1500;

    const interval = setInterval(() => {
        let m = Math.floor(time / 60);
        let s = time % 60;

        timer.innerText = `${m}:${s < 10 ? '0' : ''}${s}`;
        time--;

        if (time < 0) {
            clearInterval(interval);

            result.innerText = "Great job! You completed a focus session 🎉";

            setTimeout(() => {
                result.innerText = "Breaks help your brain recharge.";
            }, 3000);

            setTimeout(() => {
                showActivity();
            }, 6000);

            trackSession();
        }
    }, 1000);
}

// ACTIVITIES
function showActivity() {
    const list = [
        "🎮 Click anywhere fast 5 times!",
        "🧘 Close eyes for 10 seconds",
        "🧠 What is 8 + 5?"
    ];

    const random = list[Math.floor(Math.random() * list.length)];
    result.innerText = random;

    setTimeout(() => {
        result.innerText = "Let’s get back to focus 💪";
    }, 10000);
}

// TRACKING
function trackSession() {
    fetch(API + "/track", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username: currentUser })
    });
}

function loadStats() {
    fetch(API + "/stats/" + currentUser)
        .then(r => r.json())
        .then(d => {
            stats.innerText = "Sessions completed: " + d.sessions;
        });
}