"use client";

interface HotelLocationProps {
  cityName: string;
  countryName: string;
}

export function HotelLocation({ cityName, countryName }: HotelLocationProps) {
  return (
    <p className="mb-2 text-sm text-gray-600">
      {cityName}, {countryName}
    </p>
  );
} 