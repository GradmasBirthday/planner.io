import { NextRequest, NextResponse } from 'next/server'

// Helper function to extract travel parameters from user message
function extractTravelParams(message: string) {
  const messageLower = message.toLowerCase()
  
  // Default parameters
  const params = {
    destination: 'Tokyo, Japan',
    travel_dates: 'Next month',
    budget: '$2000-3000',
    travel_style: 'cultural',
    group_size: 1
  }
  
  // Extract destination
  if (messageLower.includes('tokyo') || messageLower.includes('japan')) {
    params.destination = 'Tokyo, Japan'
    params.travel_style = 'cultural'
  } else if (messageLower.includes('paris') || messageLower.includes('france')) {
    params.destination = 'Paris, France'
    params.travel_style = 'cultural'
  } else if (messageLower.includes('bali') || messageLower.includes('indonesia')) {
    params.destination = 'Bali, Indonesia'
    params.travel_style = 'relaxation'
  } else if (messageLower.includes('london') || messageLower.includes('england')) {
    params.destination = 'London, England'
    params.travel_style = 'cultural'
  }
  
  // Extract budget
  if (messageLower.includes('budget') || messageLower.includes('cheap')) {
    params.budget = '$500-1000'
    params.travel_style = 'budget'
  } else if (messageLower.includes('luxury') || messageLower.includes('expensive')) {
    params.budget = '$5000+'
    params.travel_style = 'luxury'
  }
  
  // Extract group size
  if (messageLower.includes('family')) {
    params.group_size = 4
    params.travel_style = 'family'
  } else if (messageLower.includes('couple')) {
    params.group_size = 2
  }
  
  return params
}

export async function POST(request: NextRequest) {
  try {
    const { message, tripData } = await request.json()

    // Extract travel parameters from the message
    const travelParams = extractTravelParams(message)

    // Call the Python FastAPI travel planning endpoint
    const response = await fetch('http://localhost:8000/api/v1/travel/plan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        destination: travelParams.destination,
        travel_dates: travelParams.travel_dates,
        budget: travelParams.budget,
        travel_style: travelParams.travel_style,
        group_size: travelParams.group_size
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    
    if (data.success) {
      return NextResponse.json({
        message: `Here's your personalized travel plan for ${travelParams.destination}:\n\n${data.message}`,
        data: data.data,
        powered_by: 'TripMaxx Travel Planning API'
      })
    } else {
      return NextResponse.json(
        { error: data.message || 'Failed to create travel plan' },
        { status: 500 }
      )
    }
  } catch (error) {
    console.error('Travel Planning API error:', error)
    return NextResponse.json(
      { error: 'Failed to process travel planning request. Make sure the Python server is running on port 8000 with the travel API.' },
      { status: 500 }
    )
  }
}