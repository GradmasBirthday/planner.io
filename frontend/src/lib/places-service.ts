interface PlaceData {
  name: string;
  type: string;
  description?: string;
  coordinates?: [number, number];
  rating?: number;
  price_range?: string;
  opening_hours?: string;
  category?: string;
}

interface BackendLocalExperience {
  name: string;
  description: string;
  category: string;
  location: string;
  price_range?: string;
  rating?: number;
  opening_hours?: string;
  booking_required: boolean;
  contact_info?: string;
  why_recommended: string;
  seasonal_info?: string;
}

interface BackendLocalDiscoveryResponse {
  success: boolean;
  message: string;
  data: {
    location: string;
    interests: string[];
    total_results: number;
    experiences: BackendLocalExperience[];
    events: Array<{
      name: string;
      date?: string;
      location?: string;
      description?: string;
    }>;
    restaurants: Array<{
      name: string;
      cuisine?: string;
      rating?: number;
      price_range?: string;
      location?: string;
    }>;
    attractions: Array<{
      name: string;
      category?: string;
      rating?: number;
      description?: string;
      location?: string;
    }>;
    deals: Array<{
      description: string;
      discount?: string;
      expires?: string;
    }>;
  };
}

class PlacesService {
  private readonly baseUrl = 'http://localhost:8000/api/v1';

  /**
   * Fetch famous places for a city using the backend local discovery API
   */
  async getFamousPlaces(city: string, country: string = ''): Promise<PlaceData[]> {
    try {
      const location = country ? `${city}, ${country}` : city;
      
      // Default interests for famous places
      const interests = [
        'landmarks',
        'museums',
        'attractions',
        'restaurants',
        'cultural sites',
        'historical places',
        'parks',
        'shopping',
        'nightlife',
        'local experiences'
      ];

      const requestBody = {
        location,
        interests,
        travel_dates: null,
        budget: null
      };

      const response = await fetch(`${this.baseUrl}/local/discover`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: BackendLocalDiscoveryResponse = await response.json();

      if (!data.success) {
        throw new Error(data.message || 'Failed to fetch places');
      }

      return this.transformBackendData(data.data);
    } catch (error) {
      console.error('Error fetching famous places:', error);
      // Return fallback data based on the city
      return this.getFallbackPlaces(city, country);
    }
  }

  /**
   * Transform backend response data into the format expected by MapView
   */
  private transformBackendData(data: BackendLocalDiscoveryResponse['data']): PlaceData[] {
    const places: PlaceData[] = [];

    // Transform experiences
    data.experiences.forEach(experience => {
      places.push({
        name: experience.name,
        type: this.mapCategoryToType(experience.category),
        description: experience.description,
        rating: experience.rating,
        price_range: experience.price_range,
        opening_hours: experience.opening_hours
      });
    });

    // Transform attractions
    data.attractions.forEach(attraction => {
      places.push({
        name: attraction.name,
        type: this.mapCategoryToType(attraction.category || 'attraction'),
        description: attraction.description,
        rating: attraction.rating
      });
    });

    // Transform restaurants
    data.restaurants.forEach(restaurant => {
      places.push({
        name: restaurant.name,
        type: 'restaurant',
        description: `${restaurant.cuisine || 'Local'} cuisine`,
        rating: restaurant.rating,
        price_range: restaurant.price_range
      });
    });

    // Transform events
    data.events.forEach(event => {
      places.push({
        name: event.name,
        type: 'event',
        description: event.description || `Event on ${event.date}`
      });
    });

    return places;
  }

  /**
   * Map backend category to MapView type
   */
  private mapCategoryToType(category: string): string {
    const categoryMapping: { [key: string]: string } = {
      'museum': 'museum',
      'park': 'park',
      'restaurant': 'restaurant',
      'cafe': 'cafe',
      'shopping': 'shopping',
      'landmark': 'landmark',
      'historical': 'landmark',
      'cultural': 'museum',
      'entertainment': 'entertainment',
      'nightlife': 'nightlife',
      'nature': 'park',
      'religious': 'religious',
      'district': 'district',
      'accommodation': 'accommodation',
      'transport': 'transport'
    };

    const normalizedCategory = category.toLowerCase();
    return categoryMapping[normalizedCategory] || 'attraction';
  }

  /**
   * Get fallback places when API fails
   */
  private getFallbackPlaces(city: string, country: string): PlaceData[] {
    const cityKey = city.toLowerCase();
    
    const fallbackData: { [key: string]: PlaceData[] } = {
      'tokyo': [
        { name: "Tokyo National Museum", type: "museum", description: "Japan's premier museum", rating: 4.5 },
        { name: "Ueno Park", type: "park", description: "Beautiful cherry blossom park", rating: 4.3 },
        { name: "Akihabara", type: "shopping", description: "Electronics and anime district", rating: 4.2 },
        { name: "Shinjuku", type: "district", description: "Bustling business district", rating: 4.4 },
        { name: "Tokyo Tower", type: "landmark", description: "Iconic communications tower", rating: 4.1 },
        { name: "Ginza", type: "shopping", description: "Luxury shopping district", rating: 4.5 },
        { name: "Daikanyama", type: "district", description: "Trendy neighborhood", rating: 4.3 }
      ],
      'paris': [
        { name: "Eiffel Tower", type: "landmark", description: "Iconic iron lattice tower", rating: 4.6 },
        { name: "Louvre Museum", type: "museum", description: "World's largest art museum", rating: 4.5 },
        { name: "Notre-Dame Cathedral", type: "religious", description: "Gothic cathedral", rating: 4.4 },
        { name: "Arc de Triomphe", type: "landmark", description: "Triumphant arch", rating: 4.3 },
        { name: "Montmartre", type: "district", description: "Artistic hilltop district", rating: 4.5 },
        { name: "Champs-Élysées", type: "shopping", description: "Famous shopping avenue", rating: 4.2 }
      ],
      'london': [
        { name: "Big Ben", type: "landmark", description: "Iconic clock tower", rating: 4.4 },
        { name: "Tower of London", type: "landmark", description: "Historic castle", rating: 4.3 },
        { name: "British Museum", type: "museum", description: "World-famous museum", rating: 4.5 },
        { name: "Hyde Park", type: "park", description: "Royal park", rating: 4.2 },
        { name: "Buckingham Palace", type: "landmark", description: "Royal residence", rating: 4.1 },
        { name: "London Eye", type: "landmark", description: "Giant observation wheel", rating: 4.0 }
      ],
      'new york': [
        { name: "Statue of Liberty", type: "landmark", description: "Symbol of freedom", rating: 4.5 },
        { name: "Times Square", type: "district", description: "Bustling commercial area", rating: 4.1 },
        { name: "Central Park", type: "park", description: "Urban oasis", rating: 4.6 },
        { name: "Empire State Building", type: "landmark", description: "Art Deco skyscraper", rating: 4.3 },
        { name: "Metropolitan Museum", type: "museum", description: "World-class art museum", rating: 4.7 },
        { name: "Brooklyn Bridge", type: "landmark", description: "Iconic suspension bridge", rating: 4.5 }
      ]
    };

    return fallbackData[cityKey] || [
      { name: "City Center", type: "district", description: "Main city center", rating: 4.0 },
      { name: "Local Museum", type: "museum", description: "City's main museum", rating: 4.0 },
      { name: "Central Park", type: "park", description: "City's main park", rating: 4.0 },
      { name: "Historic District", type: "district", description: "Historic area", rating: 4.0 }
    ];
  }
}

export const placesService = new PlacesService();
export type { PlaceData }; 