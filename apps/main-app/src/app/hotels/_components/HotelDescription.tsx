"use client";

interface HotelDescriptionProps {
  description: string | null;
}

export function HotelDescription({ description }: HotelDescriptionProps) {
  if (!description) return null;

  return (
    <p
      className="mb-4 line-clamp-2 text-sm text-gray-500"
      dangerouslySetInnerHTML={{ __html: description }}
    />
  );
} 