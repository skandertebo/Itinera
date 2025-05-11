"use client";

interface HotelHeaderProps {
  hotelName: string;
  rating: string | null;
}

export function HotelHeader({ hotelName, rating }: HotelHeaderProps) {
  return (
    <div className="mb-2 flex items-center justify-between">
      <h3 className="text-lg font-semibold text-gray-900 group-hover:text-indigo-600">
        {hotelName}
      </h3>
      {rating && (
        <span className="rounded-full bg-yellow-100 px-2.5 py-0.5 text-sm font-medium text-yellow-800">
          {rating}
        </span>
      )}
    </div>
  );
} 