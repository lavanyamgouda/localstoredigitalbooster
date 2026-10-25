// auth.js — Include this in ALL pages except login.html

function checkLogin() {
  var user = sessionStorage.getItem('db_user');
  if (!user) {
    window.location.href = '../login.html';
    return null;
  }
  return JSON.parse(user);
}

function logout() {
  if (confirm('Are you sure you want to logout?')) {
    sessionStorage.removeItem('db_user');
    window.location.href = '../login.html';
  }
}

function showUserInfo() {
  var user = checkLogin();
  if (!user) return;
  var avatar = document.getElementById('userAvatar');
  var initials = user.username.substring(0, 2).toUpperCase();
  if (avatar) {
    avatar.textContent = initials;
    avatar.title = user.username + ' (' + user.role + ')';
    avatar.style.cursor = 'pointer';
    avatar.onclick = function() {
      if (confirm('Logout as ' + user.username + '?')) {
        sessionStorage.removeItem('db_user');
        window.location.href = '../login.html';
      }
    };
  }
  var logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.style.display = 'block';
    logoutBtn.textContent = 'Logout (' + user.username + ')';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  showUserInfo();
});