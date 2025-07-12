export default function StatusPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-8 text-center">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Voyagia Status</h1>
        <p className="text-gray-600 mb-6">Your AI travel companion is ready!</p>
        
        <div className="space-y-3 text-left">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Frontend</span>
            <span className="text-sm text-green-600 font-medium">✓ Online</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Google Gemini</span>
            <span className="text-sm text-green-600 font-medium">✓ Connected</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">API Backend</span>
            <span className="text-sm text-green-600 font-medium">✓ Active</span>
          </div>
        </div>
        
        <div className="mt-6">
          <a 
            href="/chat" 
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Start Planning Trips
          </a>
        </div>
      </div>
    </div>
  )
}