"use client";

import { DEFAULT_HOTEL_IMAGE } from "@/constants";
import { api } from "@/trpc/react";
import { useSession } from "next-auth/react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface Props {
  hotel: {
    id: string;
    hotel_name: string;
    hotel_rating: string | null;
    description: string | null;
    hotel_facilities: string | null;
    city_name: string;
    country_name: string;
  };
}

export function FavoriteHotelCard({ hotel }: Props) {
  const { data: session } = useSession();
  const router = useRouter();

  const { data: isFavorite, isLoading: isLoadingFavorite, refetch } = api.hotels.isFavorite.useQuery(
    { hotelId: hotel.id },
    { enabled: !!session },
  );

  const toggleFavorite = api.hotels.toggleFavorite.useMutation({
    onSuccess: () => {
      // Optimistically update the UI
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
      className="group relative overflow-hidden rounded-lg bg-white shadow-md transition-all hover:shadow-lg"
    >
      <div className="relative h-48 w-full">
        <Image
          src={DEFAULT_HOTEL_IMAGE}
          alt={hotel.hotel_name}
          fill
          className="object-cover transition-transform duration-300 group-hover:scale-105"
        />
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
        <div className="mb-2 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">{hotel.hotel_name}</h3>
          {hotel.hotel_rating && (
            <span className="rounded bg-indigo-100 px-2 py-1 text-sm font-medium text-indigo-800">
              {hotel.hotel_rating} ★
            </span>
          )}
        </div>
        <p className="mb-2 text-sm text-gray-600">
          {hotel.city_name}, {hotel.country_name}
        </p>
        {hotel.description && (
          <p className="mb-2 line-clamp-2 text-sm text-gray-600" dangerouslySetInnerHTML={{ __html: hotel.description }} />
        )}
        {hotel.hotel_facilities && (
          <div className="mt-2 flex flex-wrap gap-1">
            {hotel.hotel_facilities.split(",").slice(0, 3).map((facility, index) => (
              <span
                key={index}
                className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600"
              >
                {facility.trim()}
              </span>
            ))}
            {hotel.hotel_facilities.split(",").length > 3 && (
              <span className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600">
                +{hotel.hotel_facilities.split(",").length - 3} more
              </span>
            )}
          </div>
        )}
      </div>
    </Link>
  );
} 