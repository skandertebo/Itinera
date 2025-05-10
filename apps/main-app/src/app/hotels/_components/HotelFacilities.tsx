"use client";

interface HotelFacilitiesProps {
  facilities: string | null;
}

export function HotelFacilities({ facilities }: HotelFacilitiesProps) {
  if (!facilities) return null;

  return (
    <div className="flex max-h-[3.5rem] flex-wrap gap-1 overflow-hidden truncate">
      {facilities.split(",").slice(0, 3).map((facility: string, index: number) => (
        <span
          key={index}
          className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
        >
          {facility.trim()}
        </span>
      ))}
    </div>
  );
} 