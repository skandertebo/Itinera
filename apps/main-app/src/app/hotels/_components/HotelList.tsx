"use client";

import { api } from "@/trpc/react";
import type { Hotel } from "@/types";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { HotelCard } from "./HotelCard";

export function HotelList() {
  const searchParams = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);
  const hotelsPerPage = 6;

  const { data, isLoading } = api.hotels.getHotels.useQuery({
    country: searchParams.get("country") ?? undefined,
    city: searchParams.get("city") ?? undefined,
    rating: searchParams.get("rating") ?? undefined,
    facilities: searchParams.get("facilities") ?? undefined,
    page: currentPage,
    limit: hotelsPerPage,
  });

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent"></div>
      </div>
    );
  }

  if (!data?.hotels?.length) {
    return (
      <div className="flex h-96 flex-col items-center justify-center text-center">
        <h3 className="text-lg font-semibold text-gray-900">No hotels found</h3>
        <p className="mt-2 text-sm text-gray-600">
          Try adjusting your filters to find more hotels.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Hotels Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {data.hotels.map((hotel: Hotel) => (
          <HotelCard key={hotel.id} hotel={hotel} />
        ))}
      </div>

      {/* Pagination */}
      {data.totalPages > 1 && (
        <div className="flex items-center justify-center space-x-2">
          <button
            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="rounded-md bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page {currentPage} of {data.totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((prev) => Math.min(prev + 1, data.totalPages))}
            disabled={currentPage === data.totalPages}
            className="rounded-md bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
} 