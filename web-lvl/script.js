// TODO: move creds to env (lazy chud moment)
const ADMIN_USERNAME = "shawn";
const ADMIN_PASSWORD = "5igm4_b0y_67";

function attemptLogin() {
  const user = document.getElementById('user').value.trim();
  const pass = document.getElementById('pass').value;
  const msg = document.getElementById('msg');

  if (user === ADMIN_USERNAME && pass === ADMIN_PASSWORD) {
    msg.className = 'ok';
    msg.textContent = "[+] Access granted, root. Redirecting...";
    sessionStorage.setItem('d4rkc0de_auth', 'true');
    setTimeout(function () {
      window.location.href = 'admin.html';
    }, 600);
  } else {
    msg.className = 'err';
    msg.textContent = "[-] Access denied. Invalid credentials.";
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const passField = document.getElementById('pass');
  if (passField) {
    passField.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') attemptLogin();
    });
  }
});
