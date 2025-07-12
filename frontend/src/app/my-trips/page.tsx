'use client'

import { useState } from 'react'
import { PlusIcon, MapPinIcon, CalendarIcon, UsersIcon, ShareIcon, EditIcon, TrashIcon, ChevronRightIcon } from 'lucide-react'

interface Trip {
  id: string
  title: string
  destination: string
  startDate: string
  endDate: string
  status: 'upcoming' | 'ongoing' | 'completed'
  participants: number
  budget: string
  image: string
  progress: number
}

interface Itinerary {
  day: number
  date: string
  activities: {
    time: string
    title: string
    location: string
    type: 'activity' | 'food' | 'transport' | 'accommodation'
    cost?: string
    completed?: boolean
  }[]
}

export default function MyTripsPage() {
  const [selectedTrip, setSelectedTrip] = useState<string | null>(null)

  const sampleTrips: Trip[] = [
    {
      id: '1',
      title: 'Tokyo Foodie Adventure',
      destination: 'Tokyo, Japan',
      startDate: '2024-03-15',
      endDate: '2024-03-20',
      status: 'upcoming',
      participants: 2,
      budget: '$2,500',
      image: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400',
      progress: 85
    },
    {
      id: '2',
      title: 'Bali Wellness Retreat',
      destination: 'Bali, Indonesia',
      startDate: '2024-02-10',
      endDate: '2024-02-17',
      status: 'completed',
      participants: 1,
      budget: '$1,800',
      image: 'https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=400',
      progress: 100
    },
    {
      id: '3',
      title: 'European Cultural Tour',
      destination: 'Paris, Rome, Barcelona',
      startDate: '2024-05-01',
      endDate: '2024-05-14',
      status: 'upcoming',
      participants: 4,
      budget: '$4,200',
      image: 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=400',
      progress: 60
    }
  ]

  const sampleItinerary: Itinerary[] = [
    {
      day: 1,
      date: '2024-03-15',
      activities: [
        { time: '09:00', title: 'Arrive at Haneda Airport', location: 'Tokyo', type: 'transport' },
        { time: '11:00', title: 'Check into Hotel', location: 'Shibuya', type: 'accommodation', cost: '$150' },
        { time: '14:00', title: 'Tsukiji Outer Market Food Tour', location: 'Tsukiji', type: 'food', cost: '$45', completed: true },
        { time: '19:00', title: 'Dinner at Jiro\'s Sushi', location: 'Ginza', type: 'food', cost: '$300' }
      ]
    },
    {
      day: 2,
      date: '2024-03-16',
      activities: [
        { time: '09:00', title: 'Visit Senso-ji Temple', location: 'Asakusa', type: 'activity', cost: 'Free' },
        { time: '12:00', title: 'Ramen Tasting Tour', location: 'Shibuya', type: 'food', cost: '$60' },
        { time: '15:00', title: 'Tokyo National Museum', location: 'Ueno', type: 'activity', cost: '$15' },
        { time: '18:00', title: 'Sake Bar Hopping', location: 'Golden Gai', type: 'activity', cost: '$80' }
      ]
    }
  ]

  const getStatusColor = (status: Trip['status']) => {
    switch (status) {
      case 'upcoming': return 'bg-blue-100 text-blue-800'
      case 'ongoing': return 'bg-green-100 text-green-800'
      case 'completed': return 'bg-gray-100 text-gray-800'
    }
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'food': return '🍜'
      case 'activity': return '🎯'
      case 'transport': return '✈️'
      case 'accommodation': return '🏨'
      default: return '📍'
    }
  }

  if (selectedTrip) {
    const trip = sampleTrips.find(t => t.id === selectedTrip)
    if (!trip) return null

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <button 
                  onClick={() => setSelectedTrip(null)}
                  className="mr-4 text-gray-500 hover:text-gray-700"
                >
                  ← Back to Trips
                </button>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">{trip.title}</h1>
                  <p className="text-gray-600">{trip.destination}</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <button className="p-2 text-gray-500 hover:text-gray-700">
                  <ShareIcon className="h-5 w-5" />
                </button>
                <button className="p-2 text-gray-500 hover:text-gray-700">
                  <EditIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Itinerary */}
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Trip Overview */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Trip Overview</h3>
                <div className="space-y-3">
                  <div className="flex items-center text-sm">
                    <CalendarIcon className="h-4 w-4 text-gray-400 mr-2" />
                    <span>{trip.startDate} - {trip.endDate}</span>
                  </div>
                  <div className="flex items-center text-sm">
                    <UsersIcon className="h-4 w-4 text-gray-400 mr-2" />
                    <span>{trip.participants} participants</span>
                  </div>
                  <div className="flex items-center text-sm">
                    <span className="text-gray-400 mr-2">💰</span>
                    <span>{trip.budget} budget</span>
                  </div>
                </div>
                
                <div className="mt-4">
                  <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Planning Progress</span>
                    <span>{trip.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${trip.progress}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Daily Itinerary */}
            <div className="lg:col-span-2">
              <div className="space-y-6">
                {sampleItinerary.map((day) => (
                  <div key={day.day} className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Day {day.day} - {day.date}
                      </h3>
                    </div>
                    <div className="p-6">
                      <div className="space-y-4">
                        {day.activities.map((activity, index) => (
                          <div key={index} className="flex items-start space-x-4 group">
                            <div className="flex-shrink-0">
                              <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center text-lg">
                                {getActivityIcon(activity.type)}
                              </div>
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center justify-between">
                                <div>
                                  <h4 className="text-sm font-medium text-gray-900">{activity.title}</h4>
                                  <p className="text-sm text-gray-500">{activity.location}</p>
                                </div>
                                <div className="text-right">
                                  <p className="text-sm font-medium text-gray-900">{activity.time}</p>
                                  {activity.cost && (
                                    <p className="text-sm text-gray-500">{activity.cost}</p>
                                  )}
                                </div>
                              </div>
                              {activity.completed && (
                                <div className="mt-1">
                                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                    ✓ Completed
                                  </span>
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-900">My Trips</h1>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700">
              <PlusIcon className="h-5 w-5" />
              <span>Plan New Trip</span>
            </button>
          </div>
        </div>
      </div>

      {/* Trips Grid */}
      <div className="max-w-6xl mx-auto px-6 py-6">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sampleTrips.map((trip) => (
            <div key={trip.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer" onClick={() => setSelectedTrip(trip.id)}>
              <div className="aspect-w-16 aspect-h-9 relative overflow-hidden rounded-t-lg">
                <img 
                  src={trip.image} 
                  alt={trip.destination}
                  className="w-full h-48 object-cover"
                />
                <div className="absolute top-4 left-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(trip.status)}`}>
                    {trip.status.charAt(0).toUpperCase() + trip.status.slice(1)}
                  </span>
                </div>
              </div>
              
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{trip.title}</h3>
                
                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPinIcon className="h-4 w-4 mr-2" />
                    <span>{trip.destination}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <CalendarIcon className="h-4 w-4 mr-2" />
                    <span>{trip.startDate} - {trip.endDate}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <UsersIcon className="h-4 w-4 mr-2" />
                    <span>{trip.participants} participants</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-lg font-semibold text-gray-900">{trip.budget}</span>
                  <ChevronRightIcon className="h-5 w-5 text-gray-400" />
                </div>
                
                {trip.status === 'upcoming' && (
                  <div className="mt-4">
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Planning Progress</span>
                      <span>{trip.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all"
                        style={{ width: `${trip.progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
        
        {/* Empty State */}
        {sampleTrips.length === 0 && (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MapPinIcon className="h-12 w-12 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No trips yet</h3>
            <p className="text-gray-500 mb-6">Start planning your first adventure!</p>
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
              Plan Your First Trip
            </button>
          </div>
        )}
      </div>
    </div>
  )
}