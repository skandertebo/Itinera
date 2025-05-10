"use client";

import type { api } from "@/trpc/server";
import Link from "next/link";
import { HotelDescription } from "./HotelDescription";
import { HotelFacilities } from "./HotelFacilities";
import { HotelHeader } from "./HotelHeader";
import { HotelImage } from "./HotelImage";
import { HotelLocation } from "./HotelLocation";

type Hotel = Awaited<ReturnType<typeof api.hotels.getHotels>>['hotels'][number];

interface HotelCardProps {
  hotel: Hotel;
}

export function HotelCard({ hotel }: HotelCardProps) {
  return (
    <Link
      href={`/hotels/${hotel.id}`}
      className="group overflow-hidden rounded-lg bg-white shadow-sm transition-all hover:shadow-md"
    >
      <HotelImage hotelName={hotel.hotel_name} />
      <div className="p-4">
        <HotelHeader hotelName={hotel.hotel_name} rating={hotel.hotel_rating} />
        <HotelLocation cityName={hotel.city_name} countryName={hotel.country_name} />
        <HotelDescription description={hotel.description} />
        <div className="flex items-center justify-between">
          <HotelFacilities facilities={hotel.hotel_facilities} />
          <span className="text-sm font-medium text-indigo-600 group-hover:text-indigo-500">
            View Details →
          </span>
        </div>
      </div>
    </Link>
  );
} 