function extractPageContent() {
  // Remove noise
  const noise = ['nav', 'footer', 'aside', 'script', 'style', 'noscript'];
  noise.forEach(tag => document.querySelectorAll(tag).forEach(el => el.remove()));

  // Prefer article/main, fall back to body
  const main = document.querySelector('article, main, [role="main"]') || document.body;
  
  return {
    url: window.location.href,
    title: document.title,
    text: main.innerText.trim().slice(0, 15000), // cap at 15k chars
    timestamp: new Date().toISOString(),
    source_type: 'browser'
  };
}

// Auto-capture on page load (debounced)
let captured = false;
window.addEventListener('load', () => {
  if (captured) return;
  captured = true;
  const data = extractPageContent();
  if (data.text.length < 200) return; // skip trivial pages
  chrome.runtime.sendMessage({ type: 'CAPTURE', payload: data });
});