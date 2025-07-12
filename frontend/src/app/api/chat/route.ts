import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

async function callGeminiBackend(message: string): Promise<any> {
  return new Promise((resolve, reject) => {
    // Path to the Python script
    const scriptPath = path.join(process.cwd(), '..', 'src', 'planner', 'api_handler.py')
    
    // Spawn Python process
    const pythonProcess = spawn('python3', [scriptPath, message], {
      cwd: path.join(process.cwd(), '..'),
      env: { ...process.env }
    })

    let output = ''
    let errorOutput = ''

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString()
    })

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(output)
          resolve(result)
        } catch (error) {
          reject(new Error(`Failed to parse Python output: ${output}`))
        }
      } else {
        reject(new Error(`Python script failed with code ${code}: ${errorOutput}`))
      }
    })

    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`))
    })
  })
}

export async function POST(request: NextRequest) {
  try {
    const { message, tripData } = await request.json()

    // Check if we should use the actual Gemini backend
    const useGemini = true // Always try to use Gemini if available

    if (useGemini) {
      try {
        // Call the Gemini backend
        const geminiResult = await callGeminiBackend(message)
        
        if (geminiResult.success) {
          return NextResponse.json({
            message: geminiResult.message,
            params: geminiResult.params,
            powered_by: geminiResult.powered_by || "Google Gemini"
          })
        } else {
          // Fall back to simulated response if Gemini fails
          console.warn('Gemini failed:', geminiResult.error)
        }
      } catch (error) {
        console.error('Error calling Gemini:', error)
      }
    }

    // Simulated response (fallback or development mode)
    const response = {
      message: `I'd love to help you plan that trip! Based on your request: "${message}", I can create a personalized itinerary using our AI travel agents powered by Gemini.

Let me gather some information about:
• Your preferred travel dates
• Your budget range  
• What type of experiences you're most interested in
• Any specific requirements or preferences

I'll research the best flights, accommodations, and activities for your trip. Would you like me to start with a specific destination or do you have a particular travel style in mind?

*Note: Currently running in demo mode. For full AI planning, set up your GOOGLE_API_KEY environment variable.*`,
      tripSuggestions: [
        {
          destination: "Tokyo, Japan",
          style: "Foodie Adventure",
          duration: "5 days",
          highlights: ["Tsukiji Market", "Ramen Tours", "Sushi Experiences"]
        },
        {
          destination: "Paris, France", 
          style: "Cultural & Romantic",
          duration: "7 days",
          highlights: ["Louvre Museum", "Seine River Cruise", "Montmartre Walking Tour"]
        }
      ],
      powered_by: "Demo Mode"
    }

    return NextResponse.json(response)
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Failed to process chat message' },
      { status: 500 }
    )
  }
}