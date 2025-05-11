"use client";

import { api } from "@/trpc/react";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { HotelDescription } from "./HotelDescription";
import { HotelFacilities } from "./HotelFacilities";
import { HotelHeader } from "./HotelHeader";
import { HotelImage } from "./HotelImage";
import { HotelLocation } from "./HotelLocation";

interface Hotel {
  id: string;
  hotel_name: string;
  hotel_rating: string | null;
  description: string | null;
  hotel_facilities: string | null;
  city_name: string;
  country_name: string;
}

interface HotelCardProps {
  hotel: Hotel;
}

export function HotelCard({ hotel }: HotelCardProps) {
  const { data: session } = useSession();
  const router = useRouter();

  const { data: isFavorite, isLoading: isLoadingFavorite, refetch } = api.hotels.isFavorite.useQuery(
    { hotelId: hotel.id },
    { enabled: !!session },
  );

  const toggleFavorite = api.hotels.toggleFavorite.useMutation({
    onSuccess: () => {
      void refetch();
    },
  });

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!session) {
      router.push("/api/auth/signin");
      return;
    }
    toggleFavorite.mutate({ hotelId: hotel.id });
  };

  const isButtonLoading = isLoadingFavorite || toggleFavorite.isPending;

  return (
    <Link
      href={`/hotels/${hotel.id}`}
      className="group relative overflow-hidden rounded-lg bg-white shadow-sm transition-all hover:shadow-md"
    >
      <div className="relative">
        <HotelImage hotelName={hotel.hotel_name} />
        <button
          onClick={handleFavoriteClick}
          disabled={isButtonLoading}
          className={`absolute right-2 top-2 rounded-full p-2 transition-colors ${
            isFavorite
              ? "bg-red-500 text-white hover:bg-red-600"
              : "bg-white/80 text-gray-600 hover:bg-white"
          } ${isButtonLoading ? "opacity-50 cursor-not-allowed" : ""}`}
          title={session ? (isFavorite ? "Remove from favorites" : "Add to favorites") : "Sign in to add favorites"}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="h-6 w-6"
          >
            <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
          </svg>
        </button>
      </div>
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