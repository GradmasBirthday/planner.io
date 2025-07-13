'use client'

import { AppSidebar } from '@/components/AppSidebar'
import { ChatInterface } from '@/components/ChatInterface'
import { MapView } from '@/components/MapView'

export default function ChatPage() {
  return (
    <div className="flex h-screen bg-white">
      <AppSidebar />
      <ChatInterface />
      <MapView />
    </div>
  )
}