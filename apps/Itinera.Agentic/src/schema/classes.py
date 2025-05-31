from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import date


class Destination(BaseModel):
    city: str = Field(None, description="City of the travel destination", example="Paris")
    country: str = Field(None, description="Country of the travel destination", example="France")


class Travelers(BaseModel):
    adults: int = Field(..., ge=1, description="Number of adult travelers", example=2)
    children: int = Field(..., ge=0, description="Number of child travelers", example=1)
    companions: Optional[str] = Field(
        None,
        description="Who the client is traveling with",
        example="family"
    )


class Accommodation(BaseModel):
    rooms: int = Field(..., ge=1, description="Number of rooms required", example=1)
    room_types: List[str] = Field(
        ...,
        description="Preferred room types",
        example=["standard", "family"]
    )


class Budget(BaseModel):
    min: float = Field(..., ge=0, description="Minimum budget for the trip (in USD)", example=1000)
    max: float = Field(..., ge=0, description="Maximum budget for the trip (in USD)", example=2000)


class TravelRequirements(BaseModel):
    destination: Destination
    check_in: date = Field(..., description="Check-in date (YYYY-MM-DD)", example="2025-07-01")
    check_out: date = Field(..., description="Check-out date (YYYY-MM-DD)", example="2025-07-07")
    travelers: Travelers
    accommodation: Accommodation
    budget: Budget
    travel_purpose: Optional[str] = Field(None, description="Main purpose of the trip", example="leisure")
    preferred_activities: Optional[List[str]] = Field(
        None,
        description="Activities or interests influencing destination choice",
    )
    travel_history: Optional[str] = Field(
        None,
        description="Client's travel history context",
    )
    preferred_climate: Optional[str] = Field(
        None,
        description="Preferred climate or season for the destination",
    )
    special_requirements: Optional[List[str]] = Field(
        None,
        description="Special needs or preferences",
    )
    user_currency:str= Field(
        None,
        description="User's preferred currency",
    )
    user_country:str = Field(
        None,
        description="User's country",
    )
    user_language: str = Field(
        None,
        description="User's preferred language",
    )

class Pricing(BaseModel):
    room_type: str = Field(..., description="Type of the room")
    price: str = Field(..., description="Price for the room (e.g., '$200')")


class BookingResult(BaseModel):
    name: str = Field(..., description="Name of the hotel")
    url: str = Field(..., description="URL to the hotel listing")
    rating: str = Field(..., description="Hotel rating (e.g., '8.5')")
    description: str = Field(..., description="Description of the hotel")
    facilities: Optional[List[str]] = Field(None, description="List of hotel facilities")
    surroundings: Dict[str, Any] = Field(default_factory=dict, description="Nearby points of interest or surroundings")
    detailed_ratings: Dict[str, str] = Field(default_factory=dict, description="Detailed ratings by category (e.g., cleanliness, location)")
    pricing: Optional[List[Pricing]] = Field(None, description="List of pricing options per room type")