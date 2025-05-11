"use client";

import { api } from "@/trpc/react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { FavoriteHotelCard } from "../_components/FavoriteHotelCard";

export default function FavoritesPage() {
  const { status } = useSession();
  const router = useRouter();
  const { data: favoriteHotels, isLoading, error } = api.hotels.getFavorites.useQuery(
    undefined,
    {
      enabled: status === "authenticated",
    },
  );

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/api/auth/signin");
    }
  }, [status, router]);

  if (status === "loading" || isLoading) {
    return (
      <div className="flex min-h-[50vh] flex-col items-center justify-center">
        <div className="h-32 w-32 animate-spin rounded-full border-b-2 border-t-2 border-indigo-500"></div>
        <p className="mt-4 text-gray-600">Loading your favorite hotels...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-[50vh] flex-col items-center justify-center">
        <div className="rounded-lg bg-red-50 p-4">
          <h2 className="mb-2 text-xl font-semibold text-red-800">Error loading favorites</h2>
          <p className="text-red-600">{error.message}</p>
        </div>
      </div>
    );
  }

  if (!favoriteHotels?.length) {
    return (
      <div className="flex min-h-[50vh] flex-col items-center justify-center">
        <div className="text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
          <h2 className="mt-4 text-2xl font-semibold text-gray-900">
            No favorite hotels yet
          </h2>
          <p className="mt-2 text-gray-600">
            Start adding hotels to your favorites to see them here!
          </p>
          <button
            onClick={() => router.push("/hotels")}
            className="mt-4 rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500"
          >
            Browse Hotels
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Your Favorite Hotels</h1>
        <p className="mt-2 text-gray-600">
          Browse through your saved hotels and start planning your next stay.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {favoriteHotels.map((hotel) => (
          <FavoriteHotelCard key={hotel.id} hotel={hotel} />
        ))}
      </div>
    </div>
  );
} 