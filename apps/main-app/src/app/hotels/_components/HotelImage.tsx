"use client";

import Image from "next/image";

interface HotelImageProps {
  hotelName: string;
}

export function HotelImage({ hotelName }: HotelImageProps) {
  return (
    <div className="relative h-48 w-full">
      <Image
        src="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
        alt={hotelName}
        fill
        className="object-cover transition-transform duration-300 group-hover:scale-105"
      />
    </div>
  );
} 