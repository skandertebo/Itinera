"use client";

import { DEFAULT_HOTEL_IMAGE } from "@/constants";
import Image from "next/image";

interface HotelImageProps {
  hotelName: string;
}

export function HotelImage({ hotelName }: HotelImageProps) {
  return (
    <div className="relative h-48 w-full">
      <Image
        src={DEFAULT_HOTEL_IMAGE}
        alt={hotelName}
        fill
        className="object-cover transition-transform duration-300 group-hover:scale-105"
      />
    </div>
  );
} 