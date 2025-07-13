'use client'

import { useState } from 'react'
import { AppSidebar } from '@/components/AppSidebar'
import { ChatInterface } from '@/components/ChatInterface'
import { MapView } from '@/components/MapView'

interface LocationData {
  city: string;
  country: string;
  coordinates?: [number, number];
  locations: {
    name: string;
    type: string;
    description?: string;
    coordinates?: [number, number];
  }[];
}

export default function ChatPage() {
  const [locationData, setLocationData] = useState<LocationData>({
    city: 'Tokyo',
    country: 'Japan',
    locations: []
  });

  const handleLocationUpdate = (newLocationData: LocationData) => {
    setLocationData(newLocationData);
  };

  return (
    <div className="flex h-screen bg-white">
      <AppSidebar />
      <div className="flex flex-1 min-w-0 flex-col lg:flex-row">
        <div className="flex-1 min-w-0 h-1/2 lg:h-full">
          <ChatInterface onLocationUpdate={handleLocationUpdate} />
        </div>
        <div className="flex-1 min-w-0 h-1/2 lg:h-full">
          <MapView 
            city={locationData.city}
            country={locationData.country}
            locations={locationData.locations}
          />
        </div>
      </div>
    </div>
  )
}