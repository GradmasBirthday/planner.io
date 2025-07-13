'use client'

import { useState } from 'react'
import { ChevronLeftIcon, ChevronRightIcon, CheckIcon } from 'lucide-react'

interface QuizQuestion {
  id: string
  question: string
  type: 'single' | 'multiple'
  options: { id: string; label: string; emoji: string }[]
}

interface QuizAnswers {
  [questionId: string]: string[]
}

const quizQuestions: QuizQuestion[] = [
  {
    id: 'travel_style',
    question: 'What describes your ideal travel style?',
    type: 'single',
    options: [
      { id: 'adventure', label: 'Adventure & Outdoor Activities', emoji: '🏔️' },
      { id: 'cultural', label: 'Cultural & Historical Sites', emoji: '🏛️' },
      { id: 'relaxation', label: 'Relaxation & Wellness', emoji: '🧘‍♀️' },
      { id: 'foodie', label: 'Food & Culinary Experiences', emoji: '🍜' },
      { id: 'nightlife', label: 'Nightlife & Entertainment', emoji: '🎭' },
      { id: 'nature', label: 'Nature & Wildlife', emoji: '🦋' }
    ]
  },
  {
    id: 'accommodation',
    question: 'What type of accommodation do you prefer?',
    type: 'single',
    options: [
      { id: 'luxury', label: 'Luxury Hotels & Resorts', emoji: '🏨' },
      { id: 'boutique', label: 'Boutique Hotels', emoji: '🏩' },
      { id: 'local', label: 'Local Homestays & B&Bs', emoji: '🏠' },
      { id: 'budget', label: 'Hostels & Budget Options', emoji: '🛏️' },
      { id: 'unique', label: 'Unique Stays (Treehouses, etc.)', emoji: '🌳' },
      { id: 'camping', label: 'Camping & Glamping', emoji: '⛺' }
    ]
  },
  {
    id: 'activities',
    question: 'Which activities interest you most? (Select multiple)',
    type: 'multiple',
    options: [
      { id: 'museums', label: 'Museums & Art Galleries', emoji: '🎨' },
      { id: 'hiking', label: 'Hiking & Trekking', emoji: '🥾' },
      { id: 'beaches', label: 'Beach & Water Sports', emoji: '🏖️' },
      { id: 'shopping', label: 'Shopping & Markets', emoji: '🛍️' },
      { id: 'photography', label: 'Photography & Sightseeing', emoji: '📸' },
      { id: 'festivals', label: 'Local Festivals & Events', emoji: '🎪' }
    ]
  },
  {
    id: 'budget',
    question: 'What\'s your typical travel budget per person?',
    type: 'single',
    options: [
      { id: 'budget', label: 'Budget ($500-1500)', emoji: '💰' },
      { id: 'moderate', label: 'Moderate ($1500-3000)', emoji: '💳' },
      { id: 'comfort', label: 'Comfortable ($3000-5000)', emoji: '💎' },
      { id: 'luxury', label: 'Luxury ($5000+)', emoji: '👑' }
    ]
  },
  {
    id: 'trip_length',
    question: 'How long do you usually travel?',
    type: 'single',
    options: [
      { id: 'weekend', label: 'Weekend Trips (2-3 days)', emoji: '🏃' },
      { id: 'short', label: 'Short Trips (4-7 days)', emoji: '📅' },
      { id: 'medium', label: 'Medium Trips (1-2 weeks)', emoji: '📊' },
      { id: 'long', label: 'Extended Trips (2+ weeks)', emoji: '🗓️' }
    ]
  }
]

