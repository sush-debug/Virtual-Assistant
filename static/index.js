let isSignUp = false;
let USERS_KEY = "friday_users";
let fakeUser = {email: 'test@orb.com', password: 'Test1234!', name: 'Sushant Devidas Sarawade'};
function loadUsers() {
  let users = localStorage.getItem(USERS_KEY);
  return users ? JSON.parse(users) : [fakeUser];
}
function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}
function findUser(email) {
  return loadUsers().find(u => u.email === email);
}
function validateEmail(email) {
  return /^[\w-.]+@[\w-]+\.[a-z]{2,}$/i.test(email);
}
function validatePassword(pw) {
  return /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+\-=]{6,}$/.test(pw);
}
function validateName(name) {
  return name && name.trim().length >= 2;
}
function resetAuthForm() {
  document.getElementById('authEmail').value = '';
  document.getElementById('authPassword').value = '';
  document.getElementById('fullNameError').textContent = '';
  document.getElementById('emailError').textContent = '';
  document.getElementById('passwordError').textContent = '';
  document.getElementById('authError').textContent = '';
  document.getElementById('authFullName').value = '';
}
function showAuthError(msg) {
  document.getElementById('authError').textContent = msg;
}
document.getElementById('authForm').addEventListener('submit', function(e) {
  e.preventDefault();
  let email = document.getElementById('authEmail').value.trim();
  let pw = document.getElementById('authPassword').value;
  let name = document.getElementById('authFullName').value.trim();
  let valid = true;
  document.getElementById('emailError').textContent = '';
  document.getElementById('passwordError').textContent = '';
  document.getElementById('fullNameError').textContent = '';
  document.getElementById('authError').textContent = '';
  if (isSignUp && !validateName(name)) {
    document.getElementById('fullNameError').textContent = 'Please enter a valid name';
    valid = false;
  }
  if (!validateEmail(email)) {
    document.getElementById('emailError').textContent = 'Invalid email format';
    valid = false;
  }
  if (!validatePassword(pw)) {
    document.getElementById('passwordError').textContent = 'Password must be at least 6 chars and include a letter & number';
    valid = false;
  }
  if (!valid) return;

  let users = loadUsers();
  if (!isSignUp) { // Sign In
    let u = users.find(u => u.email === email && u.password === pw);
    if (!u) {
      showAuthError('Incorrect email or password');
    } else {
      localStorage.setItem("friday_logged_in", email);
      localStorage.setItem("friday_user_name", u.name || "User");
      showInitScreen();
    }
  } else { // Sign Up
    if (findUser(email)) {
      showAuthError('User already exists. Please sign in.');
      return;
    }
    users.push({email, password: pw, name});
    saveUsers(users);
    localStorage.setItem("friday_logged_in", email);
    localStorage.setItem("friday_user_name", name);
    showInitScreen();
  }
});
document.getElementById('googleBtn').onclick = function() {
  showAuthError('Google Sign-In is a demo. Use test@orb.com / Test1234! for demo login.');
};
document.getElementById('githubBtn').onclick = function() {
  showAuthError('GitHub Sign-In is a demo. Use test@orb.com / Test1234! for demo login.');
};
document.getElementById('switchAuthLink').onclick = function() {
  isSignUp = !isSignUp;
  if (isSignUp) {
    document.getElementById('fullNameGroup').style.display = '';
    document.getElementById('authSubtitle').textContent = "Create your account to get started.";
    document.getElementById('mainAuthBtn').textContent = "Create Account";
    document.getElementById('switchAuth').innerHTML = 'Already have an account? <span id="switchAuthLink" class="switch-link">Sign in</span>';
  } else {
    document.getElementById('fullNameGroup').style.display = 'none';
    document.getElementById('authSubtitle').textContent = "Welcome back! Sign in to continue.";
    document.getElementById('mainAuthBtn').textContent = "Sign In";
    document.getElementById('switchAuth').innerHTML = 'Don\'t have an account? <span id="switchAuthLink" class="switch-link">Sign up</span>';
  }
  resetAuthForm();
  document.getElementById('switchAuthLink').onclick = arguments.callee;
};
// Password show/hide
document.getElementById('togglePassword').onclick = function() {
  let inp = document.getElementById('authPassword');
  if (inp.type === "password") {
    inp.type = "text";
    this.innerHTML = '<i class="far fa-eye-slash"></i>';
  } else {
    inp.type = "password";
    this.innerHTML = '<i class="far fa-eye"></i>';
  }
};

