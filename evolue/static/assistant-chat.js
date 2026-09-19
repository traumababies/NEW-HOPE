/* assistant-chat.js — AI Team chatbox stub */
document.addEventListener('DOMContentLoaded', function() {
  var input = document.querySelector('.chat-input');
  var messages = document.querySelector('.chat-messages');
  if (!input || !messages) return;
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && input.value.trim()) {
      var msg = document.createElement('div');
      msg.className = 'chat-message user';
      msg.textContent = input.value.trim();
      messages.appendChild(msg);
      input.value = '';
      messages.scrollTop = messages.scrollHeight;
    }
  });
});