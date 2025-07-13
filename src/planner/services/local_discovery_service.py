#!/usr/bin/env python3
"""
Local Discovery Service - Provides famous places and attractions data
"""

import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models import LocalDiscoveryData, LocalExperience

class LocalDiscoveryService:
    """Service for discovering local famous places and attractions"""
    
    def __init__(self):
        self.places_database = self._load_places_database()
    
    def _load_places_database(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive database of famous places by city"""
        return {
            "tokyo": {
                "country": "Japan",
                "coordinates": [139.6503, 35.6762],
                "places": [
                    {
                        "name": "Senso-ji Temple",
                        "category": "religious",
                        "description": "Tokyo's oldest temple, founded in 628 AD",
                        "rating": 4.3,
                        "price_range": "Free",
                        "opening_hours": "6:00-17:00",
                        "interests": ["cultural", "religious", "historical", "landmarks"],
                        "why_recommended": "Most visited spiritual site in the world, iconic Tokyo landmark"
                    },
                    {
                        "name": "Tokyo National Museum",
                        "category": "museum",
                        "description": "Japan's premier museum with extensive collection of art and antiquities",
                        "rating": 4.5,
                        "price_range": "¥1,000",
                        "opening_hours": "9:30-17:00",
                        "interests": ["museums", "cultural", "art", "historical"],
                        "why_recommended": "World's largest collection of Japanese cultural artifacts"
                    },
                    {
                        "name": "Shibuya Crossing",
                        "category": "landmark",
                        "description": "World's busiest pedestrian crossing",
                        "rating": 4.2,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["landmarks", "urban", "photography"],
                        "why_recommended": "Iconic Tokyo experience, symbol of urban energy"
                    },
                    {
                        "name": "Ueno Park",
                        "category": "park",
                        "description": "Beautiful park famous for cherry blossoms and museums",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "5:00-23:00",
                        "interests": ["parks", "nature", "cherry blossoms", "cultural"],
                        "why_recommended": "Best cherry blossom viewing spot in Tokyo"
                    },
                    {
                        "name": "Tsukiji Outer Market",
                        "category": "food",
                        "description": "Famous food market with fresh sushi and street food",
                        "rating": 4.6,
                        "price_range": "¥500-2,000",
                        "opening_hours": "5:00-14:00",
                        "interests": ["food", "markets", "sushi", "local experiences"],
                        "why_recommended": "Best place for fresh sushi and authentic Japanese breakfast"
                    },
                    {
                        "name": "Tokyo Tower",
                        "category": "landmark",
                        "description": "Iconic communications tower with city views",
                        "rating": 4.1,
                        "price_range": "¥900-2,800",
                        "opening_hours": "9:00-22:30",
                        "interests": ["landmarks", "views", "photography"],
                        "why_recommended": "Classic Tokyo landmark with panoramic city views"
                    },
                    {
                        "name": "Ginza",
                        "category": "shopping",
                        "description": "Luxury shopping district with high-end boutiques",
                        "rating": 4.5,
                        "price_range": "¥¥¥¥",
                        "opening_hours": "10:00-20:00",
                        "interests": ["shopping", "luxury", "fashion"],
                        "why_recommended": "Tokyo's most prestigious shopping destination"
                    },
                    {
                        "name": "Meiji Shrine",
                        "category": "religious",
                        "description": "Peaceful Shinto shrine dedicated to Emperor Meiji",
                        "rating": 4.7,
                        "price_range": "Free",
                        "opening_hours": "6:00-18:00",
                        "interests": ["religious", "nature", "cultural", "peaceful"],
                        "why_recommended": "Spiritual oasis in the heart of Tokyo"
                    },
                    {
                        "name": "Akihabara",
                        "category": "district",
                        "description": "Electronics and anime culture district",
                        "rating": 4.2,
                        "price_range": "¥¥",
                        "opening_hours": "10:00-20:00",
                        "interests": ["electronics", "anime", "gaming", "otaku culture"],
                        "why_recommended": "Global center of electronics and anime culture"
                    },
                    {
                        "name": "Ramen Street",
                        "category": "food",
                        "description": "Famous ramen alley with multiple authentic shops",
                        "rating": 4.8,
                        "price_range": "¥800-1,500",
                        "opening_hours": "11:00-23:00",
                        "interests": ["food", "ramen", "local experiences", "authentic"],
                        "why_recommended": "Best authentic ramen experience in Tokyo"
                    }
                ]
            },
            "paris": {
                "country": "France",
                "coordinates": [2.3522, 48.8566],
                "places": [
                    {
                        "name": "Eiffel Tower",
                        "category": "landmark",
                        "description": "Iconic iron lattice tower and symbol of Paris",
                        "rating": 4.6,
                        "price_range": "€10-25",
                        "opening_hours": "9:30-23:45",
                        "interests": ["landmarks", "architecture", "views", "photography"],
                        "why_recommended": "Most visited paid monument in the world"
                    },
                    {
                        "name": "Louvre Museum",
                        "category": "museum",
                        "description": "World's largest art museum, home to the Mona Lisa",
                        "rating": 4.5,
                        "price_range": "€15",
                        "opening_hours": "9:00-18:00",
                        "interests": ["museums", "art", "culture", "history"],
                        "why_recommended": "World's most visited museum with unparalleled art collection"
                    },
                    {
                        "name": "Notre-Dame Cathedral",
                        "category": "religious",
                        "description": "Gothic cathedral masterpiece (currently under restoration)",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "8:00-18:45",
                        "interests": ["religious", "architecture", "history", "gothic"],
                        "why_recommended": "Masterpiece of French Gothic architecture"
                    },
                    {
                        "name": "Arc de Triomphe",
                        "category": "landmark",
                        "description": "Triumphal arch honoring those who fought for France",
                        "rating": 4.3,
                        "price_range": "€12",
                        "opening_hours": "10:00-22:30",
                        "interests": ["landmarks", "history", "views", "architecture"],
                        "why_recommended": "Historic monument with panoramic views of Paris"
                    },
                    {
                        "name": "Montmartre",
                        "category": "district",
                        "description": "Historic hilltop district with artistic heritage",
                        "rating": 4.5,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["art", "history", "bohemian", "views"],
                        "why_recommended": "Former home to Picasso, Renoir, and other famous artists"
                    },
                    {
                        "name": "Champs-Élysées",
                        "category": "shopping",
                        "description": "Famous avenue with shops, cafes, and theaters",
                        "rating": 4.2,
                        "price_range": "€€€",
                        "opening_hours": "10:00-20:00",
                        "interests": ["shopping", "cafes", "fashion", "luxury"],
                        "why_recommended": "World's most beautiful avenue"
                    },
                    {
                        "name": "Seine River Cruise",
                        "category": "experience",
                        "description": "Scenic boat tour along the Seine River",
                        "rating": 4.4,
                        "price_range": "€15-25",
                        "opening_hours": "10:00-22:00",
                        "interests": ["sightseeing", "relaxation", "views", "romantic"],
                        "why_recommended": "Best way to see Paris landmarks from the water"
                    },
                    {
                        "name": "Sacré-Cœur Basilica",
                        "category": "religious",
                        "description": "Beautiful white basilica atop Montmartre hill",
                        "rating": 4.6,
                        "price_range": "Free",
                        "opening_hours": "6:00-22:30",
                        "interests": ["religious", "architecture", "views"],
                        "why_recommended": "Stunning views over Paris and beautiful interior"
                    },
                    {
                        "name": "Latin Quarter",
                        "category": "district",
                        "description": "Historic student quarter with narrow streets and cafes",
                        "rating": 4.3,
                        "price_range": "€€",
                        "opening_hours": "24/7",
                        "interests": ["history", "cafes", "nightlife", "intellectual"],
                        "why_recommended": "Heart of intellectual Paris with vibrant atmosphere"
                    },
                    {
                        "name": "Versailles Palace",
                        "category": "historical",
                        "description": "Opulent royal palace with magnificent gardens",
                        "rating": 4.7,
                        "price_range": "€18",
                        "opening_hours": "9:00-17:30",
                        "interests": ["history", "palaces", "gardens", "luxury"],
                        "why_recommended": "Ultimate symbol of French royal extravagance"
                    }
                ]
            },
            "london": {
                "country": "United Kingdom",
                "coordinates": [-0.1276, 51.5074],
                "places": [
                    {
                        "name": "Big Ben",
                        "category": "landmark",
                        "description": "Iconic clock tower and symbol of London",
                        "rating": 4.4,
                        "price_range": "Free (exterior)",
                        "opening_hours": "24/7 (exterior)",
                        "interests": ["landmarks", "architecture", "history"],
                        "why_recommended": "Most recognizable symbol of London"
                    },
                    {
                        "name": "Tower of London",
                        "category": "historical",
                        "description": "Historic castle housing the Crown Jewels",
                        "rating": 4.3,
                        "price_range": "£25",
                        "opening_hours": "9:00-17:30",
                        "interests": ["history", "castles", "crown jewels", "medieval"],
                        "why_recommended": "Nearly 1000 years of British history"
                    },
                    {
                        "name": "British Museum",
                        "category": "museum",
                        "description": "World-class museum with global artifacts",
                        "rating": 4.5,
                        "price_range": "Free",
                        "opening_hours": "10:00-17:30",
                        "interests": ["museums", "history", "culture", "artifacts"],
                        "why_recommended": "One of the world's greatest museums"
                    },
                    {
                        "name": "Hyde Park",
                        "category": "park",
                        "description": "Large royal park in central London",
                        "rating": 4.2,
                        "price_range": "Free",
                        "opening_hours": "5:00-24:00",
                        "interests": ["parks", "nature", "relaxation", "royal"],
                        "why_recommended": "Perfect escape from city bustle"
                    },
                    {
                        "name": "Buckingham Palace",
                        "category": "landmark",
                        "description": "Official London residence of the British monarch",
                        "rating": 4.1,
                        "price_range": "£26.50",
                        "opening_hours": "9:30-19:30",
                        "interests": ["royal", "palaces", "architecture", "history"],
                        "why_recommended": "Heart of the British monarchy"
                    },
                    {
                        "name": "London Eye",
                        "category": "attraction",
                        "description": "Giant observation wheel with panoramic views",
                        "rating": 4.0,
                        "price_range": "£27",
                        "opening_hours": "10:00-20:30",
                        "interests": ["views", "modern", "photography"],
                        "why_recommended": "Best views of London skyline"
                    },
                    {
                        "name": "Camden Market",
                        "category": "market",
                        "description": "Eclectic market with food, crafts, and vintage finds",
                        "rating": 4.3,
                        "price_range": "£",
                        "opening_hours": "10:00-18:00",
                        "interests": ["markets", "food", "alternative", "vintage"],
                        "why_recommended": "Unique London subculture experience"
                    },
                    {
                        "name": "Tate Modern",
                        "category": "museum",
                        "description": "Modern art gallery in former power station",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "10:00-18:00",
                        "interests": ["art", "modern", "museums", "contemporary"],
                        "why_recommended": "World's leading modern art gallery"
                    },
                    {
                        "name": "Covent Garden",
                        "category": "district",
                        "description": "Historic market area with shops and street performers",
                        "rating": 4.2,
                        "price_range": "££",
                        "opening_hours": "10:00-20:00",
                        "interests": ["shopping", "entertainment", "street performers"],
                        "why_recommended": "Vibrant area with unique shopping and dining"
                    },
                    {
                        "name": "Westminster Abbey",
                        "category": "religious",
                        "description": "Gothic abbey where British monarchs are crowned",
                        "rating": 4.6,
                        "price_range": "£23",
                        "opening_hours": "9:30-15:30",
                        "interests": ["religious", "history", "architecture", "royal"],
                        "why_recommended": "Site of royal coronations and weddings"
                    }
                ]
            },
            "new york": {
                "country": "United States",
                "coordinates": [-74.0060, 40.7128],
                "places": [
                    {
                        "name": "Statue of Liberty",
                        "category": "landmark",
                        "description": "Iconic symbol of freedom and democracy",
                        "rating": 4.5,
                        "price_range": "$21.50",
                        "opening_hours": "8:30-16:00",
                        "interests": ["landmarks", "history", "symbols", "freedom"],
                        "why_recommended": "Universal symbol of freedom and democracy"
                    },
                    {
                        "name": "Times Square",
                        "category": "district",
                        "description": "Bustling commercial and entertainment hub",
                        "rating": 4.1,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["entertainment", "shopping", "urban", "nightlife"],
                        "why_recommended": "The crossroads of the world"
                    },
                    {
                        "name": "Central Park",
                        "category": "park",
                        "description": "Iconic urban park in Manhattan",
                        "rating": 4.6,
                        "price_range": "Free",
                        "opening_hours": "6:00-1:00",
                        "interests": ["parks", "nature", "jogging", "relaxation"],
                        "why_recommended": "Manhattan's green oasis"
                    },
                    {
                        "name": "Empire State Building",
                        "category": "landmark",
                        "description": "Art Deco skyscraper with observation decks",
                        "rating": 4.3,
                        "price_range": "$37",
                        "opening_hours": "8:00-2:00",
                        "interests": ["landmarks", "views", "architecture", "art deco"],
                        "why_recommended": "Iconic NYC skyline views"
                    },
                    {
                        "name": "Metropolitan Museum of Art",
                        "category": "museum",
                        "description": "World-renowned art museum",
                        "rating": 4.7,
                        "price_range": "$25",
                        "opening_hours": "10:00-17:00",
                        "interests": ["museums", "art", "culture", "history"],
                        "why_recommended": "One of the world's largest and most prestigious art museums"
                    },
                    {
                        "name": "Brooklyn Bridge",
                        "category": "landmark",
                        "description": "Historic suspension bridge connecting Manhattan and Brooklyn",
                        "rating": 4.5,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["landmarks", "architecture", "views", "walking"],
                        "why_recommended": "Architectural marvel with spectacular views"
                    },
                    {
                        "name": "9/11 Memorial & Museum",
                        "category": "memorial",
                        "description": "Moving tribute to September 11 victims",
                        "rating": 4.8,
                        "price_range": "$24",
                        "opening_hours": "9:00-20:00",
                        "interests": ["memorial", "history", "reflection", "remembrance"],
                        "why_recommended": "Important memorial and historical site"
                    },
                    {
                        "name": "High Line",
                        "category": "park",
                        "description": "Elevated park built on former railway line",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "7:00-22:00",
                        "interests": ["parks", "art", "urban renewal", "walking"],
                        "why_recommended": "Unique urban park experience"
                    },
                    {
                        "name": "Broadway Theater District",
                        "category": "entertainment",
                        "description": "World-famous theater district",
                        "rating": 4.7,
                        "price_range": "$50-200",
                        "opening_hours": "19:00-22:00",
                        "interests": ["theater", "entertainment", "musicals", "culture"],
                        "why_recommended": "Best theater productions in the world"
                    },
                    {
                        "name": "One World Trade Center",
                        "category": "landmark",
                        "description": "Tallest building in NYC with observation deck",
                        "rating": 4.2,
                        "price_range": "$32",
                        "opening_hours": "9:00-24:00",
                        "interests": ["landmarks", "views", "modern", "memorial"],
                        "why_recommended": "Symbol of resilience with amazing views"
                    }
                ]
            },
            "barcelona": {
                "country": "Spain",
                "coordinates": [2.1734, 41.3851],
                "places": [
                    {
                        "name": "Sagrada Familia",
                        "category": "religious",
                        "description": "Gaudí's unfinished basilica masterpiece",
                        "rating": 4.7,
                        "price_range": "€20",
                        "opening_hours": "9:00-20:00",
                        "interests": ["architecture", "religious", "gaudi", "art"],
                        "why_recommended": "Gaudí's architectural masterpiece"
                    },
                    {
                        "name": "Park Güell",
                        "category": "park",
                        "description": "Colorful park designed by Antoni Gaudí",
                        "rating": 4.5,
                        "price_range": "€7",
                        "opening_hours": "8:00-21:00",
                        "interests": ["parks", "art", "gaudi", "views"],
                        "why_recommended": "Whimsical park with stunning city views"
                    },
                    {
                        "name": "Las Ramblas",
                        "category": "street",
                        "description": "Famous pedestrian street in the heart of Barcelona",
                        "rating": 4.2,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["walking", "street performers", "cafes", "shopping"],
                        "why_recommended": "The pulse of Barcelona"
                    },
                    {
                        "name": "Gothic Quarter",
                        "category": "district",
                        "description": "Historic medieval neighborhood",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["history", "medieval", "architecture", "walking"],
                        "why_recommended": "Best-preserved medieval quarter in Europe"
                    },
                    {
                        "name": "Casa Batlló",
                        "category": "architecture",
                        "description": "Modernist building designed by Gaudí",
                        "rating": 4.6,
                        "price_range": "€25",
                        "opening_hours": "9:00-21:00",
                        "interests": ["architecture", "gaudi", "art", "modernism"],
                        "why_recommended": "Gaudí's architectural genius on display"
                    },
                    {
                        "name": "La Boqueria Market",
                        "category": "market",
                        "description": "Famous food market with local specialties",
                        "rating": 4.3,
                        "price_range": "€€",
                        "opening_hours": "8:00-20:30",
                        "interests": ["food", "markets", "local", "tapas"],
                        "why_recommended": "Best place to experience Catalan cuisine"
                    },
                    {
                        "name": "Barceloneta Beach",
                        "category": "beach",
                        "description": "Popular city beach with restaurants and bars",
                        "rating": 4.1,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["beaches", "relaxation", "swimming", "seafood"],
                        "why_recommended": "Perfect urban beach experience"
                    },
                    {
                        "name": "Picasso Museum",
                        "category": "museum",
                        "description": "Museum dedicated to Pablo Picasso's early work",
                        "rating": 4.4,
                        "price_range": "€12",
                        "opening_hours": "9:00-19:00",
                        "interests": ["art", "museums", "picasso", "culture"],
                        "why_recommended": "Extensive collection of Picasso's formative years"
                    }
                ]
            },
            "rome": {
                "country": "Italy",
                "coordinates": [12.4964, 41.9028],
                "places": [
                    {
                        "name": "Colosseum",
                        "category": "historical",
                        "description": "Ancient Roman amphitheater",
                        "rating": 4.6,
                        "price_range": "€12",
                        "opening_hours": "8:30-19:00",
                        "interests": ["history", "ancient", "roman", "gladiators"],
                        "why_recommended": "Most famous ancient amphitheater in the world"
                    },
                    {
                        "name": "Vatican City",
                        "category": "religious",
                        "description": "Independent city-state with St. Peter's Basilica",
                        "rating": 4.8,
                        "price_range": "€17",
                        "opening_hours": "8:00-18:00",
                        "interests": ["religious", "art", "sistine chapel", "papal"],
                        "why_recommended": "Spiritual center of Catholic world"
                    },
                    {
                        "name": "Trevi Fountain",
                        "category": "landmark",
                        "description": "Baroque fountain where visitors throw coins",
                        "rating": 4.5,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["landmarks", "baroque", "fountains", "tradition"],
                        "why_recommended": "Most famous fountain in the world"
                    },
                    {
                        "name": "Roman Forum",
                        "category": "historical",
                        "description": "Ancient Roman marketplace and political center",
                        "rating": 4.4,
                        "price_range": "€12",
                        "opening_hours": "8:30-19:00",
                        "interests": ["history", "ancient", "roman", "archaeology"],
                        "why_recommended": "Heart of ancient Roman civilization"
                    },
                    {
                        "name": "Pantheon",
                        "category": "historical",
                        "description": "Ancient Roman temple with massive dome",
                        "rating": 4.7,
                        "price_range": "Free",
                        "opening_hours": "8:30-19:30",
                        "interests": ["architecture", "ancient", "roman", "engineering"],
                        "why_recommended": "Best-preserved ancient Roman building"
                    },
                    {
                        "name": "Spanish Steps",
                        "category": "landmark",
                        "description": "Famous stairway with 135 steps",
                        "rating": 4.2,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["landmarks", "stairs", "shopping", "people watching"],
                        "why_recommended": "Iconic Roman meeting place"
                    },
                    {
                        "name": "Trastevere",
                        "category": "district",
                        "description": "Charming medieval neighborhood",
                        "rating": 4.5,
                        "price_range": "€€",
                        "opening_hours": "24/7",
                        "interests": ["medieval", "restaurants", "nightlife", "authentic"],
                        "why_recommended": "Most authentic Roman neighborhood"
                    },
                    {
                        "name": "Castel Sant'Angelo",
                        "category": "historical",
                        "description": "Towering cylindrical building in Parco Adriano",
                        "rating": 4.3,
                        "price_range": "€14",
                        "opening_hours": "9:00-19:30",
                        "interests": ["history", "castles", "views", "papal"],
                        "why_recommended": "Unique fortress with papal history"
                    }
                ]
            },
            "amsterdam": {
                "country": "Netherlands",
                "coordinates": [4.9041, 52.3676],
                "places": [
                    {
                        "name": "Anne Frank House",
                        "category": "museum",
                        "description": "Historic house where Anne Frank wrote her diary",
                        "rating": 4.6,
                        "price_range": "€14",
                        "opening_hours": "9:00-22:00",
                        "interests": ["history", "wwii", "memorial", "education"],
                        "why_recommended": "Moving memorial to Holocaust victim"
                    },
                    {
                        "name": "Van Gogh Museum",
                        "category": "museum",
                        "description": "World's largest collection of Van Gogh artwork",
                        "rating": 4.7,
                        "price_range": "€19",
                        "opening_hours": "9:00-17:00",
                        "interests": ["art", "museums", "van gogh", "post-impressionism"],
                        "why_recommended": "Unmatched collection of Van Gogh masterpieces"
                    },
                    {
                        "name": "Rijksmuseum",
                        "category": "museum",
                        "description": "Dutch national museum with Rembrandt and Vermeer",
                        "rating": 4.5,
                        "price_range": "€20",
                        "opening_hours": "9:00-17:00",
                        "interests": ["art", "museums", "dutch masters", "history"],
                        "why_recommended": "Premier collection of Dutch Golden Age art"
                    },
                    {
                        "name": "Jordaan District",
                        "category": "district",
                        "description": "Charming neighborhood with narrow streets and canals",
                        "rating": 4.4,
                        "price_range": "€€",
                        "opening_hours": "24/7",
                        "interests": ["canals", "boutiques", "cafes", "local life"],
                        "why_recommended": "Most picturesque Amsterdam neighborhood"
                    },
                    {
                        "name": "Canal Ring",
                        "category": "landmark",
                        "description": "Historic canal system and UNESCO World Heritage site",
                        "rating": 4.8,
                        "price_range": "Free (boat tours €15)",
                        "opening_hours": "24/7",
                        "interests": ["canals", "unesco", "boats", "architecture"],
                        "why_recommended": "Unique canal system defining Amsterdam"
                    },
                    {
                        "name": "Vondelpark",
                        "category": "park",
                        "description": "Large urban park popular with locals",
                        "rating": 4.3,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["parks", "relaxation", "cycling", "local life"],
                        "why_recommended": "Perfect for experiencing Dutch outdoor culture"
                    },
                    {
                        "name": "Red Light District",
                        "category": "district",
                        "description": "Historic area known for its liberal atmosphere",
                        "rating": 4.0,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["nightlife", "history", "liberal culture", "coffee shops"],
                        "why_recommended": "Unique cultural and historical area"
                    },
                    {
                        "name": "Bloemenmarkt",
                        "category": "market",
                        "description": "Floating flower market",
                        "rating": 4.2,
                        "price_range": "€€",
                        "opening_hours": "9:00-17:30",
                        "interests": ["flowers", "markets", "tulips", "unique"],
                        "why_recommended": "World's only floating flower market"
                    }
                ]
            },
            "dubai": {
                "country": "UAE",
                "coordinates": [55.2708, 25.2048],
                "places": [
                    {
                        "name": "Burj Khalifa",
                        "category": "landmark",
                        "description": "World's tallest building",
                        "rating": 4.6,
                        "price_range": "AED 149",
                        "opening_hours": "8:30-23:00",
                        "interests": ["landmarks", "modern", "views", "architecture"],
                        "why_recommended": "Tallest building in the world with stunning views"
                    },
                    {
                        "name": "Dubai Mall",
                        "category": "shopping",
                        "description": "World's largest mall by total area",
                        "rating": 4.5,
                        "price_range": "€€€",
                        "opening_hours": "10:00-24:00",
                        "interests": ["shopping", "luxury", "entertainment", "dining"],
                        "why_recommended": "Ultimate shopping and entertainment destination"
                    },
                    {
                        "name": "Palm Jumeirah",
                        "category": "landmark",
                        "description": "Artificial island shaped like a palm tree",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["modern", "engineering", "beaches", "luxury"],
                        "why_recommended": "Engineering marvel visible from space"
                    },
                    {
                        "name": "Dubai Marina",
                        "category": "district",
                        "description": "Artificial canal city with skyscrapers",
                        "rating": 4.3,
                        "price_range": "€€€",
                        "opening_hours": "24/7",
                        "interests": ["modern", "yachts", "dining", "nightlife"],
                        "why_recommended": "Stunning waterfront with world-class dining"
                    },
                    {
                        "name": "Gold Souk",
                        "category": "market",
                        "description": "Traditional gold jewelry market",
                        "rating": 4.2,
                        "price_range": "€€€€",
                        "opening_hours": "10:00-22:00",
                        "interests": ["gold", "jewelry", "traditional", "markets"],
                        "why_recommended": "Largest gold market in the world"
                    },
                    {
                        "name": "Jumeirah Beach",
                        "category": "beach",
                        "description": "Beautiful white sand beach",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["beaches", "swimming", "relaxation", "water sports"],
                        "why_recommended": "Perfect beach with view of Burj Al Arab"
                    },
                    {
                        "name": "Dubai Fountain",
                        "category": "attraction",
                        "description": "Choreographed fountain system",
                        "rating": 4.5,
                        "price_range": "Free",
                        "opening_hours": "18:00-23:00",
                        "interests": ["fountains", "shows", "music", "evening"],
                        "why_recommended": "World's largest choreographed fountain system"
                    },
                    {
                        "name": "Spice Souk",
                        "category": "market",
                        "description": "Traditional spice and herb market",
                        "rating": 4.1,
                        "price_range": "€€",
                        "opening_hours": "10:00-22:00",
                        "interests": ["spices", "traditional", "markets", "aromatics"],
                        "why_recommended": "Authentic Middle Eastern market experience"
                    }
                ]
            },
            "sydney": {
                "country": "Australia",
                "coordinates": [151.2093, -33.8688],
                "places": [
                    {
                        "name": "Sydney Opera House",
                        "category": "landmark",
                        "description": "Iconic performing arts venue",
                        "rating": 4.7,
                        "price_range": "AUD 43",
                        "opening_hours": "9:00-20:30",
                        "interests": ["architecture", "opera", "landmarks", "performing arts"],
                        "why_recommended": "UNESCO World Heritage architectural masterpiece"
                    },
                    {
                        "name": "Sydney Harbour Bridge",
                        "category": "landmark",
                        "description": "Steel arch bridge connecting Sydney CBD",
                        "rating": 4.6,
                        "price_range": "Free (climb AUD 174)",
                        "opening_hours": "24/7",
                        "interests": ["bridges", "views", "climbing", "architecture"],
                        "why_recommended": "Iconic bridge with harbor views"
                    },
                    {
                        "name": "Bondi Beach",
                        "category": "beach",
                        "description": "Famous beach with golden sand",
                        "rating": 4.3,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["beaches", "surfing", "swimming", "coastal walks"],
                        "why_recommended": "Australia's most famous beach"
                    },
                    {
                        "name": "The Rocks",
                        "category": "district",
                        "description": "Historic area with cobblestone streets",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["history", "markets", "pubs", "cobblestones"],
                        "why_recommended": "Birthplace of modern Australia"
                    },
                    {
                        "name": "Royal Botanic Gardens",
                        "category": "park",
                        "description": "Botanic gardens with harbor views",
                        "rating": 4.5,
                        "price_range": "Free",
                        "opening_hours": "7:00-17:30",
                        "interests": ["gardens", "nature", "views", "walking"],
                        "why_recommended": "Beautiful gardens with perfect harbor views"
                    },
                    {
                        "name": "Darling Harbour",
                        "category": "district",
                        "description": "Waterfront area with attractions",
                        "rating": 4.2,
                        "price_range": "€€",
                        "opening_hours": "24/7",
                        "interests": ["waterfront", "dining", "entertainment", "aquarium"],
                        "why_recommended": "Perfect family entertainment precinct"
                    },
                    {
                        "name": "Manly Beach",
                        "category": "beach",
                        "description": "Popular beach accessible by ferry",
                        "rating": 4.4,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["beaches", "ferry", "surfing", "promenade"],
                        "why_recommended": "Beautiful beach with scenic ferry ride"
                    },
                    {
                        "name": "Circular Quay",
                        "category": "transport",
                        "description": "Harbor transport hub with views",
                        "rating": 4.3,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["harbors", "transport", "views", "ferries"],
                        "why_recommended": "Perfect starting point for harbor exploration"
                    }
                ]
            },
            "singapore": {
                "country": "Singapore",
                "coordinates": [103.8198, 1.3521],
                "places": [
                    {
                        "name": "Marina Bay Sands",
                        "category": "landmark",
                        "description": "Iconic hotel and casino complex",
                        "rating": 4.5,
                        "price_range": "SGD 23",
                        "opening_hours": "24/7",
                        "interests": ["modern", "architecture", "views", "luxury"],
                        "why_recommended": "Iconic skyline landmark with infinity pool"
                    },
                    {
                        "name": "Gardens by the Bay",
                        "category": "park",
                        "description": "Futuristic park with Supertree Grove",
                        "rating": 4.6,
                        "price_range": "SGD 28",
                        "opening_hours": "5:00-2:00",
                        "interests": ["gardens", "futuristic", "nature", "technology"],
                        "why_recommended": "Stunning fusion of nature and technology"
                    },
                    {
                        "name": "Merlion Park",
                        "category": "landmark",
                        "description": "Park featuring Singapore's iconic Merlion statue",
                        "rating": 4.2,
                        "price_range": "Free",
                        "opening_hours": "24/7",
                        "interests": ["landmarks", "symbols", "views", "photography"],
                        "why_recommended": "Singapore's most recognizable symbol"
                    },
                    {
                        "name": "Chinatown",
                        "category": "district",
                        "description": "Historic district with temples and street food",
                        "rating": 4.3,
                        "price_range": "€€",
                        "opening_hours": "24/7",
                        "interests": ["culture", "food", "temples", "heritage"],
                        "why_recommended": "Authentic Chinese culture and cuisine"
                    },
                    {
                        "name": "Little India",
                        "category": "district",
                        "description": "Vibrant Indian cultural district",
                        "rating": 4.1,
                        "price_range": "€€",
                        "opening_hours": "24/7",
                        "interests": ["culture", "indian", "temples", "spices"],
                        "why_recommended": "Immersive Indian cultural experience"
                    },
                    {
                        "name": "Sentosa Island",
                        "category": "island",
                        "description": "Resort island with beaches and attractions",
                        "rating": 4.4,
                        "price_range": "SGD 4",
                        "opening_hours": "24/7",
                        "interests": ["beaches", "theme parks", "resorts", "entertainment"],
                        "why_recommended": "Perfect family entertainment destination"
                    },
                    {
                        "name": "Hawker Centers",
                        "category": "food",
                        "description": "Open-air food courts with local cuisine",
                        "rating": 4.7,
                        "price_range": "SGD 3-8",
                        "opening_hours": "10:00-22:00",
                        "interests": ["food", "local", "cheap eats", "variety"],
                        "why_recommended": "Best way to experience Singapore's food culture"
                    },
                    {
                        "name": "Clarke Quay",
                        "category": "district",
                        "description": "Riverside entertainment district",
                        "rating": 4.2,
                        "price_range": "€€€",
                        "opening_hours": "18:00-2:00",
                        "interests": ["nightlife", "dining", "riverside", "entertainment"],
                        "why_recommended": "Premier nightlife destination"
                    }
                ]
            },
            "bangkok": {
                "country": "Thailand",
                "coordinates": [100.5018, 13.7563],
                "places": [
                    {
                        "name": "Grand Palace",
                        "category": "historical",
                        "description": "Former royal residence with ornate architecture",
                        "rating": 4.4,
                        "price_range": "THB 500",
                        "opening_hours": "8:30-15:30",
                        "interests": ["palaces", "thai architecture", "history", "royal"],
                        "why_recommended": "Most important architectural site in Thailand"
                    },
                    {
                        "name": "Wat Pho",
                        "category": "religious",
                        "description": "Temple complex with giant reclining Buddha",
                        "rating": 4.5,
                        "price_range": "THB 100",
                        "opening_hours": "8:00-18:30",
                        "interests": ["temples", "buddha", "massage", "religious"],
                        "why_recommended": "Home to traditional Thai massage"
                    },
                    {
                        "name": "Wat Arun",
                        "category": "religious",
                        "description": "Temple of Dawn with stunning spires",
                        "rating": 4.6,
                        "price_range": "THB 50",
                        "opening_hours": "8:00-18:00",
                        "interests": ["temples", "architecture", "river views", "sunrise"],
                        "why_recommended": "Most beautiful temple in Bangkok"
                    },
                    {
                        "name": "Chatuchak Weekend Market",
                        "category": "market",
                        "description": "Massive weekend market with everything",
                        "rating": 4.3,
                        "price_range": "THB 50-500",
                        "opening_hours": "9:00-18:00",
                        "interests": ["markets", "shopping", "local products", "food"],
                        "why_recommended": "Largest weekend market in the world"
                    },
                    {
                        "name": "Khao San Road",
                        "category": "street",
                        "description": "Famous backpacker street with bars and food",
                        "rating": 4.1,
                        "price_range": "THB 50-200",
                        "opening_hours": "18:00-2:00",
                        "interests": ["backpacker", "nightlife", "street food", "budget"],
                        "why_recommended": "Legendary backpacker destination"
                    },
                    {
                        "name": "Floating Markets",
                        "category": "market",
                        "description": "Traditional markets on water",
                        "rating": 4.2,
                        "price_range": "THB 100-300",
                        "opening_hours": "7:00-12:00",
                        "interests": ["markets", "boats", "traditional", "food"],
                        "why_recommended": "Unique traditional Thai market experience"
                    },
                    {
                        "name": "Jim Thompson House",
                        "category": "museum",
                        "description": "Traditional Thai house museum",
                        "rating": 4.3,
                        "price_range": "THB 150",
                        "opening_hours": "9:00-18:00",
                        "interests": ["museums", "architecture", "silk", "traditional"],
                        "why_recommended": "Beautiful example of traditional Thai architecture"
                    },
                    {
                        "name": "Lumphini Park",
                        "category": "park",
                        "description": "Large park in the city center",
                        "rating": 4.2,
                        "price_range": "Free",
                        "opening_hours": "4:30-21:00",
                        "interests": ["parks", "jogging", "tai chi", "relaxation"],
                        "why_recommended": "Green oasis in bustling Bangkok"
                    }
                ]
            }
        }
    
    async def discover_places(self, location: str, interests: List[str], 
                             travel_dates: Optional[str] = None, 
                             budget: Optional[str] = None) -> LocalDiscoveryData:
        """
        Discover famous places and attractions based on location and interests
        """
        # Normalize location for lookup
        location_key = location.lower().replace(" ", "").split(",")[0]
        
        # Get places data for the location
        city_data = self.places_database.get(location_key)
        
        if not city_data:
            # If city not in database, use AI to generate places
            return await self._generate_places_with_ai(location, interests, travel_dates, budget)
        
        # Filter places based on interests
        filtered_places = self._filter_places_by_interests(city_data["places"], interests)
        
        # Convert to LocalDiscoveryData format
        return self._convert_to_discovery_data(location, interests, filtered_places)
    
    def _filter_places_by_interests(self, places: List[Dict], interests: List[str]) -> List[Dict]:
        """Filter places based on user interests"""
        if not interests:
            return places[:10]  # Return top 10 if no specific interests
        
        # Normalize interests for matching
        normalized_interests = [interest.lower().strip() for interest in interests]
        
        # Score places based on interest matching
        scored_places = []
        for place in places:
            place_interests = [i.lower() for i in place.get("interests", [])]
            score = 0
            
            # Calculate relevance score
            for interest in normalized_interests:
                for place_interest in place_interests:
                    if interest in place_interest or place_interest in interest:
                        score += 1
                # Also check category
                if interest in place.get("category", "").lower():
                    score += 0.5
                # Check description
                if interest in place.get("description", "").lower():
                    score += 0.3
            
            if score > 0:
                scored_places.append((place, score))
        
        # Sort by score and return top places
        scored_places.sort(key=lambda x: x[1], reverse=True)
        return [place for place, score in scored_places[:12]]
    
    def _convert_to_discovery_data(self, location: str, interests: List[str], 
                                  places: List[Dict]) -> LocalDiscoveryData:
        """Convert places data to LocalDiscoveryData format"""
        
        experiences = []
        restaurants = []
        attractions = []
        events = []
        
        for place in places:
            # Create LocalExperience
            experience = LocalExperience(
                name=place["name"],
                description=place["description"],
                category=place["category"],
                location=location,
                price_range=place.get("price_range"),
                rating=place.get("rating"),
                opening_hours=place.get("opening_hours"),
                booking_required=place.get("booking_required", False),
                contact_info=place.get("contact_info"),
                why_recommended=place["why_recommended"],
                seasonal_info=place.get("seasonal_info")
            )
            experiences.append(experience)
            
            # Categorize for different lists
            if place["category"] in ["restaurant", "food", "market"]:
                restaurants.append({
                    "name": place["name"],
                    "cuisine": place.get("cuisine", "Local"),
                    "rating": place.get("rating"),
                    "price_range": place.get("price_range"),
                    "location": location
                })
            elif place["category"] in ["landmark", "museum", "historical", "park"]:
                attractions.append({
                    "name": place["name"],
                    "category": place["category"],
                    "rating": place.get("rating"),
                    "description": place["description"],
                    "location": location
                })
        
        # Generate some sample events (in real implementation, these would come from events APIs)
        events = self._generate_sample_events(location)
        
        return LocalDiscoveryData(
            location=location,
            interests=interests,
            total_results=len(experiences),
            experiences=experiences,
            events=events,
            restaurants=restaurants,
            attractions=attractions,
            deals=self._generate_sample_deals(location)
        )
    
    def _generate_sample_events(self, location: str) -> List[Dict[str, Any]]:
        """Generate sample events for the location"""
        base_events = [
            {"name": "Local Food Festival", "date": "This weekend", "location": location},
            {"name": "Art Gallery Opening", "date": "Next Friday", "location": location},
            {"name": "Cultural Performance", "date": "Every evening", "location": location},
            {"name": "Night Market", "date": "Wednesday & Saturday", "location": location},
            {"name": "Walking Tour", "date": "Daily", "location": location}
        ]
        
        # Return 2-3 random events
        return random.sample(base_events, min(3, len(base_events)))
    
    def _generate_sample_deals(self, location: str) -> List[Dict[str, Any]]:
        """Generate sample deals for the location"""
        return [
            {"description": "10% off museum admissions", "discount": "10%", "expires": "End of month"},
            {"description": "Free walking tour booking", "discount": "100%", "expires": "Limited time"},
            {"description": "Happy hour at local restaurants", "discount": "20%", "expires": "Daily 4-6 PM"}
        ]
    
    async def _generate_places_with_ai(self, location: str, interests: List[str], 
                                     travel_dates: Optional[str] = None, 
                                     budget: Optional[str] = None) -> LocalDiscoveryData:
        """Use AI to generate places for cities not in database"""
        try:
            import os
            import google.generativeai as genai
            
            # Configure Gemini
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return self._fallback_discovery_data(location, interests)
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            interests_str = ", ".join(interests)
            context = f"Travel Dates: {travel_dates}, Budget: {budget}" if travel_dates or budget else ""
            
            prompt = f"""
            Generate a list of famous places and attractions for {location} based on these interests: {interests_str}
            {context}
            
            For each place, provide:
            1. Name
            2. Category (landmark, museum, restaurant, park, etc.)
            3. Brief description
            4. Rating (1-5)
            5. Price range
            6. Opening hours
            7. Why it's recommended
            
            Focus on well-known, authentic places that match the interests. Provide at least 8-10 places.
            Format as JSON with this structure:
            {{
                "places": [
                    {{
                        "name": "Place Name",
                        "category": "landmark",
                        "description": "Brief description",
                        "rating": 4.5,
                        "price_range": "$10-20",
                        "opening_hours": "9:00-17:00",
                        "why_recommended": "Reason why this place is special"
                    }}
                ]
            }}
            """
            
            response = model.generate_content(prompt)
            
            # Parse AI response and convert to LocalDiscoveryData
            # This is a simplified implementation - in practice, you'd need robust JSON parsing
            places_data = self._parse_ai_response(response.text, location, interests)
            return places_data
            
        except Exception as e:
            print(f"Error generating AI places: {e}")
            return self._fallback_discovery_data(location, interests)
    
    def _parse_ai_response(self, ai_response: str, location: str, interests: List[str]) -> LocalDiscoveryData:
        """Parse AI response into LocalDiscoveryData format"""
        try:
            # Try to extract JSON from AI response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                places = data.get("places", [])
                
                return self._convert_to_discovery_data(location, interests, places)
            else:
                # If no JSON found, return fallback
                return self._fallback_discovery_data(location, interests)
                
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._fallback_discovery_data(location, interests)
    
    def _fallback_discovery_data(self, location: str, interests: List[str]) -> LocalDiscoveryData:
        """Fallback data when AI or database fails"""
        fallback_places = [
            {
                "name": "City Center",
                "category": "district",
                "description": "Main city center with shops and restaurants",
                "rating": 4.0,
                "price_range": "Free",
                "opening_hours": "24/7",
                "why_recommended": "Heart of the city"
            },
            {
                "name": "Central Museum",
                "category": "museum",
                "description": "Main city museum with local history",
                "rating": 4.2,
                "price_range": "$10-15",
                "opening_hours": "10:00-17:00",
                "why_recommended": "Learn about local culture and history"
            },
            {
                "name": "Historic District",
                "category": "historical",
                "description": "Old part of town with historic buildings",
                "rating": 4.1,
                "price_range": "Free",
                "opening_hours": "24/7",
                "why_recommended": "Beautiful historic architecture"
            },
            {
                "name": "Local Market",
                "category": "market",
                "description": "Traditional market with local products",
                "rating": 4.3,
                "price_range": "$5-20",
                "opening_hours": "8:00-18:00",
                "why_recommended": "Authentic local experience"
            }
        ]
        
        return self._convert_to_discovery_data(location, interests, fallback_places) 