function showInitScreen() {
  document.getElementById('authSection').style.display = 'none';
  document.getElementById('initScreen').style.display = 'flex';
  setTimeout(() => {
    document.getElementById('initScreen').style.display = 'none';
    showMainApp();
  }, 1700);
}
function maskEmail(email) {
  if (!email) return "";
  let [name, domain] = email.split("@");
  if (!domain) return email;
  let visible = name[0];
  return visible + "*".repeat(Math.max(1, name.length-2)) + name[name.length-1] + "@" + domain;
}
function showMainApp() {
  document.getElementById('mainApp').style.display = 'block';
  document.getElementById('homeSection').classList.add('active');
  // Set user info
  const email = localStorage.getItem("friday_logged_in");
  const name = localStorage.getItem("friday_user_name") || "User";
  document.getElementById('userName').textContent = name.toUpperCase();
  document.getElementById('userEmail').textContent = maskEmail(email);
  document.getElementById('userAvatar').textContent = name[0] ? name[0].toUpperCase() : "U";
}
function bootApp() {
  const email = localStorage.getItem("friday_logged_in");
  if (email) {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('initScreen').style.display = 'flex';
    setTimeout(() => {
      document.getElementById('initScreen').style.display = 'none';
      showMainApp();
    }, 1200);
    return;
  }
  document.getElementById('authSection').style.display = '';
  document.getElementById('mainApp').style.display = 'none';
  document.getElementById('initScreen').style.display = 'none';
}
bootApp();

// Navbar Navigation
document.getElementById('navHome').onclick = function() {
  document.getElementById('homeSection').style.display = 'flex';
  this.classList.add('active');
};

// Logout
document.getElementById('logoutBtn').onclick = function() {
  localStorage.removeItem("friday_logged_in");
  localStorage.removeItem("friday_user_name");
  document.getElementById('mainApp').style.display = 'none';
  document.getElementById('authSection').style.display = '';
  document.getElementById('initScreen').style.display = 'none';
  document.getElementById('homeSection').classList.add('active');
  resetAuthForm();
};


// Mic logic (main orb)
// let micOn = false;
// const micBtn = document.getElementById('micBtn');
// const fridayStatus = document.getElementById('fridayStatus');
// const micStatus = document.getElementById('micStatus');

// -------------------------
// Mic & Voice Automation
// -------------------------
let micOn = false;
const micBtn = document.getElementById('micBtn');
const fridayStatus = document.getElementById('fridayStatus');
const micStatus = document.getElementById('micStatus');

micBtn.onclick = async function() {
  micOn = !micOn;

  if (micOn) {
    micBtn.classList.add('active');
    micBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
    fridayStatus.textContent = "Listening";
    micStatus.textContent = "Listening... Click to turn off";

    while (micOn) {
      try {
        // Step 1: Call STT API (speech-to-text)
        const sttRes = await fetch("/stt/", { method: "POST" });
        const sttData = await sttRes.json();
        const userSpeech = sttData.text || "";

        if (!userSpeech) {
          fridayStatus.textContent = "Didn't catch that, listening again...";
          await new Promise(res => setTimeout(res, 500));
          continue;
        }

        // Step 2: Check if it's an automation command
        const automationKeywords = ["open", "close", "youtube search", "content", "system", "google search"];
        const isAutomation = automationKeywords.some(kw => userSpeech.toLowerCase().startsWith(kw));

        if (isAutomation) {
          // Send command to automation backend
          await sendAutomationCommands([userSpeech]);
          fridayStatus.textContent = `Executed: ${userSpeech}`;
          micStatus.textContent = "Listening for next command...";
          await new Promise(res => setTimeout(res, 500));
          continue; // skip normal chatbot flow
        }

        // Step 3: Otherwise send to Chatbot
        const chatRes = await fetch("/chat/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ message: userSpeech }),
        });
        const chatData = await chatRes.json();
        const botReply = chatData.response || "⚠️ No response from assistant.";

        // Step 4: Call TTS API to speak response
        await fetch("/tts/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({ text: botReply }),
        });

        // Update UI
        fridayStatus.textContent = "Standby";
        micStatus.textContent = "Response delivered. Listening again...";
        await new Promise(res => setTimeout(res, 500));

      } catch (err) {
        console.error("Mic error:", err);
        fridayStatus.textContent = "Error";
        micStatus.textContent = "Something went wrong, retrying...";
        await new Promise(res => setTimeout(res, 1000));
      }
    }

    // Mic turned off manually
    micBtn.classList.remove('active');
    micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    fridayStatus.textContent = "Standby";
    micStatus.textContent = "Mic is off - Click to activate";

  } else {
    // Mic manually turned off
    micBtn.classList.remove('active');
    micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    fridayStatus.textContent = "Standby";
    micStatus.textContent = "Mic is off - Click to activate";
  }
};

// CSRF helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


// Redirect to chat page when chat button is clicked
document.getElementById('navChat').onclick = function () {
  window.location.href = "/chats/"; 
};



async function sendAutomationCommands(commands) {
  try {
      const params = new URLSearchParams();
      commands.forEach(cmd => params.append('commands[]', cmd));

      const response = await fetch(`/automation/?${params.toString()}`);
      const data = await response.json();

      if (data.success) {
          console.log("Automation executed:", data.result);
      } else {
          console.error("Error:", data.error);
      }
  } catch (err) {
      console.error("Fetch error:", err);
  }
}

