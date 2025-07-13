import { PlaneTakeoffIcon, MapIcon, UsersIcon, CameraIcon } from 'lucide-react'
import Link from 'next/link'
import { TripMaxxLogo } from '@/components/TripMaxxLogo'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-red-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <TripMaxxLogo size="sm" variant="white" />
            </div>
            <div className="hidden md:flex space-x-8">
              <Link href="/chat" className="text-gray-700 hover:text-blue-600">Plan Trip</Link>
              <Link href="/inspiration" className="text-gray-700 hover:text-blue-600">Inspiration</Link>
              <Link href="/my-trips" className="text-gray-700 hover:text-blue-600">My Trips</Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Your AI Travel Companion
          </h1>
          <div className="flex justify-center mb-6">
            <TripMaxxLogo size="lg" />
          </div>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Plan perfect trips with conversational AI. Get personalized itineraries, 
            real-time bookings, and travel inspiration tailored just for you.
          </p>
          
          {/* CTA Section */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link 
              href="/chat"
              className="bg-red-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-red-700 transition-colors"
            >
              Start Planning
            </Link>
            <Link 
              href="/quiz"
              className="bg-white text-red-600 border-2 border-red-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-red-50 transition-colors"
            >
              Take Travel Quiz
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mt-20">
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <MapIcon className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Trip Planning</h3>
              <p className="text-gray-600">
                Chat naturally to create personalized itineraries with flights, hotels, and activities.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <UsersIcon className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Group Planning</h3>
              <p className="text-gray-600">
                Collaborate with friends, vote on activities, and plan together in real-time.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <PlaneTakeoffIcon className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Real-time Booking</h3>
              <p className="text-gray-600">
                Book flights, hotels, and activities with live pricing and instant confirmation.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <CameraIcon className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Start Anywhere™</h3>
              <p className="text-gray-600">
                Drop a photo, link, or screenshot to instantly generate relevant trip ideas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
