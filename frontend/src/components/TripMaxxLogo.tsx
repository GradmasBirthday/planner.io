import React from 'react';

interface TripMaxxLogoProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'white' | 'blue';
  className?: string;
}

export function TripMaxxLogo({ size = 'md', variant = 'default', className = '' }: TripMaxxLogoProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const variantClasses = {
    default: 'bg-blue-600',
    white: 'bg-white',
    blue: 'bg-blue-700'
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* Logo Icon */}
      <div className={`${sizeClasses[size]} ${variantClasses[variant]} rounded-lg flex items-center justify-center shadow-lg`}>
        <div className="relative">
          {/* Airplane icon */}
          <svg 
            className={`${size === 'sm' ? 'w-4 h-4' : size === 'md' ? 'w-5 h-5' : 'w-7 h-7'} ${
              variant === 'white' ? 'text-blue-600' : 'text-white'
            }`}
            fill="currentColor" 
            viewBox="0 0 24 24"
          >
            <path d="M21.5 12.5c0-.3-.2-.5-.5-.5h-4.5l-1.5-4.5c-.1-.3-.4-.5-.7-.5s-.6.2-.7.5L16 12h-4.5l-1.5-4.5c-.1-.3-.4-.5-.7-.5s-.6.2-.7.5L8 12H3.5c-.3 0-.5.2-.5.5s.2.5.5.5H8l1.5 4.5c.1.3.4.5.7.5s.6-.2.7-.5L12 13h4.5l1.5 4.5c.1.3.4.5.7.5s.6-.2.7-.5L20 13h4.5c.3 0 .5-.2.5-.5z"/>
          </svg>
          
          {/* Globe overlay */}
          <div className={`absolute inset-0 flex items-center justify-center ${
            variant === 'white' ? 'text-blue-400' : 'text-white/80'
          }`}>
            <svg 
              className={`${size === 'sm' ? 'w-2 h-2' : size === 'md' ? 'w-2.5 h-2.5' : 'w-3 h-3'}`}
              fill="currentColor" 
              viewBox="0 0 24 24"
            >
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
            </svg>
          </div>
        </div>
      </div>
      
      {/* Text Logo */}
      <div className="flex flex-col">
        <span className={`font-bold ${
          size === 'sm' ? 'text-sm' : size === 'md' ? 'text-lg' : 'text-2xl'
        } text-blue-600`}>
          TripMaxx
        </span>
        <span className={`text-xs ${
          size === 'sm' ? 'text-gray-500' : size === 'md' ? 'text-gray-600' : 'text-gray-700'
        }`}>
          Travel AI
        </span>
      </div>
    </div>
  );
}

// Compact version for small spaces
export function TripMaxxLogoCompact({ size = 'md', variant = 'default', className = '' }: TripMaxxLogoProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const variantClasses = {
    default: 'bg-blue-600',
    white: 'bg-white',
    blue: 'bg-blue-700'
  };

  return (
    <div className={`${sizeClasses[size]} ${variantClasses[variant]} rounded-lg flex items-center justify-center shadow-lg ${className}`}>
      <div className="relative">
        {/* Airplane icon */}
        <svg 
          className={`${size === 'sm' ? 'w-4 h-4' : size === 'md' ? 'w-5 h-5' : 'w-7 h-7'} ${
            variant === 'white' ? 'text-blue-600' : 'text-white'
          }`}
          fill="currentColor" 
          viewBox="0 0 24 24"
        >
          <path d="M21.5 12.5c0-.3-.2-.5-.5-.5h-4.5l-1.5-4.5c-.1-.3-.4-.5-.7-.5s-.6.2-.7.5L16 12h-4.5l-1.5-4.5c-.1-.3-.4-.5-.7-.5s-.6.2-.7.5L8 12H3.5c-.3 0-.5.2-.5.5s.2.5.5.5H8l1.5 4.5c.1.3.4.5.7.5s.6-.2.7-.5L12 13h4.5l1.5 4.5c.1.3.4.5.7.5s.6-.2.7-.5L20 13h4.5c.3 0 .5-.2.5-.5z"/>
        </svg>
        
        {/* Globe overlay */}
        <div className={`absolute inset-0 flex items-center justify-center ${
          variant === 'white' ? 'text-blue-400' : 'text-white/80'
        }`}>
          <svg 
            className={`${size === 'sm' ? 'w-2 h-2' : size === 'md' ? 'w-2.5 h-2.5' : 'w-3 h-3'}`}
            fill="currentColor" 
            viewBox="0 0 24 24"
          >
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
          </svg>
        </div>
      </div>
    </div>
  );
}
