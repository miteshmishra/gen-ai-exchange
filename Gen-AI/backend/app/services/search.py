from typing import Dict, Any, List
import random
import asyncio
from ..models.search import SearchQuery, Hotel, Location

class SearchService:
    @staticmethod
    async def search_hotels(query: SearchQuery) -> Dict[str, Any]:
        """
        Search for hotels based on the provided criteria.
        This is a mock implementation that generates random hotel data.
        """
        await asyncio.sleep(random.uniform(0.2, 0.6))  # Simulate network delay
        hotels = []
        
        for i in range(random.randint(5, 12)):
            hotels.append({
                "id": f"HT{random.randint(1000, 9999)}",
                "name": f"Hotel {random.choice(['Grand', 'Royal', 'Premium', 'Plaza'])} {random.choice(['Central', 'Downtown', 'Plaza', 'Bay'])}",
                "location": {
                    "city": query.destination,
                    "address": f"{random.randint(100, 999)} Main St",
                    "coordinates": {
                        "lat": round(random.uniform(25, 48), 6),
                        "lng": round(random.uniform(-120, -70), 6)
                    }
                },
                "rating": round(random.uniform(3.5, 5.0), 1),
                "price_per_night": random.randint(80, 400),
                "amenities": random.sample([
                    "WiFi", "Pool", "Gym", "Spa", "Restaurant",
                    "Bar", "Parking", "Pet Friendly", "Business Center"
                ], random.randint(3, 6)),
                "images": [f"https://picsum.photos/300/200?random={i}"],
                "availability": True
            })
        
        return {
            "hotels": hotels,
            "total": len(hotels)
        }

    @staticmethod
    async def search_flights(query: SearchQuery) -> Dict[str, Any]:
        """
        Search for flights based on the provided criteria.
        This is a mock implementation that generates random flight data.
        """
        await asyncio.sleep(random.uniform(0.2, 0.6))
        flights = []

        airlines = ["SkyWings", "Global Air", "Ocean Pacific", "Mountain Express"]
        for i in range(random.randint(3, 8)):
            airline = random.choice(airlines)
            base_price = random.randint(200, 1000)
            flights.append({
                "id": f"FL{random.randint(1000, 9999)}",
                "airline": airline,
                "flight_number": f"{airline[:2].upper()}{random.randint(100, 999)}",
                "departure": {
                    "city": query.origin,
                    "time": "10:00 AM",  # Simplified for demo
                    "date": query.dateFrom
                },
                "arrival": {
                    "city": query.destination,
                    "time": "12:00 PM",  # Simplified for demo
                    "date": query.dateFrom
                },
                "duration": "2h 00m",
                "price": {
                    "economy": base_price,
                    "business": base_price * 2.5,
                    "first": base_price * 4
                },
                "seats_available": random.randint(1, 50)
            })

        return {
            "flights": flights,
            "total": len(flights)
        }

    @staticmethod
    async def search_experiences(query: SearchQuery) -> Dict[str, Any]:
        """
        Search for experiences based on the provided criteria.
        This is a mock implementation that generates random experience data.
        """
        await asyncio.sleep(random.uniform(0.2, 0.6))
        experiences = []

        experience_types = [
            "City Tour", "Food Tasting", "Museum Visit", "Adventure",
            "Workshop", "Concert", "Sports Event", "Cultural Experience"
        ]

        for i in range(random.randint(4, 10)):
            exp_type = random.choice(experience_types)
            base_price = random.randint(30, 200)
            experiences.append({
                "id": f"EX{random.randint(1000, 9999)}",
                "title": f"{query.destination} {exp_type}",
                "type": exp_type,
                "description": f"Experience the best of {query.destination} with our guided {exp_type.lower()}",
                "duration": f"{random.randint(1, 6)} hours",
                "price": base_price,
                "rating": round(random.uniform(4.0, 5.0), 1),
                "reviews_count": random.randint(10, 200),
                "availability": {
                    "date": query.dateFrom,
                    "slots_available": random.randint(1, 20)
                },
                "includes": random.sample([
                    "Guide", "Transportation", "Meals", "Equipment",
                    "Photos", "Souvenirs", "Insurance"
                ], random.randint(2, 4)),
                "image": f"https://picsum.photos/300/200?random={i}"
            })

        return {
            "experiences": experiences,
            "total": len(experiences)
        }
