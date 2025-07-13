import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { ArrowLeft, MapPin, Clock, Star, Heart, Share2, Filter, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';

// Mock locations for Tokyo
const tokyoLocations = [
  { name: "Tokyo National Museum", coords: [139.7756, 35.7188], type: "museum", rating: 4.5, time: "2-3 hours" },
  { name: "Ueno Park", coords: [139.7717, 35.7148], type: "park", rating: 4.3, time: "1-2 hours" },
  { name: "Aoyama Flower Market Tea House", coords: [139.7143, 35.6684], type: "cafe", rating: 4.7, time: "1 hour" },
  { name: "Akihabara", coords: [139.7731, 35.7022], type: "shopping", rating: 4.2, time: "3-4 hours" },
  { name: "Shinjuku", coords: [139.7036, 35.6895], type: "district", rating: 4.4, time: "2-3 hours" },
  { name: "The Pizza Bar 38th", coords: [139.7638, 35.6812], type: "restaurant", rating: 4.6, time: "1-2 hours" },
  { name: "Don", coords: [139.7006, 35.6762], type: "restaurant", rating: 4.8, time: "1 hour" },
  { name: "Ginza", coords: [139.7671, 35.6735], type: "shopping", rating: 4.5, time: "2-3 hours" },
  { name: "Tokyo Tower", coords: [139.7454, 35.6586], type: "landmark", rating: 4.1, time: "1-2 hours" },
  { name: "Ivy Place", coords: [139.7289, 35.6654], type: "cafe", rating: 4.4, time: "1 hour" },
  { name: "Daikanyama", coords: [139.6989, 35.6499], type: "district", rating: 4.3, time: "2-3 hours" },
  { name: "Meguro Museum of Art, Tokyo", coords: [139.7159, 35.6341], type: "museum", rating: 4.0, time: "1-2 hours" },
  { name: "Bills Odaiba", coords: [139.7753, 35.6297], type: "restaurant", rating: 4.6, time: "1-2 hours" },
  { name: "Trattoria Pizzeria Amici", coords: [139.7011, 35.6585], type: "restaurant", rating: 4.7, time: "1-2 hours" }
];

const locationTypes = [
  { type: "all", label: "All", count: tokyoLocations.length },
  { type: "restaurant", label: "Restaurants", count: 4 },
  { type: "cafe", label: "Cafes", count: 2 },
  { type: "museum", label: "Museums", count: 2 },
  { type: "shopping", label: "Shopping", count: 2 },
  { type: "landmark", label: "Landmarks", count: 1 },
  { type: "park", label: "Parks", count: 1 },
  { type: "district", label: "Districts", count: 2 },
];

export function MapView() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const initializeMap = () => {
    if (!mapContainer.current) return;

    // Get Mapbox token from environment variable
    const mapboxToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    
    if (!mapboxToken) {
      setMapError('Mapbox token not configured. Please add NEXT_PUBLIC_MAPBOX_TOKEN to your environment variables.');
      return;
    }

    mapboxgl.accessToken = mapboxToken;
    
    try {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/light-v11',
        center: [139.7319, 35.6762], // Tokyo center
        zoom: 11,
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');

      // Add markers for Tokyo locations
      tokyoLocations.forEach((location) => {
        const el = document.createElement('div');
        el.className = 'marker';
        el.style.cssText = `
          background: none;
          border: none;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
        `;
        el.innerHTML = `
          <div style="background: linear-gradient(135deg, #3b82f6, #06b6d4); border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(59,130,246,0.18);">
            <svg width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>
              <path d='M12 21c-4.8-5.3-7-8.2-7-11A7 7 0 0 1 19 10c0 2.8-2.2 5.7-7 11z'/><circle cx='12' cy='10' r='3'/>
            </svg>
          </div>
        `;

        el.addEventListener('mouseenter', () => {
          el.style.transform = 'scale(1.2)';
        });
        el.addEventListener('mouseleave', () => {
          el.style.transform = 'scale(1)';
        });

        new mapboxgl.Marker(el)
          .setLngLat(location.coords as [number, number])
          .setPopup(
            new mapboxgl.Popup({ 
              offset: 25,
              className: 'custom-popup'
            })
              .setHTML(`
                <div class="p-4 min-w-[200px]">
                  <div class="flex items-start justify-between mb-2">
                    <h3 class="font-semibold text-slate-900">${location.name}</h3>
                    <div class="flex items-center gap-1">
                      <span class="inline-flex items-center"><svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#facc15' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg></span>
                      <span class="text-sm font-medium">${location.rating}</span>
                    </div>
                  </div>
                  <div class="flex items-center gap-2 text-xs text-slate-600 mb-3">
                    <div class="px-2 py-1 bg-slate-100 rounded-full">${location.type}</div>
                    <div class="flex items-center gap-1">
                      <svg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='#64748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/></svg>
                      ${location.time}
                    </div>
                  </div>
                  <div class="flex gap-2">
                    <button class="flex-1 px-3 py-1.5 bg-blue-500 text-white text-xs rounded-lg hover:bg-blue-600 transition-colors">
                      Save
                    </button>
                    <button class="px-3 py-1.5 border border-slate-200 text-xs rounded-lg hover:bg-slate-50 transition-colors">
                      Share
                    </button>
                  </div>
                </div>
              `)
          )
          .addTo(map.current!);
      });

      map.current.on('load', () => {
        setMapLoaded(true);
      });

    } catch (error) {
      console.error('Failed to initialize map:', error);
      setMapError('Failed to load map. Please check your Mapbox token.');
    }
  };

  useEffect(() => {
    initializeMap();
    
    return () => {
      map.current?.remove();
    };
  }, []);

  const filteredLocations = tokyoLocations.filter(location => {
    const matchesType = selectedType === "all" || location.type === selectedType;
    const matchesSearch = location.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  return (
    <div className="w-96 h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex flex-col shadow-xl">
      {/* Modern Header */}
      <div className="bg-white/90 backdrop-blur-md border-b border-slate-200/50 p-4">
        <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg">
            <ArrowLeft className="w-4 h-4" />
          </Button>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Tokyo, Japan</h2>
              <p className="text-xs text-slate-600">Explore amazing destinations</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg">
              <Heart className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg">
              <Share2 className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search locations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white/80 backdrop-blur-sm border border-slate-200/50 rounded-xl focus:bg-white focus:border-slate-300 transition-all duration-200 text-sm"
          />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200/50 p-3">
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-hide">
          {locationTypes.map((type) => (
            <button
              key={type.type}
              onClick={() => setSelectedType(type.type)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all duration-200 ${
                selectedType === type.type
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-sm'
                  : 'bg-white/80 backdrop-blur-sm border border-slate-200/50 text-slate-700 hover:bg-white hover:border-slate-300'
              }`}
            >
              <span>{type.label}</span>
              <span className={`px-1.5 py-0.5 rounded-full text-xs ${
                selectedType === type.type ? 'bg-white/20' : 'bg-slate-100'
              }`}>
                {type.count}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Error Message */}
      {mapError && (
        <div className="p-4 bg-red-50 border-b border-red-200">
          <div className="space-y-3">
            <p className="text-sm text-red-600">
              {mapError}
            </p>
            <p className="text-xs text-red-500">
              Add <code className="bg-red-100 px-1 rounded">NEXT_PUBLIC_MAPBOX_TOKEN</code> to your <code className="bg-red-100 px-1 rounded">.env.local</code> file
            </p>
          </div>
        </div>
      )}

      {/* Map Container */}
      <div className="flex-1 relative">
        <div ref={mapContainer} className="w-full h-full" />
        
        {/* Location List Overlay */}
        {mapLoaded && !mapError && (
          <div className="absolute bottom-4 left-4 right-4">
            <div className="bg-white/90 backdrop-blur-md rounded-xl p-4 shadow-lg border border-slate-200/50">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className="text-sm font-semibold text-slate-900">Top Locations</div>
                  <div className="text-xs text-slate-600">
                    {filteredLocations.length} of {tokyoLocations.length} places
                  </div>
                </div>
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg">
                  <Filter className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-2 max-h-32 overflow-y-auto">
                {filteredLocations.slice(0, 3).map((location, index) => (
                  <div key={index} className="flex items-center gap-3 p-2 bg-white/80 backdrop-blur-sm rounded-lg hover:bg-white transition-all duration-200 cursor-pointer">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                      <MapPin className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-slate-900 truncate">{location.name}</div>
                      <div className="flex items-center gap-2 text-xs text-slate-600">
                        <span className="px-1.5 py-0.5 bg-slate-100 rounded-full">{location.type}</span>
                        <div className="flex items-center gap-1">
                          <Star className="w-3 h-3 text-yellow-400 fill-current" />
                          {location.rating}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 