export function initChatWidget() {
  const widget = document.getElementById('chat-widget');
  const panel = document.getElementById('chat-widget-panel');
  const toggle = document.getElementById('chat-widget-toggle');
  const closeBtn = document.getElementById('chat-widget-close');

  if (!widget || !panel || !toggle) {
    return;
  }

  const setOpen = (isOpen) => {
    widget.dataset.chatOpen = isOpen ? 'true' : 'false';
    panel.hidden = !isOpen;
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.setAttribute('aria-label', isOpen ? 'Закрити чат' : 'Відкрити чат');

    if (isOpen) {
      widget.dispatchEvent(new CustomEvent('chatOpen'));
      const input = panel.querySelector('#chat-message-input');
      if (input) {
        window.requestAnimationFrame(() => input.focus());
      }
    }
  };

  toggle.addEventListener('click', () => {
    setOpen(panel.hidden);
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => setOpen(false));
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !panel.hidden) {
      setOpen(false);
    }
  });
}
