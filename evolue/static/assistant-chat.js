/* assistant-chat.js - Nerdy glasses picker + Activities icon + chat input */
(function() {
  var GREETINGS = {
    'creative_director': '*wakes up* All right, I am here. What is the brief?',
    'copywriter': '*wakes up, yawns* Copy desk is open. What are we writing?',
    'muse': '*yawns sleepily* ...a direction to follow?',
    'cataloger': '*wakes up* Catalog mode on. What are we filing?',
    'media_editor': '*wakes up* Editing bay is warm. Point me at media.',
    'release_gate': '*wakes up* Gate check ready - show me what cleared.',
    'publishing_worker': '*wakes up* Publishing desk on. What goes out?',
    'godzilla': '*stretches and yawns* ...treats?',
  };
  document.addEventListener('DOMContentLoaded', function() {
    var panel = document.querySelector('[data-assistant-chat]');
    if (!panel) return;
    var pickToggle = panel.querySelector('[data-chat-pick-toggle]');
    var pickMenu = panel.querySelector('[data-chat-pick-menu]');
    var messagesEl = panel.querySelector('[data-chat-messages]');
    var inputEl = panel.querySelector('[data-chat-input]');
    var greeted = new Set();
    if (pickToggle && pickMenu) {
      pickToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        pickMenu.hidden = !pickMenu.hidden;
        pickToggle.setAttribute('aria-expanded', String(!pickMenu.hidden));
      });
      document.addEventListener('click', function(e) {
        if (!pickMenu.contains(e.target) && !pickToggle.contains(e.target)) pickMenu.hidden = true;
      });
      pickMenu.querySelectorAll('[data-assistant-select]').forEach(function(opt) {
        opt.addEventListener('click', function() {
          pickMenu.hidden = true;
          var kind = opt.dataset.assistantSelect;
          var label = opt.dataset.assistantName || kind;
          panel.dataset.activeAssistant = kind;
          if (!greeted.has(kind) && messagesEl) {
            greeted.add(kind);
            var line = GREETINGS[kind] || '*wakes up* ' + label + ' is ready.';
            var bubble = document.createElement('div');
            bubble.className = 'chat-message assistant';
            bubble.innerHTML = '<div>' + line + '</div>';
            messagesEl.appendChild(bubble);
            messagesEl.scrollTop = messagesEl.scrollHeight;
          }
        });
      });
    }
    var activityBtn = panel.querySelector('[data-activity-open]');
    if (activityBtn) {
      activityBtn.addEventListener('click', function() {
        var dialog = document.querySelector('.assistant-panel');
        if (dialog && dialog.showModal) dialog.showModal();
      });
    }
    if (inputEl) {
      inputEl.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey && inputEl.value.trim()) {
          e.preventDefault();
          var text = inputEl.value.trim();
          inputEl.value = '';
          if (messagesEl) {
            var msg = document.createElement('div');
            msg.className = 'chat-message user';
            msg.innerHTML = '<div>' + text + '</div>';
            messagesEl.appendChild(msg);
            messagesEl.scrollTop = messagesEl.scrollHeight;
          }
        }
      });
    }
  });
})();
