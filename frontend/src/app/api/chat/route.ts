import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { message, tripData } = await request.json()

    // Call the Python FastAPI server
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    if (data.success) {
      return NextResponse.json({
        message: data.message,
        powered_by: data.powered_by
      })
    } else {
      return NextResponse.json(
        { error: data.message },
        { status: 500 }
      )
    }
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Failed to process chat message. Make sure the Python server is running on port 8000.' },
      { status: 500 }
    )
  }
}