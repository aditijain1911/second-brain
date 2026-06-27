import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { question } = await req.json();

  const res = await fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();
  return NextResponse.json(data);
}