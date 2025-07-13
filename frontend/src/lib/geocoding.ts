interface GeocodingResult {
  name: string;
  coordinates: [number, number]; // [longitude, latitude]
  place_type: string;
  place_name: string;
  context?: {
    country?: string;
    region?: string;
    locality?: string;
  };
}

interface MapboxGeocodingResponse {
  features: {
    place_name: string;
    center: [number, number];
    place_type: string[];
    context?: {
      id: string;
      text: string;
    }[];
  }[];
}

class GeocodingService {
  private apiKey: string;
  private baseUrl = 'https://api.mapbox.com/geocoding/v5/mapbox.places';
  
  constructor() {
    this.apiKey = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || '';
    if (!this.apiKey) {
      console.warn('Mapbox token not found. Geocoding will use fallback coordinates.');
    }
  }

  /**
   * Get coordinates for a city
   */
  async getCityCoordinates(city: string, country?: string): Promise<[number, number] | null> {
    const query = country ? `${city}, ${country}` : city;
    const result = await this.geocode(query, ['place', 'locality', 'neighborhood']);
    return result ? result.coordinates : null;
  }

  /**
   * Get coordinates for multiple locations
   */
  async getLocationCoordinates(locations: { name: string; city: string }[]): Promise<{ name: string; coordinates: [number, number] | null }[]> {
    const results = await Promise.all(
      locations.map(async (location) => {
        const query = `${location.name}, ${location.city}`;
        const result = await this.geocode(query, ['poi', 'address', 'place']);
        return {
          name: location.name,
          coordinates: result ? result.coordinates : null
        };
      })
    );
    return results;
  }

  /**
   * Geocode a query string
   */
  private async geocode(query: string, types: string[] = []): Promise<GeocodingResult | null> {
    if (!this.apiKey) {
      return this.getFallbackCoordinates(query);
    }

    try {
      const encodedQuery = encodeURIComponent(query);
      const typeParams = types.length > 0 ? `&types=${types.join(',')}` : '';
      const url = `${this.baseUrl}/${encodedQuery}.json?access_token=${this.apiKey}&limit=1${typeParams}`;

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Geocoding API error: ${response.status}`);
      }

      const data: MapboxGeocodingResponse = await response.json();
      
      if (data.features.length === 0) {
        return this.getFallbackCoordinates(query);
      }

      const feature = data.features[0];
      return {
        name: feature.place_name,
        coordinates: feature.center,
        place_type: feature.place_type[0],
        place_name: feature.place_name,
        context: this.parseContext(feature.context)
      };
    } catch (error) {
      console.error('Geocoding error:', error);
      return this.getFallbackCoordinates(query);
    }
  }

  /**
   * Parse context from Mapbox response
   */
  private parseContext(context?: { id: string; text: string }[]) {
    if (!context) return undefined;

    const result: { country?: string; region?: string; locality?: string } = {};
    
    context.forEach(item => {
      if (item.id.startsWith('country')) {
        result.country = item.text;
      } else if (item.id.startsWith('region')) {
        result.region = item.text;
      } else if (item.id.startsWith('locality')) {
        result.locality = item.text;
      }
    });

    return result;
  }

  /**
   * Fallback coordinates for common cities when API is not available
   */
  private getFallbackCoordinates(query: string): GeocodingResult | null {
    const queryLower = query.toLowerCase();
    
    const fallbackCoordinates: { [key: string]: [number, number] } = {
      'tokyo': [139.6917, 35.6895],
      'tokyo, japan': [139.6917, 35.6895],
      'paris': [2.3522, 48.8566],
      'paris, france': [2.3522, 48.8566],
      'london': [-0.1276, 51.5074],
      'london, england': [-0.1276, 51.5074],
      'new york': [-74.0060, 40.7128],
      'new york, usa': [-74.0060, 40.7128],
      'rome': [12.4964, 41.9028],
      'rome, italy': [12.4964, 41.9028],
      'barcelona': [2.1734, 41.3851],
      'barcelona, spain': [2.1734, 41.3851],
      'amsterdam': [4.9041, 52.3676],
      'amsterdam, netherlands': [4.9041, 52.3676],
      'dubai': [55.2708, 25.2048],
      'dubai, uae': [55.2708, 25.2048],
      'singapore': [103.8198, 1.3521],
      'bangkok': [100.5018, 13.7563],
      'bangkok, thailand': [100.5018, 13.7563],
      'sydney': [151.2093, -33.8688],
      'sydney, australia': [151.2093, -33.8688],
      'bali': [115.0920, -8.3405],
      'bali, indonesia': [115.0920, -8.3405],
      'seoul': [126.9780, 37.5665],
      'seoul, south korea': [126.9780, 37.5665],
      'mumbai': [72.8777, 19.0760],
      'mumbai, india': [72.8777, 19.0760],
      'hong kong': [114.1694, 22.3193],
      'los angeles': [-118.2437, 34.0522],
      'los angeles, usa': [-118.2437, 34.0522],
      'berlin': [13.4050, 52.5200],
      'berlin, germany': [13.4050, 52.5200],
      'madrid': [-3.7038, 40.4168],
      'madrid, spain': [-3.7038, 40.4168],
      'vienna': [16.3738, 48.2082],
      'vienna, austria': [16.3738, 48.2082],
      'prague': [14.4378, 50.0755],
      'prague, czech republic': [14.4378, 50.0755],
      'istanbul': [28.9784, 41.0082],
      'istanbul, turkey': [28.9784, 41.0082],
      'cairo': [31.2357, 30.0444],
      'cairo, egypt': [31.2357, 30.0444],
      'cape town': [18.4241, -33.9249],
      'cape town, south africa': [18.4241, -33.9249],
      'rio de janeiro': [-43.1729, -22.9068],
      'rio de janeiro, brazil': [-43.1729, -22.9068],
      'mexico city': [-99.1332, 19.4326],
      'mexico city, mexico': [-99.1332, 19.4326],
      'toronto': [-79.3832, 43.6532],
      'toronto, canada': [-79.3832, 43.6532],
      'vancouver': [-123.1207, 49.2827],
      'vancouver, canada': [-123.1207, 49.2827],
    };

    // Check for exact matches
    for (const [city, coords] of Object.entries(fallbackCoordinates)) {
      if (queryLower.includes(city)) {
        return {
          name: query,
          coordinates: coords,
          place_type: 'place',
          place_name: query
        };
      }
    }

    // Default to Tokyo if no match found
    return {
      name: query,
      coordinates: [139.6917, 35.6895],
      place_type: 'place',
      place_name: query
    };
  }
}

export const geocodingService = new GeocodingService();
export type { GeocodingResult }; 