import { 
  MessageCircle, 
  Heart, 
  Map, 
  Plus, 
  Settings, 
  HelpCircle, 
  LogOut, 
  User,
  Star,
  TrendingUp,
  Globe,
  Search
} from "lucide-react";
import { cn } from "@/lib/utils";
import { TripMaxxLogo } from "./TripMaxxLogo";

const navigationItems = [
  { 
    icon: MessageCircle, 
    label: "AI Assistant", 
    count: 1, 
    active: true,
    description: "Chat with AI"
  },
  { 
    icon: Map, 
    label: "My Trips", 
    count: 3,
    description: "Your itineraries"
  }
];

const recentChats = [
  { name: "Tokyo Food Tour Planning", time: "2 hours ago", unread: true },
  { name: "Paris Cultural Trip", time: "1 day ago", unread: false },
  { name: "NYC Adventure Ideas", time: "3 days ago", unread: false },
  { name: "Budget Europe Trip", time: "1 week ago", unread: false },
];

export function AppSidebar() {
  return (
    <div className="w-72 bg-gradient-to-b from-slate-800 to-slate-900 text-white h-screen flex flex-col shadow-2xl">
      {/* Logo Section */}
      <div className="p-4 border-b border-slate-700/50">
        <TripMaxxLogo size="sm" variant="white" />
        <div className="mt-2 flex items-center gap-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-xs text-slate-300">AI Travel Assistant</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="py-3 px-3">
        <div className="space-y-1">
          {navigationItems.map((item) => (
            <div
              key={item.label}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer transition-all duration-200 group",
                item.active 
                  ? "bg-blue-600/20 border border-blue-500/30 text-white" 
                  : "hover:bg-slate-700/50 text-slate-200 hover:text-white"
              )}
            >
              <div className={cn(
                "w-7 h-7 rounded-lg flex items-center justify-center transition-all duration-200",
                item.active 
                  ? "bg-blue-600 text-white" 
                  : "bg-slate-700/50 text-slate-300 group-hover:bg-slate-600/50 group-hover:text-white"
              )}>
                <item.icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium truncate">{item.label}</span>
                  {item.count && (
                    <span className="bg-blue-500 text-xs px-1.5 py-0.5 rounded-full font-medium">
                      {item.count}
                    </span>
                  )}
                </div>
                <div className="text-xs text-slate-400 truncate">{item.description}</div>
              </div>
            </div>
          ))}
        </div>
      </nav>

      {/* Recent Chats */}
      <div className="px-3 py-2 border-t border-slate-700/50">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xs font-semibold text-slate-200">Recent Chats</h3>
          <Search className="w-3 h-3 text-slate-400" />
        </div>
        <div className="space-y-1">
          {recentChats.map((chat, index) => (
            <div key={index} className="flex items-center gap-2 p-2 bg-slate-800/30 hover:bg-slate-700/30 rounded-lg cursor-pointer transition-all duration-200">
              <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                <MessageCircle className="w-3 h-3 text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium text-white truncate">{chat.name}</div>
                <div className="text-xs text-slate-400">{chat.time}</div>
              </div>
              {chat.unread && (
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="px-3 py-2 border-t border-slate-700/50">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xs font-semibold text-slate-200">Your Stats</h3>
          <TrendingUp className="w-3 h-3 text-slate-400" />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-slate-800/30 rounded-lg p-2">
            <div className="flex items-center gap-1 mb-1">
              <Globe className="w-3 h-3 text-blue-400" />
              <span className="text-xs text-slate-400">Countries</span>
            </div>
            <div className="text-sm font-bold text-white">12</div>
          </div>
          <div className="bg-slate-800/30 rounded-lg p-2">
            <div className="flex items-center gap-1 mb-1">
              <Star className="w-3 h-3 text-yellow-400" />
              <span className="text-xs text-slate-400">Reviews</span>
            </div>
            <div className="text-sm font-bold text-white">47</div>
          </div>
        </div>
      </div>

      {/* New Trip Button */}
      <div className="p-3 border-t border-slate-700/50">
        <button className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 py-2.5 rounded-lg text-center transition-all duration-200 font-medium shadow-lg hover:shadow-xl hover:scale-[1.02] flex items-center justify-center gap-2 text-sm">
          <Plus className="w-4 h-4" />
          New Trip
        </button>
      </div>

      {/* User Profile */}
      <div className="p-3 border-t border-slate-700/50">
        <div className="flex items-center gap-3 p-2 bg-slate-800/30 rounded-lg">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center shadow-lg">
            <User className="w-4 h-4 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-white">Sarah Johnson</div>
            <div className="text-xs text-slate-400 truncate">Premium Traveler</div>
          </div>
          <div className="flex items-center gap-1">
            <button className="p-1 hover:bg-slate-700/50 rounded transition-colors">
              <Settings className="w-3 h-3 text-slate-400" />
            </button>
            <button className="p-1 hover:bg-slate-700/50 rounded transition-colors">
              <HelpCircle className="w-3 h-3 text-slate-400" />
            </button>
            <button className="p-1 hover:bg-slate-700/50 rounded transition-colors">
              <LogOut className="w-3 h-3 text-slate-400" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 