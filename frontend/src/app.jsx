import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!input.trim()) return
    const question = input
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
      const data = await res.json()
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources
      }])
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: ' + e.message }])
    }
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1 style={{ borderBottom: '2px solid #333', paddingBottom: '10px' }}>🧠 Second Brain</h1>
      <div style={{ height: '500px', overflowY: 'auto', border: '1px solid #ddd', borderRadius: '8px', padding: '16px', marginBottom: '16px', backgroundColor: '#f9f9f9' }}>
        {messages.length === 0 && (
          <p style={{ color: '#999', textAlign: 'center', marginTop: '200px' }}>Ask me anything you've read...</p>
        )}
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: '16px', display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <div style={{ maxWidth: '70%', padding: '12px 16px', borderRadius: '12px', backgroundColor: m.role === 'user' ? '#007bff' : '#fff', color: m.role === 'user' ? '#fff' : '#333', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
              <p style={{ margin: 0 }}>{m.content}</p>
              {m.sources && m.sources.length > 0 && (
                <div style={{ marginTop: '8px', fontSize: '12px', opacity: 0.7 }}>
                  {m.sources.slice(0, 2).map((s, j) => (
                    <a key={j} href={s.url} target="_blank" rel="noreferrer" style={{ display: 'block', color: 'inherit' }}>📄 {s.url}</a>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && <div style={{ textAlign: 'center', color: '#999' }}>Thinking...</div>}
      </div>
      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="What did I read about neural networks?"
          style={{ flex: 1, padding: '12px 16px', borderRadius: '8px', border: '1px solid #ddd', fontSize: '16px' }}
        />
        <button onClick={send} disabled={loading}
          style={{ padding: '12px 24px', borderRadius: '8px', backgroundColor: '#007bff', color: '#fff', border: 'none', cursor: 'pointer', fontSize: '16px' }}>
          {loading ? '...' : 'Ask'}
        </button>
      </div>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)