export default function QuizPage() {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<QuizAnswers>({})
  const [showResults, setShowResults] = useState(false)

  const handleAnswer = (questionId: string, optionId: string) => {
    const question = quizQuestions[currentQuestion]
    
    setAnswers(prev => {
      if (question.type === 'single') {
        return { ...prev, [questionId]: [optionId] }
      } else {
        const currentAnswers = prev[questionId] || []
        const isSelected = currentAnswers.includes(optionId)
        
        if (isSelected) {
          return { ...prev, [questionId]: currentAnswers.filter(id => id !== optionId) }
        } else {
          return { ...prev, [questionId]: [...currentAnswers, optionId] }
        }
      }
    })
  }

  const nextQuestion = () => {
    if (currentQuestion < quizQuestions.length - 1) {
      setCurrentQuestion(prev => prev + 1)
    } else {
      setShowResults(true)
    }
  }

  const prevQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1)
    }
  }

  const getTravelPersona = () => {
    const travelStyle = answers['travel_style']?.[0]
    const accommodation = answers['accommodation']?.[0]
    const budget = answers['budget']?.[0]
    
    if (travelStyle === 'adventure' && budget === 'budget') {
      return {
        title: 'The Budget Adventurer',
        description: 'You love outdoor activities and exploring nature while keeping costs low.',
        recommendations: ['Hostels & camping', 'Hiking trails', 'National parks', 'Local transportation']
      }
    } else if (travelStyle === 'cultural' && accommodation === 'luxury') {
      return {
        title: 'The Cultural Connoisseur',
        description: 'You appreciate art, history, and culture with a taste for luxury.',
        recommendations: ['Boutique hotels', 'Private tours', 'Fine dining', 'Museums & galleries']
      }
    } else if (travelStyle === 'foodie') {
      return {
        title: 'The Culinary Explorer',
        description: 'Your travels revolve around discovering amazing food and local cuisine.',
        recommendations: ['Food tours', 'Cooking classes', 'Local markets', 'Street food adventures']
      }
    } else if (travelStyle === 'relaxation') {
      return {
        title: 'The Wellness Seeker',
        description: 'You travel to unwind, recharge, and focus on your well-being.',
        recommendations: ['Spa resorts', 'Yoga retreats', 'Beach destinations', 'Meditation centers']
      }
    } else {
      return {
        title: 'The Well-Rounded Traveler',
        description: 'You enjoy a balanced mix of activities and experiences.',
        recommendations: ['Mixed itineraries', 'Diverse accommodations', 'Varied activities', 'Flexible planning']
      }
    }
  }

  const progress = ((currentQuestion + 1) / quizQuestions.length) * 100

  if (showResults) {
    const persona = getTravelPersona()
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="max-w-2xl mx-auto px-6 py-12">
          <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckIcon className="h-10 w-10 text-green-600" />
            </div>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Your Travel Persona</h1>
            <h2 className="text-2xl font-semibold text-blue-600 mb-4">{persona.title}</h2>
            <p className="text-gray-600 mb-8 text-lg">{persona.description}</p>
            
            <div className="bg-gray-50 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended for you:</h3>
              <div className="space-y-2">
                {persona.recommendations.map((rec, index) => (
                  <div key={index} className="flex items-center text-gray-700">
                    <CheckIcon className="h-4 w-4 text-green-500 mr-2" />
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => window.location.href = '/chat'}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Start Planning a Trip
              </button>
              <button
                onClick={() => {
                  setCurrentQuestion(0)
                  setAnswers({})
                  setShowResults(false)
                }}
                className="bg-white text-gray-700 border border-gray-300 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
              >
                Retake Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const question = quizQuestions[currentQuestion]
  const currentAnswers = answers[question.id] || []
  const canProceed = currentAnswers.length > 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="max-w-2xl mx-auto px-6 py-12">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Question {currentQuestion + 1} of {quizQuestions.length}</span>
            <span>{Math.round(progress)}% complete</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            {question.question}
          </h1>

          <div className="space-y-3 mb-8">
            {question.options.map((option) => {
              const isSelected = currentAnswers.includes(option.id)
              return (
                <button
                  key={option.id}
                  onClick={() => handleAnswer(question.id, option.id)}
                  className={`w-full p-4 rounded-lg border-2 transition-all text-left flex items-center space-x-4 ${
                    isSelected
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-2xl">{option.emoji}</span>
                  <span className="text-gray-900 font-medium">{option.label}</span>
                  {isSelected && (
                    <CheckIcon className="h-5 w-5 text-blue-600 ml-auto" />
                  )}
                </button>
              )
            })}
          </div>

          {question.type === 'multiple' && (
            <p className="text-sm text-gray-500 text-center mb-6">
              You can select multiple options
            </p>
          )}

          {/* Navigation */}
          <div className="flex justify-between">
            <button
              onClick={prevQuestion}
              disabled={currentQuestion === 0}
              className={`flex items-center px-4 py-2 rounded-lg ${
                currentQuestion === 0
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <ChevronLeftIcon className="h-5 w-5 mr-1" />
              Previous
            </button>

            <button
              onClick={nextQuestion}
              disabled={!canProceed}
              className={`flex items-center px-6 py-2 rounded-lg font-medium ${
                canProceed
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}
            >
              {currentQuestion === quizQuestions.length - 1 ? 'See Results' : 'Next'}
              <ChevronRightIcon className="h-5 w-5 ml-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}