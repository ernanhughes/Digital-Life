document.addEventListener('click', async function (event) {
  const button = event.target.closest('[data-copy-prompt]');
  if (!button) return;

  const page = button.closest('.prompt-page');
  const code = page && page.querySelector('[data-prompt-body] pre code');
  if (!code) return;

  const original = button.textContent;

  try {
    await navigator.clipboard.writeText(code.textContent.trim());
    button.textContent = 'Copied';
  } catch (error) {
    const range = document.createRange();
    range.selectNodeContents(code);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    button.textContent = 'Select and copy';
  }

  window.setTimeout(function () {
    button.textContent = original;
  }, 1800);
});
