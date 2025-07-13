import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { ArrowLeft, MapPin, Clock, Star, Heart, Share2, Filter, Search, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { geocodingService } from '@/lib/geocoding';
import { placesService, PlaceData } from '@/lib/places-service';

interface MapViewProps {
  city?: string;
  country?: string;
  locations?: PlaceData[];
}

// Mock locations for Tokyo (matching PlaceData interface)
const tokyoLocations: PlaceData[] = [
  { name: "Tokyo National Museum", coordinates: [139.7756, 35.7188], type: "museum", rating: 4.5, opening_hours: "9:30-17:00", description: "Japan's premier museum" },
  { name: "Ueno Park", coordinates: [139.7717, 35.7148], type: "park", rating: 4.3, opening_hours: "24/7", description: "Beautiful cherry blossom park" },
  { name: "Aoyama Flower Market Tea House", coordinates: [139.7143, 35.6684], type: "cafe", rating: 4.7, opening_hours: "11:00-20:00", description: "Unique flower-themed cafe" },
  { name: "Akihabara", coordinates: [139.7731, 35.7022], type: "shopping", rating: 4.2, opening_hours: "10:00-20:00", description: "Electronics and anime district" },
  { name: "Shinjuku", coordinates: [139.7036, 35.6895], type: "district", rating: 4.4, description: "Bustling business district" },
  { name: "The Pizza Bar 38th", coordinates: [139.7638, 35.6812], type: "restaurant", rating: 4.6, opening_hours: "17:00-23:00", price_range: "$$$" },
  { name: "Don", coordinates: [139.7006, 35.6762], type: "restaurant", rating: 4.8, opening_hours: "11:00-21:00", price_range: "$$" },
  { name: "Ginza", coordinates: [139.7671, 35.6735], type: "shopping", rating: 4.5, opening_hours: "10:00-20:00", description: "Luxury shopping district" },
  { name: "Tokyo Tower", coordinates: [139.7454, 35.6586], type: "landmark", rating: 4.1, opening_hours: "9:00-22:30", description: "Iconic communications tower" },
  { name: "Ivy Place", coordinates: [139.7289, 35.6654], type: "cafe", rating: 4.4, opening_hours: "11:00-22:00", price_range: "$$" },
  { name: "Daikanyama", coordinates: [139.6989, 35.6499], type: "district", rating: 4.3, description: "Trendy neighborhood" },
  { name: "Meguro Museum of Art, Tokyo", coordinates: [139.7159, 35.6341], type: "museum", rating: 4.0, opening_hours: "10:00-18:00", description: "Contemporary art museum" },
  { name: "Bills Odaiba", coordinates: [139.7753, 35.6297], type: "restaurant", rating: 4.6, opening_hours: "8:00-22:00", price_range: "$$$" },
  { name: "Trattoria Pizzeria Amici", coordinates: [139.7011, 35.6585], type: "restaurant", rating: 4.7, opening_hours: "11:30-23:00", price_range: "$$" }
];

export function MapView({ 
  city = "Tokyo", 
  country = "Japan", 
  locations = tokyoLocations 
}: MapViewProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [cityCoordinates, setCityCoordinates] = useState<[number, number]>([139.7319, 35.6762]);
  const [processedLocations, setProcessedLocations] = useState<PlaceData[]>(locations);
  const [markers, setMarkers] = useState<mapboxgl.Marker[]>([]);
  const [loadingPlaces, setLoadingPlaces] = useState(false);
  const [placesError, setPlacesError] = useState<string | null>(null);

  // Dynamic location types based on processed locations
  const locationTypes = [
    { type: "all", label: "All", count: processedLocations.length },
    ...Array.from(new Set(processedLocations.map((loc: PlaceData) => loc.type))).map((type: string) => ({
      type,
      label: type.charAt(0).toUpperCase() + type.slice(1) + 's',
      count: processedLocations.filter((loc: PlaceData) => loc.type === type).length
    }))
  ];

  // Function to fetch famous places for the current city
  const fetchFamousPlaces = async () => {
    if (!city) return;
    
    setLoadingPlaces(true);
    setPlacesError(null);
    
    try {
      const places = await placesService.getFamousPlaces(city, country);
      setProcessedLocations(places);
    } catch (error) {
      console.error('Error fetching famous places:', error);
      setPlacesError('Failed to load famous places');
      // Keep existing locations on error
    } finally {
      setLoadingPlaces(false);
    }
  };

  // Get city coordinates and fetch famous places when city changes
  useEffect(() => {
    const getCityCoords = async () => {
      const coords = await geocodingService.getCityCoordinates(city, country);
      if (coords) {
        setCityCoordinates(coords);
      }
    };
    getCityCoords();
    
    // Fetch famous places for the new city
    fetchFamousPlaces();
  }, [city, country]);

  // Get location coordinates when processed locations change
  useEffect(() => {
    const getLocationCoords = async () => {
      if (processedLocations.length === 0) return;
      
      const locationsWithCoords = await geocodingService.getLocationCoordinates(
        processedLocations.map(loc => ({ name: loc.name, city: `${city}, ${country}` }))
      );
      
      const updatedLocations = processedLocations.map(loc => {
        const coordResult = locationsWithCoords.find(c => c.name === loc.name);
        return {
          ...loc,
          coordinates: coordResult?.coordinates || undefined
        };
      });
      
      setProcessedLocations(updatedLocations);
    };
    
    // Only fetch coordinates if locations don't already have them
    const needsCoordinates = processedLocations.some(loc => !loc.coordinates);
    if (needsCoordinates) {
      getLocationCoords();
    }
  }, [processedLocations.length, city, country]);

  // Update map center when city coordinates change
  useEffect(() => {
    if (map.current && cityCoordinates) {
      map.current.setCenter(cityCoordinates);
    }
  }, [cityCoordinates]);

  // Update markers when processed locations change
  useEffect(() => {
    if (!map.current) return;

    // Clear existing markers
    markers.forEach(marker => marker.remove());
    
    // Add new markers
    const newMarkers: mapboxgl.Marker[] = [];
    
    processedLocations.forEach((location) => {
      // Skip locations without coordinates
      if (!location.coordinates) return;

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

             const marker = new mapboxgl.Marker(el)
         .setLngLat(location.coordinates as [number, number])
         .setPopup(
           new mapboxgl.Popup({ 
             offset: 25,
             className: 'custom-popup'
           })
             .setHTML(`
               <div class="p-4 min-w-[200px]">
                 <div class="flex items-start justify-between mb-2">
                   <h3 class="font-semibold text-slate-900">${location.name}</h3>
                   ${location.rating ? `<div class="flex items-center gap-1">
                     <span class="inline-flex items-center"><svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#facc15' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'/></svg></span>
                     <span class="text-sm font-medium">${location.rating}</span>
                   </div>` : ''}
                 </div>
                 <div class="flex items-center gap-2 text-xs text-slate-600 mb-3">
                   <div class="px-2 py-1 bg-slate-100 rounded-full">${location.type}</div>
                   ${location.opening_hours ? `<div class="flex items-center gap-1">
                     <svg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='#64748b' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/></svg>
                     ${location.opening_hours}
                   </div>` : ''}
                   ${location.price_range ? `<div class="px-2 py-1 bg-green-100 text-green-800 rounded-full">${location.price_range}</div>` : ''}
                 </div>
                 <div class="flex gap-2">
                   <button class="flex-1 px-3 py-1.5 bg-blue-500 text-white text-xs rounded-lg hover:bg-blue-600 transition-colors">
                     Save
                   </button>
                   <button class="px-3 py-1.5 border border-slate-200 text-xs rounded-lg hover:bg-slate-50 transition-colors">
                     Share
                   </button>
                 </div>
                 ${location.description ? `<div class="mt-2 text-xs text-slate-500">${location.description}</div>` : ''}
               </div>
             `)
         )
         .addTo(map.current!);

      newMarkers.push(marker);
    });

    setMarkers(newMarkers);
  }, [processedLocations]);

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
        center: cityCoordinates,
        zoom: 11,
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');



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

  const filteredLocations = processedLocations.filter(location => {
    const matchesType = selectedType === "all" || location.type === selectedType;
    const matchesSearch = location.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  return (
    <div className="flex-1 h-full bg-gradient-to-br from-slate-50 to-blue-50 flex flex-col shadow-xl">
      {/* Modern Header */}
      <div className="bg-white/90 backdrop-blur-md border-b border-slate-200/50 p-4">
        <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100 rounded-lg">
            <ArrowLeft className="w-4 h-4" />
          </Button>
            <div>
              <h2 className="text-lg font-bold text-slate-900">{city}{country ? `, ${country}` : ''}</h2>
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

      {/* Places Loading/Error */}
      {(loadingPlaces || placesError) && (
        <div className="p-4 bg-blue-50 border-b border-blue-200">
          {loadingPlaces && (
            <div className="flex items-center gap-2 text-sm text-blue-600">
              <Loader2 className="w-4 h-4 animate-spin" />
              Loading famous places for {city}...
            </div>
          )}
          {placesError && (
            <p className="text-sm text-orange-600">
              {placesError} - Using default locations
            </p>
          )}
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
                    {filteredLocations.length} of {processedLocations.length} places
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
                        {location.rating && (
                          <div className="flex items-center gap-1">
                            <Star className="w-3 h-3 text-yellow-400 fill-current" />
                            {location.rating}
                          </div>
                        )}
                        {location.price_range && (
                          <span className="px-1.5 py-0.5 bg-green-100 text-green-800 rounded-full">{location.price_range}</span>
                        )}
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