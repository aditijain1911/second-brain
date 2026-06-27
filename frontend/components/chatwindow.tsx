'use client';
import { useState } from 'react';

interface Source { url: string; title: string; timestamp: string; score: number; }
interface Message { role: 'user' | 'assistant'; content: string; sources?: Source[]; }

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    const res = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: input })
    });
    const data = await res.json();
    
    setMessages(prev => [...prev, { 
      role: 'assistant', 
      content: data.answer, 
      sources: data.sources 
    }]);
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto p-4">
      <div className="flex-1 overflow-y-auto space-y-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100'
            }`}>
              <p>{m.content}</p>
              {m.sources && <SourceCards sources={m.sources} />}
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-2 mt-4">
        <input 
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="What did I read about React last week?"
          className="flex-1 border rounded-xl px-4 py-3 focus:outline-none focus:ring-2"
        />
        <button onClick={send} className="bg-blue-600 text-white px-6 rounded-xl">
          {loading ? '...' : 'Ask'}
        </button>
      </div>
    </div>
  );
}