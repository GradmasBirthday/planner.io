'use client'

import { AppSidebar } from '@/components/AppSidebar'
import { ChatInterface } from '@/components/ChatInterface'
import { MapView } from '@/components/MapView'

export default function ChatPage() {
  return (
    <div className="flex h-screen bg-white">
      <AppSidebar />
      <div className="flex flex-1 min-w-0 flex-col lg:flex-row">
        <div className="flex-1 min-w-0 h-1/2 lg:h-full">
          <ChatInterface />
        </div>
        <div className="flex-1 min-w-0 h-1/2 lg:h-full">
          <MapView />
        </div>
      </div>
    </div>
  )
}