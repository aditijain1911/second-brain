const API_URL = 'http://localhost:8000';

chrome.runtime.onMessage.addListener(async (msg) => {
  if (msg.type !== 'CAPTURE') return;
  try {
    await fetch(`${API_URL}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(msg.payload)
    });
  } catch (e) {
    // Queue locally if offline
    const q = await chrome.storage.local.get('queue') || { queue: [] };
    q.queue.push(msg.payload);
    await chrome.storage.local.set(q);
  }
});