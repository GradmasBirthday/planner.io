import { useState, useRef, useEffect } from "react";
import { 
  Send, 
  MessageCircle, 
  Search, 
  Heart, 
  MoreHorizontal, 
  ThumbsUp, 
  ThumbsDown, 
  Plus, 
  Mic, 
  Paperclip,
  Sparkles,
  Globe,
  Calendar,
  MapPin,
  DollarSign,
  Users,
  Clock,
  Star,
  Bookmark,
  Share2,
  Copy,
  RefreshCw
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
  avatar: string;
  avatarColor: "purple" | "dark" | "gradient";
  showActions?: boolean;
  timestamp: Date;
  suggestions?: string[];
  tripData?: {
    destination?: string;
    duration?: string;
    budget?: string;
    style?: string;
  };
}

interface QuickAction {
  icon: React.ReactNode;
  label: string;
  description: string;
  action: () => void;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: inputMessage,
      avatar: "👤",
      avatarColor: "purple",
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage("");
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentMessage,
          tripData: null
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get AI response');
      }

      const data = await response.json();
      
      // Simulate typing delay for better UX
      setTimeout(() => {
        const aiResponse: Message = {
          id: (Date.now() + 1).toString(),
          type: "assistant",
          content: data.message,
          avatar: "🤖",
          avatarColor: "gradient",
          showActions: true,
          timestamp: new Date(),
          suggestions: [
            "Plan a beach vacation",
            "Find budget-friendly options",
            "Explore cultural experiences",
            "Get restaurant recommendations"
          ]
        };
        
        setMessages(prev => [...prev, aiResponse]);
        setIsLoading(false);
        setIsTyping(false);
      }, 1500);

    } catch (error) {
      console.error('Error calling chat API:', error);
      
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: "I'm sorry, I'm having trouble connecting to our travel planning service right now. Please try again in a moment!",
        avatar: "🤖",
        avatarColor: "gradient",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorResponse]);
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputMessage(suggestion);
    inputRef.current?.focus();
  };

  const quickActions: QuickAction[] = [
    {
      icon: <Globe className="w-5 h-5" />,
      label: "Plan Trip",
      description: "Create a complete itinerary",
      action: () => setInputMessage("Plan a 7-day trip to Europe")
    },
    {
      icon: <Calendar className="w-5 h-5" />,
      label: "Find Dates",
      description: "Best time to visit",
      action: () => setInputMessage("When is the best time to visit Japan?")
    },
    {
      icon: <DollarSign className="w-5 h-5" />,
      label: "Budget Planning",
      description: "Cost estimates & tips",
      action: () => setInputMessage("Plan a budget-friendly trip under $2000")
    },
    {
      icon: <MapPin className="w-5 h-5" />,
      label: "Local Gems",
      description: "Hidden spots & experiences",
      action: () => setInputMessage("Find hidden gems in Paris")
    }
  ];

  return (
    <div className="flex-1 flex flex-col h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Modern Header */}
      <div className="bg-white border-b border-slate-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">
                  AI Travel Assistant
                </h1>
                <p className="text-sm text-slate-600">Powered by Google Gemini</p>
              </div>
            </div>
            <div className="flex items-center gap-2 px-3 py-1 bg-green-100 rounded-full">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs font-medium text-green-700">Online</span>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm" className="flex items-center gap-2">
              <Bookmark className="w-4 h-4" />
              Saved
            </Button>
            <Button variant="outline" size="sm" className="flex items-center gap-2">
              <Share2 className="w-4 h-4" />
              Share
            </Button>
            <Button size="sm" className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white">
              <Plus className="w-4 h-4" />
              New Trip
            </Button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={action.action}
              className="flex items-center gap-3 p-3 bg-slate-50 border border-slate-200 rounded-xl hover:bg-white hover:border-slate-300 transition-all duration-200 hover:shadow-sm group"
            >
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-white group-hover:scale-110 transition-transform">
                {action.icon}
              </div>
              <div className="text-left">
                <div className="text-sm font-semibold text-slate-900">{action.label}</div>
                <div className="text-xs text-slate-600">{action.description}</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <div className="mx-auto w-20 h-20 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-3xl flex items-center justify-center mb-6 shadow-lg">
              <Sparkles className="h-10 w-10 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900 mb-3">Welcome to AI Travel Planning</h3>
            <p className="text-slate-600 mb-8 max-w-lg mx-auto text-lg">
              I'm your AI travel companion powered by Google Gemini. Tell me about your dream trip and I'll help you plan the perfect adventure.
            </p>
            
            {/* Quick Prompts */}
            <div className="space-y-4">
              <p className="text-sm text-slate-500 font-medium">Try these examples:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {[
                  "Plan a 5-day foodie trip to Tokyo",
                  "Beach vacation for under $2000",
                  "Cultural tour of Europe",
                  "Adventure trip to New Zealand"
                ].map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => setInputMessage(prompt)}
                    className="p-4 text-left bg-white border border-slate-200 rounded-xl hover:bg-slate-50 hover:border-slate-300 text-slate-700 transition-all duration-200 hover:shadow-md hover:scale-[1.02]"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                        <Sparkles className="w-4 h-4 text-white" />
                      </div>
                      <span className="font-medium">{prompt}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            {message.type === 'assistant' && (
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg">
                {message.avatar}
              </div>
            )}
            
            <div className={`max-w-[70%] ${message.type === 'user' ? 'order-first' : ''}`}>
              <div className={`p-4 rounded-2xl ${
                message.type === 'user' 
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg' 
                  : 'bg-white border border-slate-200 shadow-sm text-slate-900'
              }`}>
                <div className="prose prose-sm max-w-none">
                  {message.content}
                </div>
              </div>
              
              {message.showActions && (
                <div className="flex items-center gap-2 mt-3 ml-2">
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                    <ThumbsUp className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                    <ThumbsDown className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                    <Copy className="w-4 h-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                    <Bookmark className="w-4 h-4" />
                  </Button>
                </div>
              )}

              {message.suggestions && (
                <div className="mt-4 space-y-2">
                  <p className="text-sm text-slate-600 font-medium">Try asking about:</p>
                  <div className="flex flex-wrap gap-2">
                    {message.suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="px-3 py-1.5 text-sm bg-slate-50 border border-slate-200 rounded-full hover:bg-white hover:border-slate-300 text-slate-700 transition-all duration-200 hover:shadow-sm"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {message.type === 'user' && (
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg">
                {message.avatar}
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-4 justify-start">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg">
              🤖
            </div>
            <div className="max-w-[70%]">
              <div className="p-4 bg-white border border-slate-200 rounded-2xl shadow-sm">
                <div className="flex items-center space-x-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-slate-600 font-medium">Planning your perfect trip...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Modern Input */}
      <div className="bg-white border-t border-slate-200 p-6">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" className="h-12 w-12 p-0 hover:bg-slate-100 rounded-xl">
            <Paperclip className="w-5 h-5" />
          </Button>
          
          <div className="flex-1 relative">
            <Input 
              ref={inputRef}
              placeholder="Ask me anything about travel planning..." 
              className="pr-24 h-12 rounded-xl border-slate-200 bg-white text-slate-900 placeholder:text-slate-400 focus:border-slate-300 transition-all duration-200"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
              <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg">
                <Mic className="w-4 h-4" />
              </Button>
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg"
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
          
          <Button 
            size="sm" 
            className="h-12 px-6 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white rounded-xl font-medium"
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
          >
            {isLoading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
} 